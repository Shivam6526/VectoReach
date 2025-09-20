CREATE OR REPLACE VECTOR INDEX `<project-id>.semantic_ads_targeting.target_ads_embeddings_index`
ON `<project-id>.semantic_ads_targeting.target_ads_embeddings` (ml_generate_embedding_result)
OPTIONS(
  distance_type = 'COSINE',
  index_type = 'IVF'
);