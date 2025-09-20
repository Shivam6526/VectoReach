# Generates an ads dataset by sampling 30% of products from each category and
# rotating them through predefined ad templates to create ad text.
# For each ad, it assigns a random image from the same category (falling back to the original if none available),
# generates unique ad_ids, and derives target_keywords from the category name.
# The final ads (with text, image, keywords, and metadata) are saved into ads.csv for use in targeting experiments

import pandas as pd
import numpy as np
import uuid

# Load CSVs
products_df = pd.read_csv("<your jupyter notebook path to products.csv>")
categories_df = pd.read_csv("<your jupyter notebook path to categories.csv>")

# Merge categories
products_df = products_df.merge(categories_df, left_on="category_id", right_on="id", how="left")

# Sample 30% per category
def sample_category(group):
    n = max(1, int(len(group) * 0.3))
    return group.sample(n=n, random_state=42)

sampled_products = products_df.groupby("category_name", group_keys=False).apply(sample_category).reset_index(drop=True)

# Template rotation
ad_templates = [
    "20% off all {category} today!",
    "Save big on {category} — shop now!",
    "Special deal on {category} — limited time!",
    "Get the best {category} at unbeatable prices!"
]

sampled_products = sampled_products.sample(frac=1, random_state=42).reset_index(drop=True)
sampled_products["ad_template"] = [ad_templates[i % len(ad_templates)] for i in range(len(sampled_products))]
sampled_products["ad_text"] = [
    template.format(category=cat)
    for template, cat in zip(sampled_products["ad_template"], sampled_products["category_name"])
]

# Precompute category → list of images
category_images = products_df.groupby("category_id")["imgUrl"].apply(list).to_dict()

# Vectorized random image selection
cat_ids = sampled_products["category_id"].values
orig_imgs = sampled_products["imgUrl"].values
new_imgs = np.empty_like(orig_imgs, dtype=object)

for cat_id in np.unique(cat_ids):
    idxs = np.where(cat_ids == cat_id)[0]
    imgs = np.array(category_images[cat_id])
    for i in idxs:
        possible_imgs = imgs[imgs != orig_imgs[i]]
        if len(possible_imgs) == 0:
            new_imgs[i] = orig_imgs[i]
        else:
            new_imgs[i] = np.random.choice(possible_imgs)

sampled_products["ad_image_url"] = new_imgs
sampled_products["used_fallback_image"] = sampled_products["ad_image_url"] == sampled_products["imgUrl"]

# Assign ad_id, ad_title, target_keywords
sampled_products["ad_id"] = [str(uuid.uuid4())[:8] for _ in range(len(sampled_products))]
sampled_products["ad_title"] = sampled_products["ad_text"]
sampled_products["target_keywords"] = sampled_products["category_name"].str.lower().str.replace("&", "").str.replace(",", "").str.replace(" ", ",")

# Save CSV
ads_df = sampled_products[[
    "ad_id", "asin", "ad_title", "ad_text", "ad_image_url",
    "target_keywords", "category_id", "category_name", "used_fallback_image"
]].rename(columns={"asin": "product_id"})

ads_df.to_csv("<your path in jupyter notebook where you want to save ads.csv>", index=False)
print(f"✅ Generated {len(ads_df)} ads")
print(f"📌 {sampled_products['used_fallback_image'].sum()} fallback images")