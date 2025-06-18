# recommend.py
import joblib
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("recommend.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("🔁 Loading data...")
try:
    df = joblib.load('df_cleaned.pkl')
    cosine_sim = joblib.load('cosine_sim.pkl')
    logging.info("✅ Data loaded successfully.")
except Exception as e:
    logging.error("❌ Failed to load required files: %s", str(e))
    raise e


def recommend_songs(song_name, mood=None, top_n=5):
    logging.info("🎵 Recommending songs for: '%s' with mood: '%s'", song_name, mood)
    
    idx = df[df['song'].str.lower() == song_name.lower()].index
    if len(idx) == 0:
        logging.warning("⚠️ Song not found in dataset.")
        return None
    
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the most similar songs
    song_indices = [i[0] for i in sim_scores[1:]]  # skip the input song itself

    result_df = df.iloc[song_indices]

    # If mood is specified, filter it
    if mood:
        result_df = result_df[result_df['mood'] == mood]
        if result_df.empty:
            logging.warning("⚠️ No songs found with matching mood. Returning empty result.")
            return result_df

    # Limit to top_n results
    result_df = result_df[['artist', 'song', 'mood']].head(top_n).reset_index(drop=True)
    result_df.index = result_df.index + 1  # Start from 1 instead of 0
    result_df.index.name = "S.No."

    logging.info("✅ Top %d recommendations ready.", len(result_df))

    return result_df