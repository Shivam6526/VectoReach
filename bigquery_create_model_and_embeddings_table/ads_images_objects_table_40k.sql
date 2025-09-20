CREATE OR REPLACE EXTERNAL TABLE
  `<project-id>.semantic_ads_targeting.ads_images_objects_table_40k`
WITH CONNECTION `<region>.<conn-id>` OPTIONS ( object_metadata = 'SIMPLE',
    uris = ['gs://<gcs bucket having 40k images>/*'] );