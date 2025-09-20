# Generates a synthetic users dataset of 5,000 records, where each user is assigned a
# primary shopping category with its segment, plus 1–3 secondary categories and their segments.
# It enriches users with demographics like age group, gender, country, and preferred device to simulate diversity.
# The result is saved as users.csv, providing realistic user profiles for targeting and behavior modeling

import pandas as pd
import random

# Load mapping: category_id, category_name, primary_segment, secondary_segments
mapping_df = pd.read_csv(
    "<your path in jupyter notebook to category_segment_mapping.csv>",
    names=["category_id", "category_name", "primary_segment", "secondary_segments"]
)

NUM_USERS = 5000
users_data = []

for i in range(NUM_USERS):
    user_id = f"U{i + 1:05d}"

    # Pick a primary category randomly
    primary_row = mapping_df.sample(1).iloc[0]
    primary_category_id = primary_row['category_id']
    primary_segment = primary_row['primary_segment']

    # Pick 1–3 random secondary category IDs (excluding the primary one)
    other_categories = mapping_df[mapping_df['category_id'] != primary_category_id]
    secondary_category_ids = list(other_categories.sample(random.randint(1, 3))['category_id'])

    # Lookup their primary_segment values to populate secondary_segments
    secondary_segments_list = list(
        mapping_df[mapping_df['category_id'].isin(secondary_category_ids)]['primary_segment']
    )

    users_data.append({
        "user_id": user_id,
        "primary_category_id": primary_category_id,
        "primary_segment": primary_segment,
        "secondary_category_ids": ",".join(map(str, secondary_category_ids)),
        "secondary_segments": ",".join(secondary_segments_list),
        "age_group": random.choice(["18-24", "25-34", "35-44", "45-54", "55+"]),
        "gender": random.choice(["Male", "Female", "Other"]),
        "country": random.choice(["US", "UK", "CA", "AU", "IN"]),
        "preferred_device": random.choice(["mobile", "desktop", "tablet"])
    })

users_df = pd.DataFrame(users_data)
users_df.to_csv("<your path in jupyter notebook where you want to save users.csv>", index=False)

print(f"✅ Generated {len(users_df)} users and saved to users.csv")