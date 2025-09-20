CREATE OR REPLACE TABLE `<project-id>.semantic_ads_targeting.target_ads_embeddings` AS
SELECT
  *
FROM ML.GENERATE_EMBEDDING(
  MODEL `<project-id>.semantic_ads_targeting.text_embedding_model_4`,
  (
    SELECT
      ad_id,
      ad_text AS content
    FROM `<project-id>.semantic_ads_targeting.target_ads`
  ),
  STRUCT(TRUE AS flatten_json_output)
);