import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px
from datetime import datetime

# Authenticate the Spotify API with your client ID and client secret
client_id = "dd6b3d9b8e6644ca80a399ff7e8d5a6e"
client_secret = "4594fd9a71014bcd87bcf87d2cef5148"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create a Streamlit app
st.title("Spotify Playlist Analyzer")

# Add a sidebar for user input
playlist_name = st.sidebar.text_input("Enter the name of the Spotify playlist:")

# Search for the playlist ID based on the name
if playlist_name:
    playlists = sp.search(playlist_name, type="playlist")["playlists"]["items"]
    if playlists:
        playlist_id = playlists[0]["id"]
    else:
        st.write("No playlists found with that name.")
        playlist_id = None
else:
    playlist_id = None

# Retrieve data from the Spotify API
if playlist_id:
    playlist = sp.playlist(playlist_id)
    tracks = playlist["tracks"]["items"]
    track_names = [track["track"]["name"] for track in tracks]
    track_artists = [", ".join([artist["name"] for artist in track["track"]["artists"]]) for track in tracks]
    track_popularity = [track["track"]["popularity"] for track in tracks]
    track_duration = [track["track"]["duration_ms"] for track in tracks]
    track_album = [track["track"]["album"]["name"] for track in tracks]
    track_release_date = [track["track"]["album"]["release_date"] for track in tracks]

    # Display the playlist data in a table
    st.write(f"## {playlist['name']}")
    st.write(f"**Description:** {playlist['description']}")
    st.write(f"**Number of tracks:** {len(tracks)}")
    st.write("")
    st.write("### Tracklist")
    for i in range(len(tracks)):
        st.write(f"{track_names[i]} by {track_artists[i]}")

    # Create a dataframe from the playlist data
    data = {
        "Name": track_names,
        "Artist": track_artists,
        "Album": track_album,
        "Release Date": track_release_date,
        "Popularity": track_popularity,
        "Duration (ms)": track_duration,
    }
    df = pd.DataFrame(data)

    # Ensure 'Popularity' is numeric
    df['Popularity'] = pd.to_numeric(df['Popularity'], errors='coerce')

    # Drop rows with invalid 'Popularity'
    df = df.dropna(subset=['Popularity'])

    # Display a bar chart of the top 10 most popular artists in the playlist
    st.write("#### Top 10 Artists")
    top_artists = (
        df.groupby("Artist", as_index=False)["Popularity"]
        .mean()
        .sort_values("Popularity", ascending=False)
        .head(10)
    )
    fig_top_artists = px.bar(top_artists, x="Artist", y="Popularity", title="Top 10 Artists")
    st.plotly_chart(fig_top_artists)

    # Display a bar chart of the top 10 most popular songs in the playlist
    st.write("#### Top 10 Songs")
    top_songs = (
        df.groupby("Name", as_index=False)["Popularity"]
        .mean()
        .sort_values("Popularity", ascending=False)
        .head(10)
    )
    fig_top_songs = px.bar(top_songs, x="Name", y="Popularity", title="Top 10 Songs")
    st.plotly_chart(fig_top_songs)

    # Display a line chart of track release date vs. popularity
    st.write("#### Release Date vs. Popularity")
    df["Release Year"] = pd.to_datetime(df["Release Date"]).dt.year
    popularity_by_year = df.groupby("Release Year").mean().reset_index()[["Release Year", "Popularity"]]
    fig_release_date_popularity = px.line(popularity_by_year, x="Release Year", y="Popularity", title="Release Date vs. Popularity")
    st.plotly_chart(fig_release_date_popularity)

# End of App
st.write("---")
st.write("Created by Chukwuebuka Ezeokeke")
st.write("Check out the code on [GitHub](https://github.com/Chukwuebuka-2003/spotify-playlist-analyzer).")
st.write("Powered by [Streamlit](https://streamlit.io/), [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/), [Pandas](https://pandas.pydata.org/), and [Plotly](https://plotly.com/).")
st.write("Data provided by the [Spotify API](https://developer.spotify.com/documentation/web-api/).")
