CREATE OR REPLACE TABLE
  `<project-id>.semantic_ads_targeting.user_profiles_with_embeddings_primary` AS
WITH
  user_interest_text AS (
    SELECT
      ue.user_id,
      STRING_AGG(DISTINCT c.category_name, ' ') AS interest_text
    FROM
      `<project-id>.semantic_ads_targeting.user_events` ue
    JOIN
      `<project-id>.semantic_ads_targeting.products` p
    ON
      ue.product_id = p.asin
    JOIN
      `<project-id>.semantic_ads_targeting.categories` c
    ON
      p.category_id = c.id
    GROUP BY
      ue.user_id
  ),
  user_with_fallback AS (
    SELECT
      u.user_id,
      COALESCE(uit.interest_text, u.primary_segment) AS interest_text
    FROM
      `<project-id>.semantic_ads_targeting.users` u
    LEFT JOIN
      user_interest_text uit
    ON
      u.user_id = uit.user_id
  )
SELECT
  *
FROM
  ML.GENERATE_EMBEDDING(
    MODEL `<project-id>.semantic_ads_targeting.text_embedding_model_4`,
    (
      SELECT
        user_id,
        interest_text AS content
      FROM
        user_with_fallback
    ),
    STRUCT(TRUE AS flatten_json_output)
  );