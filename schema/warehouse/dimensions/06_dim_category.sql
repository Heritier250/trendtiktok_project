-- Pre-define categories (like EAC countries)
USE trendtiktok_warehouse;
CREATE TABLE dim_category (
    category_sk INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    category_group VARCHAR(50),  -- Entertainment, Education, etc.
    is_trending BOOLEAN DEFAULT TRUE
);

-- Insert known TikTok categories
INSERT INTO dim_category (category_name, category_group) VALUES
('Dance', 'Entertainment'),
('Comedy', 'Entertainment'),
('Music', 'Entertainment'),
('Education', 'Learning'),
('Beauty', 'Lifestyle'),
('Sports', 'Sports'),
('Food', 'Lifestyle'),
('Pets', 'Animals'),
('Travel', 'Lifestyle'),
('Technology', 'Education'),
('Fashion', 'Lifestyle'),
('Fitness', 'Health'),
('Gaming', 'Entertainment');
