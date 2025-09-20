import streamlit as st
from google.cloud import bigquery

# -------------------
# Setup
# -------------------
PROJECT_ID = "<project-id>"
DATASET = "semantic_ads_targeting"

USER_TABLE = f"{PROJECT_ID}.{DATASET}.user_profiles_with_embeddings_primary"
ADS_TABLE = f"{PROJECT_ID}.{DATASET}.target_ads_embeddings"
ADS_ORIGINAL_TABLE = f"{PROJECT_ID}.{DATASET}.target_ads"

client = bigquery.Client()
# or, use SA json file
# client = bigquery.Client.from_service_account_json(r"<path to SA json file>")

st.set_page_config(page_title="Semantic vs Keyword Ads Demo: Text Embeddings based", layout="wide")
st.title("🎯 Semantic vs Keyword Ads Targeting Demo")

# -------------------
# User Input
# -------------------
user_id = st.text_input("Enter a user_id:", "U02876")

if st.button("Find Ads"):
    # -------------------
    # Query User Profile
    # -------------------
    user_query = f"""
    SELECT user_id, content, ml_generate_embedding_result AS embedding
    FROM `{USER_TABLE}`
    WHERE user_id = '{user_id}'
    """
    user_row = client.query(user_query).result().to_dataframe()

    if user_row.empty:
        st.warning(f"No data found for user {user_id}")
        st.stop()

    user_content = user_row.iloc[0]["content"]

    st.subheader("👤 User Profile")
    st.write(f"**Interaction Summary:** {user_content}")

    # -------------------
    # Keyword-based search
    # -------------------
    first_keyword = user_content.lower().split()[0]

    keyword_query = f"""
    SELECT e.ad_id, e.content, a.ad_image_url
    FROM `{ADS_TABLE}` e
    JOIN `{ADS_ORIGINAL_TABLE}` a
    ON e.ad_id = a.ad_id
    WHERE LOWER(e.content) LIKE "%{first_keyword}%"
    LIMIT 5
    """
    keyword_results = client.query(keyword_query).result().to_dataframe()

    # -------------------
    # Semantic search using VECTOR_SEARCH
    # -------------------
    semantic_query = f"""
    SELECT base.ad_id, base.content, a.ad_image_url, distance
    FROM VECTOR_SEARCH(
      TABLE `{ADS_TABLE}`,
      'ml_generate_embedding_result',
      (SELECT ml_generate_embedding_result
       FROM `{USER_TABLE}`
       WHERE user_id = '{user_id}'),
      top_k => 5
    )
    JOIN `{ADS_ORIGINAL_TABLE}` a
    ON base.ad_id = a.ad_id
    """
    semantic_results = client.query(semantic_query).result().to_dataframe()

    # -------------------
    # Display Results Side by Side
    # -------------------
    col1, col2 = st.columns(2)

    # Helper to render ad "cards"
    def render_ads(df, semantic=False):
        if df.empty:
            st.info("No ads found.")
            return

        for _, row in df.iterrows():
            with st.container():
                st.markdown(
                    """
                    <div style="
                        border:1px solid #ddd;
                        border-radius:10px;
                        padding:10px;
                        margin-bottom:15px;
                        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
                        background-color:white;">
                    """,
                    unsafe_allow_html=True,
                )
                st.image(row["ad_image_url"], width=200)
                st.markdown(f"**{row['content']}**")
                meta = f"🆔 {row['ad_id']}"
                if semantic:
                    meta += f"  |  🔍 Distance: {row['distance']:.4f}"
                st.caption(meta)
                st.markdown("</div>", unsafe_allow_html=True)

    with col1:
        st.subheader("🔑 Keyword-based Ads")
        render_ads(keyword_results, semantic=False)

    with col2:
        st.subheader("🤖 Semantic-based Ads")
        render_ads(semantic_results, semantic=True)
