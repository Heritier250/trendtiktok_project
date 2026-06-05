/*-- =============================================
-- DIMENSION: Time/Date
-- Source: Generated (not from staging)
-- SCD Type: Static (never changes)
-- =============================================*/

USE trendtiktok_warehouse;

CREATE TABLE IF NOT EXISTS dim_time (
    -- Surrogate key (integer format: YYYYMMDD)
    time_sk INT PRIMARY KEY COMMENT 'Surrogate key - YYYYMMDD format',
    
    -- Date components
    full_date DATE NOT NULL UNIQUE COMMENT 'Actual date',
    year INT NOT NULL COMMENT 'Year (YYYY)',
    quarter INT NOT NULL COMMENT 'Quarter (1-4)',
    month INT NOT NULL COMMENT 'Month (1-12)',
    month_name VARCHAR(20) NOT NULL COMMENT 'January, February, etc.',
    day_of_month INT NOT NULL COMMENT 'Day of month (1-31)',
    day_of_year INT NOT NULL COMMENT 'Day of year (1-366)',
    day_of_week INT NOT NULL COMMENT '1=Monday, 7=Sunday',
    day_name VARCHAR(10) NOT NULL COMMENT 'Monday, Tuesday, etc.',
    week_of_year INT NOT NULL COMMENT 'Week number (1-52)',
    
    -- Business calendar
    is_weekend BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Saturday or Sunday?',
    is_holiday BOOLEAN DEFAULT FALSE COMMENT 'National holiday?',
    holiday_name VARCHAR(100) COMMENT 'Name of holiday if applicable',
    
    -- TikTok specific
    is_trending_day BOOLEAN DEFAULT FALSE COMMENT 'Unusually high activity day',
    
    -- Indexes
    INDEX idx_year (year),
    INDEX idx_year_month (year, month),
    INDEX idx_week (year, week_of_year),
    INDEX idx_month_day (month, day_of_month),
    INDEX idx_is_weekend (is_weekend)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
COMMENT='Time dimension - pre-populated static calendar';
