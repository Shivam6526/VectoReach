CREATE TABLE IF NOT EXISTS
  `<project-id>.semantic_ads_targeting.target_ads` (
    `ad_id` STRING,
    `product_id` STRING,
    `ad_title` STRING,
    `ad_text` STRING,
    `ad_image_url` STRING,
    `target_keywords` STRING,
    `category_id` INT64,
    `category_name` STRING,
    `used_fallback_image` BOOL
  );