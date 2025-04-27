# Import libraries
import streamlit as st
import pandas as pd
import pickle

# 1. Streamlit Page Configuration (FIRST STREAMLIT COMMAND) — Only once!
st.set_page_config(page_title="Music Recommendation App 🎵", layout="wide")

# 2. 🎨 Set Custom Theme and Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ECDCE4;
    }
    h1, h2, h3, h4 {
        color: #6A0572;
    }
    div.stButton > button:first-child {
        background-color: #FF6F91;
        color: white;
        font-size: 18px;
        height: 3em;
        width: 100%;
        border-radius: 10px;
        border: None;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Title and Introduction
st.title("🎶 Personalized Music Recommendation System")
st.write("Welcome to your own AI-powered music recommendation app. Pick a song and discover similar vibes! 🌟")

# 4. Load the Data and Models
music_df = pickle.load(open('notebook/music.pkl', 'rb'))
similarity = pickle.load(open('notebook/similarity.pkl', 'rb'))

# 5. Recommendation Function
def recommend(song):
    index = music_df[music_df['Track_Name'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_songs = []
    for i in distances[1:6]:
        recommended_songs.append(music_df.iloc[i[0]].Track_Name)
    return recommended_songs

# Divider
st.divider()

# 📊 Popularity Trends (removed image)
st.header("🎵 Popularity Trends Across Tracks")
st.info("Track Popularity Overview")  # (Optional: can add a plot later)

# Divider
st.divider()

# 🔥 Top Trending Tracks
st.header("🔥 Top Trending Tracks Right Now!")

top_tracks = music_df['Track_Name'].value_counts().head(5).index.tolist()

for idx, track in enumerate(top_tracks, start=1):
    st.write(f"**{idx}. {track}**")

# Divider
st.divider()

# 🎵 Song Selection Section
st.header("🔎 Find Your Next Favorite Song!")

selected_song = st.selectbox(
    "Pick a song you like:",
    music_df['Track_Name'].values
)

if st.button("🎵 Recommend Similar Songs"):
    recommendations = recommend(selected_song)

    st.subheader("🔥 Recommended Songs for You:")

    for idx, song in enumerate(recommendations, 1):
        artist = music_df[music_df['Track_Name'] == song]['Artist_Name'].values[0]
        album = music_df[music_df['Track_Name'] == song]['Album_Name'].values[0]
        track_uri = music_df[music_df['Track_Name'] == song]['Track_URI'].values[0]

        if pd.notna(track_uri):
            track_id = track_uri.split(':')[-1]
            spotify_url = f"https://open.spotify.com/track/{track_id}"
            st.write(f"**{idx}. {song}**  \n*Artist:* {artist}  \n*Album:* {album}")

            st.markdown(
                f"""
                <a href="{spotify_url}" target="_blank">
                    <button style="background-color:#1DB954; color:white; padding:10px 24px; font-size:16px; border:none; border-radius:10px; cursor:pointer;">
                        ▶️ Play on Spotify
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )
        else:
            st.write(f"**{idx}. {song}**  \n*Artist:* {artist}  \n*Album:* {album}")

    st.success("Enjoy your music journey! 🚀🎶")

# Divider
st.divider()

# 📊 Metrics Section
st.header("📊 App Insights")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Songs in Database", len(music_df))
with col2:
    st.metric("Songs Recommended per Request", 5)

# Footer
st.markdown("Made by **Rishita** using Streamlit")
