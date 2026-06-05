-- =============================================
-- Add Comments to Staging Table (Safe Version)
-- =============================================

USE Stg_Trend_tiktok_db;

-- Table level comment
ALTER TABLE stg_tiktok_trends 
COMMENT = 'Staging table for raw TikTok trending data collected from scraping/API. Near real-time raw data.';

-- Column level comments (Safer - only adds comment)
ALTER TABLE stg_tiktok_trends 
    MODIFY trend_name VARCHAR(255) NOT NULL COMMENT 'Name of the trending challenge, sound or topic on TikTok',
    MODIFY hashtag VARCHAR(100) COMMENT 'Primary hashtag of the trend (e.g. #fyp, #viral)',
    MODIFY video_count INT DEFAULT 0 COMMENT 'Total number of videos using this trend',
    MODIFY avg_views BIGINT DEFAULT 0 COMMENT 'Average views per video in this trend',
    MODIFY avg_likes BIGINT DEFAULT 0 COMMENT 'Average likes received',
    MODIFY avg_comments BIGINT DEFAULT 0 COMMENT 'Average number of comments',
    MODIFY avg_shares BIGINT DEFAULT 0 COMMENT 'Average number of shares',
    MODIFY country VARCHAR(100) COMMENT 'Country/region where trend is popular',
    MODIFY category VARCHAR(100) COMMENT 'Content category (Dance, Comedy, Fashion, Food, etc.)',
    MODIFY trend_date DATE NOT NULL COMMENT 'Date the trend data was captured',
    MODIFY crawl_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When this record was inserted into the database';
