-- 1. First create ALL dimension tables (6 tables)
-- 2. Then create FACT tables (3 tables)
-- 3. Each fact table will have foreign keys to relevant dimensions

-- For your EAC project, start with ONE fact table:
USE trendtiktok_warehouse;
CREATE TABLE fact_video_performance (
    fact_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    creator_sk INT NOT NULL,
    video_sk INT NOT NULL,
    audio_sk INT NOT NULL,
    country_sk INT NOT NULL,
    category_sk INT NOT NULL,
    time_sk INT NOT NULL,
    views_count BIGINT DEFAULT 0,
    likes_count BIGINT DEFAULT 0,
    shares_count BIGINT DEFAULT 0,
    
    FOREIGN KEY (creator_sk) REFERENCES dim_creator(creator_sk),
    FOREIGN KEY (video_sk) REFERENCES dim_video(video_sk),
    FOREIGN KEY (audio_sk) REFERENCES dim_audio(audio_sk),
    FOREIGN KEY (country_sk) REFERENCES dim_country(country_sk),
    FOREIGN KEY (category_sk) REFERENCES dim_category(category_sk),
    FOREIGN KEY (time_sk) REFERENCES dim_time(time_sk)
);
