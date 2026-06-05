-- =============================================
-- Trendtiktok Project - Staging Layer
-- Table: stg_tiktok_trends
-- =============================================

USE Stg_Trend_tiktok_db;

CREATE TABLE IF NOT EXISTS stg_tiktok_trends (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    trend_name VARCHAR(255) NOT NULL,
    hashtag VARCHAR(100),
    video_count INT DEFAULT 0,
    avg_views BIGINT DEFAULT 0,
    avg_likes BIGINT DEFAULT 0,
    avg_comments BIGINT DEFAULT 0,
    avg_shares BIGINT DEFAULT 0,
    country VARCHAR(100),
    category VARCHAR(100),
    trend_date DATE NOT NULL,
    crawl_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_trend_date (trend_date),
    INDEX idx_hashtag (hashtag),
    INDEX idx_country (country)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci;
/*===============================================================================================
Still caring about staging tables this a table that will  be accommodaiting the  vidoes realated 
Table name is Stg_tiktok_videos
=================================================================================================*/
CREATE TABLE IF NOT EXISTS Stg_tiktok_video(
  video_id VARCHAR(40) PRIMARY KEY NOT NULL COMMENT 'Real video id ',
  creator_username Varchar(60) NOT NULL COMMENT 'content creator user name',
  creator_id VARCHAR(50) NOT NULL COMMENT 'content creator id ',
  audio_id VARCHAR(50) NOT NULL COMMENT 'audio original id',
  video_discrpation TEXT,
  hashtags TEXT,
  video_url VARCHAR(800) NOT NULL ,
  duration_second INT DEFAULT 0,
  views_count BIGINT DEFAULT 0 COMMENT 'The number of views does video have',
  likes_count BIGINT DEFAULT 0 COMMENT 'the number of likes does video have',
  comment_count BIGINT DEFAULT 0 COMMENT 'The number of comments each video have',
  shares_count BIGINT DEFAULT 0 COMMENT 'How many people has so far shared certain video',
  saves_count BIGINT DEFAULT 0 COMMENT 'How many people has so far saved my videos',
  posted_date DATE,
  posted_datetime DATETIME,
  crawl_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_creator (creator_username),
  INDEX idx_posted_date (posted_date),
  INDEX idx_audio (audio_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*===================================================================
The next tables  will be accomodaiying only audios 
Table name Stg_tiktok_audio
==================================================================*/

CREATE TABLE IF NOT EXISTS Stg_tiktok_audio(
    audio_id VARCHAR(50) PRIMARY KEY NOT NULL COMMENT 'Unique key to differencaite audio',
    audio_name VARCHAR(50) NOT NULL COMMENT 'Audios name',
    artist_name VARCHAR(60) COMMENT 'the singer of audio',
    duration_second INT DEFAULT 0,
    audio_url VARCHAR(800),
    tatal_user  BIGINT DEFAULT 0,
    total_video BIGINT DEFAULT 0,
    original_creator_username VARCHAR(60),
    audio_published_date  DATE,
    crawl_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP ,
    INDEX idx_audio (audio_name),
    INDEX idx_org_cre_username(original_creator_username)
)ENGINE=InnoDB DEFAULT CHARSET =utf8mb4 COLLATE =utf8mb4_unicode_ci;
/*========================================================================================
The next tables is staging table that will be accomadating Content creators
the tabble name is Stg_tiktok_creator
==========================================================================================*/
CREATE TABLE IF NOT EXISTS Stg_tiktok_creator (
  creator_id VARCHAR(50) PRIMARY KEY NOT NULL COMMENT 'Content creator id',
  username VARCHAR(70) NOT NULL UNIQUE COMMENT 'The contant creators name',
  display_name VARCHAR(60) comment 'the exact person showing the content',
  bio TEXT,
  avatar_url VARCHAR(400),
  follower_count BIGINT  DEFAULT 0 COMMENT 'the number of people that follow your contents',
  following_count BIGINT DEFAULT 0 COMMENT 'the number of other content creator you really folow',
  video_count BIGINT DEFAULT 0 COMMENT 'the number of videos you have posted so far',
  like_count BIGINT DEFAULT 0 COMMENT 'the number of likes you have so far',
  is_varified BOOLEAN DEFAULT False,
  is_private BOOLEAN DEFAULT False,
  account_created_date DATE COMMENT 'the exact moment when the account was or is created',
  crawl_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_username (username),
  INDEX idx_followers (follower_count)
) ENGINE=InnoDB DEFAULT CHARSET =utf8mb4 COLLATE = utf8mb4_unicode_ci; 





