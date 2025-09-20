CREATE TABLE IF NOT EXISTS
  `<project-id>.semantic_ads_targeting.user_events` (
    `event_id` STRING,
    `user_id` STRING,
    `product_id` STRING,
    `category_id` INT64,
    `event_type` STRING,
    `event_timestamp` TIMESTAMP,
    `primary_segment` STRING,
    `secondary_segments` STRING
  );