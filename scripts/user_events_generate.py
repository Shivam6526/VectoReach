# Generates a synthetic user_events.csv dataset by simulating user interactions with products.
# For each user, it randomly samples products from their primary or secondary categories and
# assigns random event types (view, click, add_to_cart, purchase) with timestamps as given.
# Each event is enriched with user segments and stored with a unique event_id.
# Finally, all events are saved to CSV for use in analytics or vector search experiments.

import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

# Load users and products
users_df = pd.read_csv("<your jupyter notebook path to users.csv>")
products_df = pd.read_csv("<your jupyter notebook path products.csv>")

events_data = []


def random_date(start, end):
    delta = end - start
    random_seconds = random.randrange(int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


# add start_date and end_date as per your choice
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 8, 31)

for _, user in users_df.iterrows():
    try:
        # Parse secondary category IDs safely
        secondary_ids = [
            int(cid.strip()) for cid in str(user['secondary_category_ids']).split(",") if cid.strip().isdigit()
        ]
    except:
        secondary_ids = []

    primary_products = products_df[products_df['category_id'] == user['primary_category_id']]
    secondary_products = products_df[products_df['category_id'].isin(secondary_ids)]

    for _ in range(random.randint(5, 20)):  # Events per user
        roll = random.random()

        if roll < 0.7 and not primary_products.empty:
            product = primary_products.sample(1).iloc[0]
        elif roll < 0.9 and not secondary_products.empty:
            product = secondary_products.sample(1).iloc[0]
        else:
            product = products_df.sample(1).iloc[0]

        events_data.append({
            "event_id": str(uuid.uuid4())[:8],
            "user_id": user['user_id'],
            "asin": product['asin'],  # products.csv uses asin
            "category_id": product['category_id'],
            "event_type": random.choice(["view", "click", "add_to_cart", "purchase"]),
            "event_timestamp": random_date(start_date, end_date).isoformat(),
            # Optional enrichment for analytics:
            "primary_segment": user["primary_segment"],
            "secondary_segments": user["secondary_segments"]
        })

events_df = pd.DataFrame(events_data)
events_df.to_csv("<your path in jupyter notebook where you want to save user_events.csv>", index=False)

print(f"✅ Generated {len(events_df)} events across {events_df['category_id'].nunique()} categories")
