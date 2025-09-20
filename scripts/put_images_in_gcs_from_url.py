# Migrates ad images from their original URLs into a Google Cloud Storage (GCS) bucket.
# It fetches ad metadata from BigQuery, downloads each ad_image_url, and uploads the image as <product_id>.jpg into GCS.
# Using ProcessPoolExecutor with multiple workers,
# it parallelizes downloads/uploads for speed and tracks progress with tqdm.
# Finally, it saves a CSV mapping ads to their new gcs_image_uri for later use in BigQuery.

import pandas as pd
import requests
from google.cloud import bigquery, storage
from io import BytesIO
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm # A library for progress bars, pip install tqdm

# --- Configuration ---
PROJECT_ID = "<gcp-project-id>"
DATASET_ID = "<dataset-id>"
TABLE_ID = "target_ads"
BUCKET_NAME = "semantic-product-images"  # Your GCS bucket name
MAX_WORKERS = 16  # Adjust based on your machine's cores (e.g., 16 for your notebook)

# --- Initialize GCS Client (outside the function for efficiency) ---
# Note: BQ client can't be passed between processes easily, but storage client is fine.
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

def process_image(ad_row):
    """
    Function to process a single ad: download, upload, and return the new URI.
    This function will be run by each worker process.
    """
    http_url = ad_row['ad_image_url']
    file_name = f"{ad_row['product_id']}.jpg"
    gcs_uri = f"gs://{BUCKET_NAME}/{file_name}"

    try:
        # Download the image
        response = requests.get(http_url, stream=True, timeout=20)
        response.raise_for_status()

        # Upload to GCS
        blob = bucket.blob(file_name)
        blob.upload_from_file(BytesIO(response.content), content_type='image/jpeg')

        # Return the successful mapping
        return {
            'ad_id': ad_row['ad_id'],
            'product_id': ad_row['product_id'],
            'ad_image_url': http_url,
            'gcs_image_uri': gcs_uri
        }
    except Exception as e:
        # Log the error and return None for this row
        # print(f"Error processing {http_url}: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Fetch ad data from BigQuery
    print("Fetching ads from BigQuery...")
    bq_client = bigquery.Client()
    query = f"SELECT ad_id, product_id, ad_image_url FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
    df = bq_client.query(query).to_dataframe()
    print(f"Found {len(df)} ads to process.")

    # Convert dataframe rows to a list of dictionaries to pass to workers
    tasks = df.to_dict('records')
    results = []

    # 2. Use ProcessPoolExecutor to run tasks in parallel
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Create a future for each task
        future_to_task = {executor.submit(process_image, task): task for task in tasks}

        # Use tqdm for a live progress bar
        for future in tqdm(as_completed(future_to_task), total=len(tasks), desc="Migrating Images"):
            result = future.result()
            if result:  # Only append successful results
                results.append(result)

    print(f"\nImage migration complete. Successfully processed {len(results)}/{len(tasks)} images.")

    # 3. Create a final DataFrame and save to CSV
    if results:
        updated_df = pd.DataFrame(results)
        updated_df.to_csv("target_ads_with_gcs_uris.csv", index=False)
        print("Saved updated ad data to 'target_ads_with_gcs_uris.csv'")
        print("You should now upload this new CSV to a BigQuery table (e.g., 'target_ads_gcs').")
    else:
        print("No images were successfully processed.")