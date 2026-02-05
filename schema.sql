-- E0469 Payer Coverage Analysis Database Schema
-- PostgreSQL 16

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS payer_policies CASCADE;
DROP TABLE IF EXISTS searched_payers CASCADE;
DROP TABLE IF EXISTS coverage_categories CASCADE;
DROP TABLE IF EXISTS payers CASCADE;

-- Coverage categories reference table
CREATE TABLE coverage_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    color_code VARCHAR(20),
    description TEXT,
    sort_order INTEGER
);

-- Insert coverage categories with color codes
INSERT INTO coverage_categories (name, color_code, description, sort_order) VALUES
    ('NOT COVERED', '#FFC7CE', 'Categorical exclusion from benefits', 1),
    ('NOT COVERED - Experimental/Investigational', '#FFC7CE', 'Explicit exclusion as experimental', 2),
    ('NOT COVERED - EIU Non-Reimbursable', '#FFC7CE', 'EIU list - non-reimbursable', 3),
    ('Investigational', '#FFEB9C', 'Insufficient evidence for coverage', 4),
    ('Investigational - Experimental', '#FFEB9C', 'Considered experimental/investigational', 5),
    ('Partial - OLE Unproven', '#FFEB9C', 'OLE devices unproven, HFCWO may be covered', 6),
    ('Partial - Limited Conditions', '#FFEB9C', 'Coverage limited to specific conditions', 7),
    ('Partial - Some Investigational', '#FFEB9C', 'Some uses considered investigational', 8),
    ('Case-by-Case (No LCD)', '#BDD7EE', 'No LCD - claims reviewed individually', 9),
    ('Case Review - Prior Auth Needed', '#BDD7EE', 'Requires prior auth review', 10),
    ('Prior Auth Required', '#BDD7EE', 'Prior authorization required', 11),
    ('Prior Auth Required (MA)', '#BDD7EE', 'Medicare Advantage prior auth required', 12),
    ('Covered with Criteria', '#C6EFCE', 'Covered when criteria met', 13),
    ('Covered with Prior Auth', '#C6EFCE', 'Covered with prior authorization', 14),
    ('Covered with Limits', '#C6EFCE', 'Covered with frequency/quantity limits', 15),
    ('Covered - Fee Schedule', '#C6EFCE', 'Listed in fee schedule', 16),
    ('Covered - Per Fee Schedule', '#C6EFCE', 'Coverage per fee schedule', 17),
    ('Covered - Rental Only', '#C6EFCE', 'Rental only, no purchase', 18),
    ('Varies - EIU or Clinical Review', '#BDD7EE', 'Plan-dependent coverage', 19),
    ('Reference Only', '#E2E8F0', 'Manufacturer/reference document', 20);

-- Payers master table
CREATE TABLE payers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    payer_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on payer name for faster searches
CREATE INDEX idx_payers_name ON payers(name);
CREATE INDEX idx_payers_type ON payers(payer_type);

-- Payer policies table (coverage details)
CREATE TABLE payer_policies (
    id SERIAL PRIMARY KEY,
    payer_id INTEGER NOT NULL REFERENCES payers(id) ON DELETE CASCADE,
    coverage_status VARCHAR(100),
    prior_auth_required VARCHAR(100),
    investigational VARCHAR(100),
    not_med_necessary VARCHAR(100),
    policy_date VARCHAR(50),
    policy_number VARCHAR(255),
    notes TEXT,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for common queries
CREATE INDEX idx_payer_policies_payer_id ON payer_policies(payer_id);
CREATE INDEX idx_payer_policies_coverage ON payer_policies(coverage_status);

-- Searched payers (no explicit E0469 policy found)
CREATE TABLE searched_payers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    payer_type VARCHAR(100),
    notes TEXT,
    date_searched DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT searched_payer_unique UNIQUE(name)
);

CREATE INDEX idx_searched_payers_type ON searched_payers(payer_type);

-- Function to update timestamp on row update
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to auto-update updated_at
CREATE TRIGGER update_payers_updated_at
    BEFORE UPDATE ON payers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_payer_policies_updated_at
    BEFORE UPDATE ON payer_policies
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- View for payer with latest policy info
CREATE VIEW payer_coverage_view AS
SELECT
    p.id,
    p.name,
    p.payer_type,
    pp.coverage_status,
    pp.prior_auth_required,
    pp.investigational,
    pp.not_med_necessary,
    pp.policy_date,
    pp.policy_number,
    pp.notes,
    pp.source_url,
    cc.color_code
FROM payers p
LEFT JOIN payer_policies pp ON p.id = pp.payer_id
LEFT JOIN coverage_categories cc ON pp.coverage_status = cc.name
ORDER BY p.name;

-- Summary stats view
CREATE VIEW coverage_summary AS
SELECT
    coverage_status,
    COUNT(*) as count
FROM payer_policies
GROUP BY coverage_status
ORDER BY count DESC;

-- Payer type summary view
CREATE VIEW payer_type_summary AS
SELECT
    payer_type,
    COUNT(*) as count
FROM payers
GROUP BY payer_type
ORDER BY count DESC;
