#!/usr/bin/env python3
"""
E0469 Payer Coverage Dashboard
Flask web application for viewing and managing payer coverage data.
"""

from flask import Flask, request, jsonify, render_template, Response
import psycopg2
from psycopg2.extras import RealDictCursor
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
import os
import requests
import re
from functools import wraps

app = Flask(__name__)

# Basic Auth Configuration
AUTH_USERNAME = os.environ.get("AUTH_USERNAME", "payer")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD", "")

def check_auth(username, password):
    """Check if username/password combination is valid."""
    return username == AUTH_USERNAME and password == AUTH_PASSWORD

def authenticate():
    """Send 401 response to enable basic auth login."""
    return Response(
        'Access denied. Please provide valid credentials.',
        401,
        {'WWW-Authenticate': 'Basic realm="E0469 Payer Dashboard"'}
    )

@app.before_request
def require_auth_for_all():
    """Require authentication for all requests."""
    if not AUTH_PASSWORD:
        return
    if request.endpoint == 'static':
        return
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

# Database configuration
DB_CONFIG = {
    "dbname": os.environ.get("DB_NAME", "e0469_analysis"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 5432))
}


def get_db_connection():
    """Get database connection with RealDictCursor."""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


# Coverage status = the payer's determination for E0469 (one value per policy).
# Ordered most favorable -> least favorable; colors are the badge backgrounds.
COVERAGE_CATEGORIES = {
    "Covered": "#C6EFCE",                    # Green - includes codes on a PA list / fee schedule
    "Not Medically Necessary": "#FCD5B4",    # Orange
    "Investigational": "#FFEB9C",            # Yellow
    "Not Covered": "#FFC7CE",                # Red - only when the policy explicitly says so
}
COVERAGE_STATUSES = list(COVERAGE_CATEGORIES)

# Prior auth is tracked separately: "Yes" only when a document explicitly requires it.
PRIOR_AUTH_VALUES = ["Yes", "No", "Not Applicable", "Not Stated"]

# Heatmap: a state's single color when it has mixed statuses (most restrictive wins)
STATUS_SEVERITY = ["Not Covered", "Investigational", "Not Medically Necessary",
                   "Covered"]


@app.route('/')
def dashboard():
    """Render main dashboard."""
    return render_template('dashboard.html')


@app.route('/map')
def map_view():
    """Render heatmap view."""
    return render_template('map.html')


@app.route('/api/state-coverage')
def get_state_coverage():
    """Get coverage status by state for heatmap with breakdown by status."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Get all payers grouped by state and coverage status
    cur.execute("""
        SELECT
            p.state,
            pp.coverage_status,
            COUNT(*) as payer_count,
            STRING_AGG(p.name, ', ' ORDER BY p.name) as payers
        FROM payers p
        JOIN payer_policies pp ON p.id = pp.payer_id
        WHERE p.state IS NOT NULL
        GROUP BY p.state, pp.coverage_status
        ORDER BY p.state
    """)

    rows = cur.fetchall()
    conn.close()

    # Aggregate by state with breakdown by status
    state_data = {}
    for row in rows:
        state = row['state']
        status = row['coverage_status']
        count = row['payer_count']
        payers = row['payers']

        if state not in state_data:
            state_data[state] = {
                'state': state,
                'total_payers': 0,
                'statuses': {},
                'payers_by_status': {}
            }

        state_data[state]['total_payers'] += count
        state_data[state]['statuses'][status] = count
        state_data[state]['payers_by_status'][status] = payers

    # Determine display color based on majority or mixed status
    result = []
    for state, data in state_data.items():
        statuses = data['statuses']

        # Primary status for color: most restrictive status present in the state
        primary_status = next((s for s in STATUS_SEVERITY if s in statuses), list(statuses)[0])

        result.append({
            'state': state,
            'coverage_status': primary_status,
            'color': COVERAGE_CATEGORIES.get(primary_status, '#E2E8F0'),
            'total_payers': data['total_payers'],
            'statuses': statuses,
            'payers_by_status': data['payers_by_status']
        })

    return jsonify(result)


@app.route('/api/payers')
def get_payers():
    """Get payers with filtering, sorting, and pagination."""
    # Parse query parameters
    name = request.args.get('name', '').strip()
    payer_type = request.args.get('payer_type', '').strip()
    coverage_status = request.args.get('coverage_status', '').strip()
    prior_auth = request.args.get('prior_auth', '').strip()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    sort_by = request.args.get('sort_by', 'name').strip()
    sort_dir = request.args.get('sort_dir', 'asc').strip().lower()

    # Validate sort parameters
    allowed_sort_fields = ['name', 'payer_type', 'state', 'coverage_status', 'prior_auth_required',
                           'policy_date', 'policy_number']
    if sort_by not in allowed_sort_fields:
        sort_by = 'name'
    if sort_dir not in ['asc', 'desc']:
        sort_dir = 'asc'

    # Build WHERE clause
    where_clauses = []
    params = []

    if name:
        where_clauses.append("p.name ILIKE %s")
        params.append(f"%{name}%")

    if payer_type:
        where_clauses.append("p.payer_type = %s")
        params.append(payer_type)

    if coverage_status:
        where_clauses.append("pp.coverage_status = %s")
        params.append(coverage_status)

    if prior_auth:
        where_clauses.append("pp.prior_auth_required = %s")
        params.append(prior_auth)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    # Calculate offset
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cur = conn.cursor()

    # Get total count
    cur.execute(f"""
        SELECT COUNT(DISTINCT p.id)
        FROM payers p
        LEFT JOIN payer_policies pp ON p.id = pp.payer_id
        WHERE {where_sql}
    """, params)
    total = cur.fetchone()['count']

    # Get payers with policies
    cur.execute(f"""
        SELECT
            p.id,
            p.name,
            p.payer_type,
            p.state,
            pp.coverage_status,
            pp.prior_auth_required,
            pp.policy_wording,
            pp.policy_date,
            pp.policy_number,
            pp.notes,
            pp.source_url
        FROM payers p
        LEFT JOIN payer_policies pp ON p.id = pp.payer_id
        WHERE {where_sql}
        ORDER BY {sort_by} {sort_dir} NULLS LAST
        LIMIT %s OFFSET %s
    """, params + [per_page, offset])

    payers = [dict(row) for row in cur.fetchall()]

    for payer in payers:
        payer['coverage_category'] = payer['coverage_status']
        payer['color_code'] = COVERAGE_CATEGORIES.get(payer['coverage_status'], '#E2E8F0')

    conn.close()

    return jsonify({
        'payers': payers,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page if total > 0 else 1
    })


@app.route('/api/payers/<int:payer_id>')
def get_payer(payer_id):
    """Get single payer details."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.id,
            p.name,
            p.payer_type,
            p.state,
            pp.coverage_status,
            pp.prior_auth_required,
            pp.policy_wording,
            pp.policy_date,
            pp.policy_number,
            pp.notes,
            pp.source_url
        FROM payers p
        LEFT JOIN payer_policies pp ON p.id = pp.payer_id
        WHERE p.id = %s
    """, [payer_id])

    payer = cur.fetchone()
    conn.close()

    if payer:
        payer = dict(payer)
        payer['coverage_category'] = payer['coverage_status']
        payer['color_code'] = COVERAGE_CATEGORIES.get(payer['coverage_status'], '#E2E8F0')
        return jsonify(payer)
    else:
        return jsonify({'error': 'Payer not found'}), 404


@app.route('/api/payers/<int:payer_id>', methods=['PUT'])
def update_payer(payer_id):
    """Update payer policy information."""
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    # Update payer_policies
    update_fields = []
    params = []

    if 'coverage_status' in data:
        update_fields.append("coverage_status = %s")
        params.append(data['coverage_status'])

    if 'prior_auth_required' in data:
        update_fields.append("prior_auth_required = %s")
        params.append(data['prior_auth_required'])

    if 'policy_wording' in data:
        update_fields.append("policy_wording = %s")
        params.append(data['policy_wording'])

    if 'notes' in data:
        update_fields.append("notes = %s")
        params.append(data['notes'])

    if update_fields:
        params.append(payer_id)
        cur.execute(f"""
            UPDATE payer_policies
            SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE payer_id = %s
        """, params)
        conn.commit()

    conn.close()

    return jsonify({'success': True})


@app.route('/api/coverage-statuses')
def get_coverage_statuses():
    """Get the coverage status values (with colors) and prior auth values."""
    return jsonify({
        'statuses': [{'name': s, 'color': COVERAGE_CATEGORIES[s]} for s in COVERAGE_STATUSES],
        'prior_auth': PRIOR_AUTH_VALUES
    })


@app.route('/api/payer-types')
def get_payer_types():
    """Get distinct payer types."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT payer_type
        FROM payers
        WHERE payer_type IS NOT NULL
        ORDER BY payer_type
    """)

    types = [row['payer_type'] for row in cur.fetchall()]
    conn.close()

    return jsonify(types)


@app.route('/api/aggregates')
def get_aggregates():
    """Get summary statistics."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Total payers
    cur.execute("SELECT COUNT(*) as count FROM payers")
    total_payers = cur.fetchone()['count']

    # Total searched (no policy)
    cur.execute("SELECT COUNT(*) as count FROM searched_payers")
    total_searched = cur.fetchone()['count']

    # Coverage status counts
    cur.execute("""
        SELECT coverage_status, COUNT(*) as count
        FROM payer_policies
        GROUP BY coverage_status
        ORDER BY count DESC
    """)
    coverage_counts = [dict(row) for row in cur.fetchall()]

    # Payer type counts
    cur.execute("""
        SELECT payer_type, COUNT(*) as count
        FROM payers
        GROUP BY payer_type
        ORDER BY count DESC
    """)
    type_counts = [dict(row) for row in cur.fetchall()]

    # Coverage status x prior auth (for summary chart, PA chart and matrix)
    cur.execute("""
        SELECT coverage_status, prior_auth_required, COUNT(*) as count
        FROM payer_policies
        GROUP BY coverage_status, prior_auth_required
    """)
    pairs = cur.fetchall()

    conn.close()

    status_totals = {s: 0 for s in COVERAGE_STATUSES}
    pa_totals = {v: 0 for v in PRIOR_AUTH_VALUES}
    matrix = {s: {v: 0 for v in PRIOR_AUTH_VALUES} for s in COVERAGE_STATUSES}
    for row in pairs:
        status, pa, count = row['coverage_status'], row['prior_auth_required'], row['count']
        status_totals[status] = status_totals.get(status, 0) + count
        pa_totals[pa] = pa_totals.get(pa, 0) + count
        matrix.setdefault(status, {}).setdefault(pa, 0)
        matrix[status][pa] += count

    return jsonify({
        'total_payers': total_payers,
        'total_searched': total_searched,
        'coverage_counts': coverage_counts,
        'type_counts': type_counts,
        'summary_counts': [{'category': s, 'count': c, 'color': COVERAGE_CATEGORIES.get(s, '#E2E8F0')}
                           for s, c in status_totals.items()],
        'prior_auth_counts': [{'value': v, 'count': c} for v, c in pa_totals.items()],
        'matrix': [{'status': s, 'color': COVERAGE_CATEGORIES.get(s, '#E2E8F0'), 'cells': cells}
                   for s, cells in matrix.items()],
        'prior_auth_values': PRIOR_AUTH_VALUES
    })


@app.route('/api/searched-payers')
def get_searched_payers():
    """Get payers that were searched but no E0469 policy found."""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    payer_type = request.args.get('payer_type', '').strip()
    sort_by = request.args.get('sort_by', 'name').strip()
    sort_dir = request.args.get('sort_dir', 'asc').strip().lower()

    # Allowlist: only Name and Type sortable
    if sort_by not in ('name', 'payer_type'):
        sort_by = 'name'
    if sort_dir not in ('asc', 'desc'):
        sort_dir = 'asc'

    offset = (page - 1) * per_page

    conn = get_db_connection()
    cur = conn.cursor()

    where_sql = "1=1"
    params = []

    if payer_type:
        where_sql = "payer_type = %s"
        params.append(payer_type)

    # Get total
    cur.execute(f"SELECT COUNT(*) as count FROM searched_payers WHERE {where_sql}", params)
    total = cur.fetchone()['count']

    # Get payers
    cur.execute(f"""
        SELECT id, name, payer_type, notes, date_searched
        FROM searched_payers
        WHERE {where_sql}
        ORDER BY {sort_by} {sort_dir} NULLS LAST, name ASC
        LIMIT %s OFFSET %s
    """, params + [per_page, offset])

    payers = [dict(row) for row in cur.fetchall()]
    conn.close()

    return jsonify({
        'payers': payers,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page if total > 0 else 1
    })


@app.route('/api/export')
def export_excel():
    """Export payer data to Excel."""
    # Get filter parameters
    name = request.args.get('name', '').strip()
    payer_type = request.args.get('payer_type', '').strip()
    coverage_status = request.args.get('coverage_status', '').strip()
    prior_auth = request.args.get('prior_auth', '').strip()

    conn = get_db_connection()
    cur = conn.cursor()

    # Build WHERE clause
    where_clauses = []
    params = []

    if name:
        where_clauses.append("p.name ILIKE %s")
        params.append(f"%{name}%")

    if payer_type:
        where_clauses.append("p.payer_type = %s")
        params.append(payer_type)

    if coverage_status:
        where_clauses.append("pp.coverage_status = %s")
        params.append(coverage_status)

    if prior_auth:
        where_clauses.append("pp.prior_auth_required = %s")
        params.append(prior_auth)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    # Get payers with policies
    cur.execute(f"""
        SELECT
            p.name,
            p.payer_type,
            p.state,
            pp.coverage_status,
            pp.prior_auth_required,
            pp.policy_wording,
            pp.policy_date,
            pp.policy_number,
            pp.notes,
            pp.source_url
        FROM payers p
        LEFT JOIN payer_policies pp ON p.id = pp.payer_id
        WHERE {where_sql}
        ORDER BY p.name
    """, params)

    payers = cur.fetchall()

    # Get searched payers
    cur.execute("""
        SELECT name, payer_type, notes, date_searched
        FROM searched_payers
        ORDER BY name
    """)
    searched = cur.fetchall()

    conn.close()

    # Create workbook
    wb = Workbook()

    # Styles
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    # Sheet 1: Payers with E0469 Policies
    ws1 = wb.active
    ws1.title = "E0469 Payer Policies"

    headers1 = ["Payer Name", "Payer Type", "State", "Coverage Status", "Prior Auth",
                "Policy Wording", "Policy Date", "Policy Number", "Notes", "Source URL"]

    for col, header in enumerate(headers1, 1):
        cell = ws1.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
        cell.border = thin_border

    for row_num, payer in enumerate(payers, 2):
        ws1.cell(row=row_num, column=1, value=payer['name'])
        ws1.cell(row=row_num, column=2, value=payer['payer_type'])
        ws1.cell(row=row_num, column=3, value=payer['state'])

        coverage_cell = ws1.cell(row=row_num, column=4, value=payer['coverage_status'])
        color = COVERAGE_CATEGORIES.get(payer['coverage_status'], '#E2E8F0').replace('#', '')
        coverage_cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        ws1.cell(row=row_num, column=5, value=payer['prior_auth_required'])
        ws1.cell(row=row_num, column=6, value=payer['policy_wording'])
        ws1.cell(row=row_num, column=7, value=payer['policy_date'])
        ws1.cell(row=row_num, column=8, value=payer['policy_number'])
        ws1.cell(row=row_num, column=9, value=payer['notes'])
        ws1.cell(row=row_num, column=10, value=payer['source_url'])

        for col in range(1, 11):
            ws1.cell(row=row_num, column=col).border = thin_border
            ws1.cell(row=row_num, column=col).alignment = Alignment(vertical='top', wrap_text=True)

    # Set column widths
    widths1 = [35, 18, 8, 26, 16, 70, 18, 25, 60, 50]
    for col, width in enumerate(widths1, 1):
        ws1.column_dimensions[get_column_letter(col)].width = width

    ws1.freeze_panes = "A2"

    # Sheet 2: Searched Payers (No E0469)
    ws2 = wb.create_sheet("Searched - No E0469")

    headers2 = ["Payer Name", "Payer Type", "Notes", "Date Searched"]

    for col, header in enumerate(headers2, 1):
        cell = ws2.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
        cell.border = thin_border

    for row_num, payer in enumerate(searched, 2):
        ws2.cell(row=row_num, column=1, value=payer['name'])
        ws2.cell(row=row_num, column=2, value=payer['payer_type'])
        ws2.cell(row=row_num, column=3, value=payer['notes'])
        ws2.cell(row=row_num, column=4, value=str(payer['date_searched']) if payer['date_searched'] else '')

        for col in range(1, 5):
            ws2.cell(row=row_num, column=col).border = thin_border
            ws2.cell(row=row_num, column=col).alignment = Alignment(vertical='top', wrap_text=True)

    widths2 = [40, 25, 60, 15]
    for col, width in enumerate(widths2, 1):
        ws2.column_dimensions[get_column_letter(col)].width = width

    ws2.freeze_panes = "A2"

    # Sheet 3: Summary
    ws3 = wb.create_sheet("Summary")
    ws3.cell(row=1, column=1, value="E0469 Payer Coverage Analysis Summary")
    ws3.cell(row=1, column=1).font = Font(bold=True, size=14)

    summary_data = [
        ("", ""),
        ("HCPCS Code:", "E0469"),
        ("Description:", "Lung expansion airway clearance, continuous high frequency oscillation, and nebulization device"),
        ("Effective Date:", "October 1, 2024"),
        ("", ""),
        ("Total Payers with Explicit E0469 Policies:", str(len(payers))),
        ("Searched Payers (No E0469 Found):", str(len(searched))),
        ("", ""),
        ("Report Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    ]

    for row_num, (label, value) in enumerate(summary_data, 3):
        ws3.cell(row=row_num, column=1, value=label)
        if label.endswith(":"):
            ws3.cell(row=row_num, column=1).font = Font(bold=True)
        ws3.cell(row=row_num, column=2, value=value)

    ws3.column_dimensions['A'].width = 45
    ws3.column_dimensions['B'].width = 80

    # Save to BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"E0469_Payer_Coverage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    return Response(
        output.getvalue(),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


@app.route('/api/payers', methods=['POST'])
def add_payer():
    """Add a new payer with policy."""
    data = request.get_json()

    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Payer name is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Check if payer already exists
        cur.execute("SELECT id FROM payers WHERE name = %s", [name])
        existing = cur.fetchone()
        if existing:
            return jsonify({'error': f'Payer "{name}" already exists'}), 400

        # Insert payer
        state = data.get('state', '').strip().upper() or None
        cur.execute("""
            INSERT INTO payers (name, payer_type, state)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (name, data.get('payer_type', ''), state))
        payer_id = cur.fetchone()['id']

        # Insert policy if coverage status provided
        if data.get('coverage_status') or data.get('source_url') or data.get('notes'):
            cur.execute("""
                INSERT INTO payer_policies (
                    payer_id, coverage_status, prior_auth_required,
                    policy_wording, policy_date, policy_number,
                    notes, source_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                payer_id,
                data.get('coverage_status', ''),
                data.get('prior_auth_required', ''),
                data.get('policy_wording', ''),
                data.get('policy_date', ''),
                data.get('policy_number', ''),
                data.get('notes', ''),
                data.get('source_url', '')
            ))

        conn.commit()
        return jsonify({'success': True, 'id': payer_id})

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/web-search', methods=['POST'])
def web_search():
    """Search the web for E0469 payer policies."""
    data = request.get_json()
    query = data.get('query', '').strip()

    if not query:
        return jsonify({'error': 'Search query is required'}), 400

    # Build search query for E0469 policies
    search_query = f'"{query}" "E0469" policy site:.gov OR site:.com OR site:.org filetype:pdf OR medical policy'

    try:
        # Use DuckDuckGo HTML search (no API key required)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        # Search DuckDuckGo
        search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(search_query)}"
        response = requests.get(search_url, headers=headers, timeout=10)

        results = []

        if response.status_code == 200:
            # Parse results from HTML
            # Extract URLs and titles from DuckDuckGo results
            html = response.text

            # Find result links - DuckDuckGo uses class="result__a"
            pattern = r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
            matches = re.findall(pattern, html, re.IGNORECASE)

            for url, title in matches[:10]:  # Limit to 10 results
                # Clean up URL (DuckDuckGo wraps URLs)
                if 'uddg=' in url:
                    url_match = re.search(r'uddg=([^&]+)', url)
                    if url_match:
                        url = requests.utils.unquote(url_match.group(1))

                # Filter for likely policy documents
                if any(x in url.lower() for x in ['policy', 'medical', 'coverage', '.pdf', 'provider']):
                    results.append({
                        'title': title.strip(),
                        'url': url
                    })

        # Also search Google (backup)
        if len(results) < 5:
            google_url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}"
            try:
                g_response = requests.get(google_url, headers=headers, timeout=10)
                if g_response.status_code == 200:
                    # Extract URLs from Google results
                    g_pattern = r'<a[^>]*href="/url\?q=([^"&]+)[^"]*"'
                    g_matches = re.findall(g_pattern, g_response.text)
                    for url in g_matches[:5]:
                        url = requests.utils.unquote(url)
                        if not any(x in url for x in ['google.com', 'youtube.com', 'facebook.com']):
                            if url not in [r['url'] for r in results]:
                                results.append({
                                    'title': url.split('/')[-1][:50] or 'Policy Document',
                                    'url': url
                                })
            except:
                pass  # Google search is optional fallback

        return jsonify({
            'query': query,
            'results': results[:10]
        })

    except requests.Timeout:
        return jsonify({'error': 'Search timed out. Please try again.'}), 504
    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 500


if __name__ == '__main__':
    print("Starting E0469 Payer Coverage Dashboard...")
    print(f"Database: {DB_CONFIG['dbname']} on {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print("Dashboard URL: http://localhost:5002")
    app.run(host='0.0.0.0', port=5002, debug=True)
