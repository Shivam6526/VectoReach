CREATE OR REPLACE MODEL `<project-id>.semantic_ads_targeting.text_embedding_model_4`
REMOTE WITH CONNECTION `projects/<project-id>/locations/us/connections/<conn-id>`
OPTIONS (
  ENDPOINT = 'text-embedding-004'
);
