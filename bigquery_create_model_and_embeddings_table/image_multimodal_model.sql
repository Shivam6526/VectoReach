CREATE OR REPLACE MODEL `<project-id>.semantic_ads_targeting.multimodal_embedding_1`
REMOTE WITH CONNECTION `projects/<project-id>/locations/us/connections/<conn-id>`
OPTIONS (
  ENDPOINT = 'multimodalembedding@001'
);