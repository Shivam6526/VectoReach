CREATE OR REPLACE TABLE
  `<project-id>.semantic_ads_targeting.ads_image_embeddings_multimodal_40k` AS
SELECT
  *
FROM
  ML.GENERATE_EMBEDDING( MODEL `<project-id>.semantic_ads_targeting.multimodal_embedding_1`,
    (
    SELECT
      *
    FROM
      `<project-id>.semantic_ads_targeting.ads_images_objects_table_40k`
    WHERE
      content_type = 'image/jpeg'),
    STRUCT(TRUE AS flatten_json_output)
);