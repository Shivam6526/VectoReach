CREATE TABLE IF NOT EXISTS
  `<project-id>.semantic_ads_targeting.users` (
    `user_id` STRING,
    `primary_category_id` STRING,
    `primary_segment` STRING,
    `secondary_category_ids` STRING,
    `secondary_segments` STRING,
    `age_group` STRING,
    `gender` STRING,
    `country` STRING,
    `preferred_device` STRING
  );