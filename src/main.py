# app.py
import streamlit as st
from recommend import df, recommend_songs

# Set custom Streamlit page config
st.set_page_config(
    page_title="Music Recommender 🎵",
    page_icon="🎧",  # You can also use a path to a .ico or .png file
    layout="centered"
)


st.title("🎶 Instant Music Recommender")

song_list = sorted(df['song'].dropna().unique())
selected_song = st.selectbox("🎵 Select a song:", song_list)

moods = ['All', 'happy', 'sad', 'chill', 'angry', 'neutral']
selected_mood = st.selectbox("🎭 Filter by mood (optional):", moods)

mood_filter = None if selected_mood == "All" else selected_mood


if st.button("🚀 Recommend Similar Songs"):
    with st.spinner("Finding similar songs..."):
        recommendations = recommend_songs(selected_song, mood=mood_filter)

        if recommendations is None or recommendations.empty:
            st.warning("Sorry, no recommendations found.")
        else:
            st.success(f"Top similar songs (Mood: {selected_mood})")
            st.table(recommendations)