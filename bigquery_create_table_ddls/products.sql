CREATE TABLE IF NOT EXISTS
  `<project-id>.semantic_ads_targeting.products` (
    `asin` STRING,
    `title` STRING,
    `imgUrl` STRING,
    `productURL` STRING,
    `stars` FLOAT64,
    `reviews` INT64,
    `price` FLOAT64,
    `listPrice` FLOAT64,
    `category_id` INT64,
    `isBestSeller` BOOL,
    `boughtInLastMonth` INT64
  );