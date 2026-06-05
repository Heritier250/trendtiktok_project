/*-- =============================================
-- DIMENSION: Audio/Sound
-- Source: Stg_tiktok_audio
-- SCD Type: 1 (Audio metadata rarely changes)
-- =============================================*/
USE trendtiktok_warehouse;

CREATE TABLE IF NOT EXISTS dim_audio (
    -- Surrogate key
    audio_sk INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Surrogate key - internal ID',
    
    -- Business key
    audio_id VARCHAR(50) NOT NULL UNIQUE COMMENT 'TikTok unique audio ID',
    
    -- Fixed attributes
    audio_name VARCHAR(50) NOT NULL COMMENT 'Audio track name',
    artist_name VARCHAR(60) COMMENT 'Artist/singer name',
    duration_seconds INT DEFAULT 0 COMMENT 'Audio length',
    audio_url VARCHAR(800) COMMENT 'URL to audio file',
    
    -- Original creator
    original_creator_username VARCHAR(60) COMMENT 'Who first used this sound',
    
    -- Time attribute
    audio_published_date DATE COMMENT 'When audio was published',
    
    -- Metadata
    first_detected DATE COMMENT 'When we first saw this audio',
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_audio_id (audio_id),
    INDEX idx_audio_name (audio_name),
    INDEX idx_artist (artist_name),
    INDEX idx_published_date (audio_published_date),
    
    FULLTEXT INDEX ft_audio_search (audio_name, artist_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Audio dimension - fixed metadata';
