CREATE OR REPLACE TABLE `<project-id>.semantic_ads_targeting.target_ads_multimodal_embeddings_40k` AS
WITH img_embeddings_with_id AS (
  SELECT
    g.ad_id,
    i.ml_generate_embedding_result as img_embedding
  FROM `<project-id>.semantic_ads_targeting.ads_image_embeddings_multimodal_40k` i
  JOIN `<project-id>.semantic_ads_targeting.target_ads_gcs` g
    ON i.product_id = g.product_id
)
SELECT
  t.ad_id,
  t.content as ad_text,
  t.ml_generate_embedding_result as text_embedding,
  ie.img_embedding,
  ARRAY(
    SELECT (te + ie) / 2
    FROM UNNEST(t.ml_generate_embedding_result) te WITH OFFSET pos1
    JOIN UNNEST(ie.img_embedding) ie WITH OFFSET pos2
      ON pos1 = pos2
  ) AS multimodal_embedding
FROM `<project-id>.semantic_ads_targeting.target_ads_embeddings` t
JOIN img_embeddings_with_id ie
  ON t.ad_id = ie.ad_id;