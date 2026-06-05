                                                   
/*-- =============================================
-- DIMENSION: Video
-- Source: Stg_tiktok_video
-- SCD Type: 1 (Videos don't change after posting)
-- =============================================*/
USE trendtiktok_warehouse;

CREATE TABLE IF NOT EXISTS dim_video (
    -- Surrogate key
    video_sk INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Surrogate key - internal ID',
    
    -- Business key
    video_id VARCHAR(40) NOT NULL UNIQUE COMMENT 'TikTok unique video ID',
    
    -- Fixed attributes (never change)
    video_url VARCHAR(800) NOT NULL COMMENT 'URL to video',
    video_description TEXT COMMENT 'Video caption/description',
    hashtags TEXT COMMENT 'All hashtags used',
    duration_seconds INT DEFAULT 0 COMMENT 'Video length',
    
    -- Time attributes
    posted_at DATETIME COMMENT 'When video was posted',
    posted_date DATE COMMENT 'Posted date (denormalized for performance)',
    
    -- Derived attribute (extracted from hashtags)
    primary_hashtag VARCHAR(100) 
        GENERATED ALWAYS AS (SUBSTRING_INDEX(hashtags, ',', 1)) STORED 
        COMMENT 'First hashtag in list',
    
    -- Metadata
    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_video_id (video_id),
    INDEX idx_posted_date (posted_date),
    INDEX idx_primary_hashtag (primary_hashtag),
    INDEX idx_duration (duration_seconds),
    
    FULLTEXT INDEX ft_description (video_description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Video dimension - fixed attributes only';







