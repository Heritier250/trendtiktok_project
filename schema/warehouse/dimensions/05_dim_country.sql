/*-- =============================================
-- DIMENSION: Country - East Africa Community
-- Scope: 7 EAC member states
-- Future: Can expand to other regions
-- =============================================*/

USE trendtiktok_warehouse;

CREATE TABLE IF NOT EXISTS dim_country (
    country_sk INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Surrogate key',
    country_code VARCHAR(2) NOT NULL UNIQUE COMMENT 'ISO 2-letter code',
    country_name VARCHAR(50) NOT NULL COMMENT 'Full country name',
    region VARCHAR(50) DEFAULT 'East Africa' COMMENT 'Region',
    eac_member_since YEAR COMMENT 'Year joined EAC',
    is_active BOOLEAN DEFAULT TRUE COMMENT 'Still tracking?',
    
    INDEX idx_country_code (country_code),
    INDEX idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert EAC countries
INSERT INTO dim_country (country_code, country_name, eac_member_since) VALUES
('KE', 'Kenya', 2000),
('TZ', 'Tanzania', 2000),
('UG', 'Uganda', 2000),
('RW', 'Rwanda', 2007),
('BI', 'Burundi', 2007),
('SS', 'South Sudan', 2016),
('CD', 'Congo DR', 2022);

-- Just verify inserted country....
SELECT * FROM dim_country;
