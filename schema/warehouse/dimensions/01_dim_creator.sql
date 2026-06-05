/*-- =============================================
-- DIMENSION: Creator
-- Source: Stg_tiktok_creator
-- SCD Type: 2 (Track name changes, verification status)
-- =============================================*/

USE trendtiktok_warehouse;

CREATE TABLE IF NOT EXISTS dim_creator (
    -- Surrogate key (internal use only)
    creator_sk INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Surrogate key - internal ID',
    
    -- Business key (from TikTok)
    creator_id VARCHAR(50) NOT NULL COMMENT 'TikTok unique creator ID',
    
    -- Slowly changing attributes
    username VARCHAR(70) NOT NULL COMMENT 'Current username',
    display_name VARCHAR(60) COMMENT 'Display name on profile',
    bio TEXT COMMENT 'Creator biography',
    is_verified BOOLEAN DEFAULT FALSE COMMENT 'Blue checkmark status',
    
    -- SCD Type 2 tracking fields
    is_current BOOLEAN DEFAULT TRUE COMMENT 'Is this the current version?',
    valid_from DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When this version became active',
    valid_to DATETIME DEFAULT '9999-12-31 23:59:59' COMMENT 'When this version ended',
    
    -- Metadata
    first_seen DATE COMMENT 'When first discovered',
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_creator_id (creator_id),
    INDEX idx_username (username),
    INDEX idx_current (is_current),
    INDEX idx_verified (is_verified),
    
    -- Business constraint: Only ONE current version per creator
    UNIQUE KEY uk_current_creator (creator_id, is_current)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Creator dimension - tracks historical changes';
