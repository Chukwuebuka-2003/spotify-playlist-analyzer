import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import plotly.express as px
from datetime import datetime



# authenticate the Spotify API with your client ID and client secret
client_id = st.secrets["spotify"]["client_id"]
client_secret = st.secrets["spotify"]["client_secret"]
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# create a Streamlit app
st.title("Spotify Playlist Analyzer")

# add a sidebar for user input
playlist_name = st.sidebar.text_input("Enter the name of the Spotify playlist:")

# search for the playlist ID based on the name
if playlist_name:
    playlists = sp.search(playlist_name, type="playlist")["playlists"]["items"]
    if playlists:
        playlist_id = playlists[0]["id"]
    else:
        st.write("No playlists found with that name.")
        playlist_id = None
else:
    playlist_id = None

# retrieve data from the Spotify API
if playlist_id:
    playlist = sp.playlist(playlist_id)
    tracks = playlist["tracks"]["items"]
    track_names = [track["track"]["name"] for track in tracks]
    track_artists = [", ".join([artist["name"] for artist in track["track"]["artists"]]) for track in tracks]
    track_popularity = [track["track"]["popularity"] for track in tracks]
    track_duration = [track["track"]["duration_ms"] for track in tracks]
    track_album = [track["track"]["album"]["name"] for track in tracks]
    track_release_date = [track["track"]["album"]["release_date"] for track in tracks]

    # display the playlist data in a table
    # Create a DataFrame with the playlist data
    playlist_data = {
        "Name": track_names,
        "Artist": track_artists,
        "Album": track_album,
        "Release Date": track_release_date,
        "Popularity": track_popularity,
        "Duration (ms)": track_duration,
    }

    df = pd.DataFrame(playlist_data)

# Display playlist details and DataFrame
    st.write(f"## {playlist['name']}")
    st.write(f"**Description:** {playlist['description']}")
    st.write(f"**Number of tracks:** {len(tracks)}")
    st.write("")

    st.write("### Tracklist")
    st.dataframe(df)

    # analyze the playlist data
    st.write("")
    st.write("### Playlist Analysis")

    # create a dataframe from the playlist data
    data = {"Name": track_names, "Artist": track_artists, "Album": track_album, "Release Date": track_release_date, "Popularity": track_popularity, "Duration (ms)": track_duration}
    df = pd.DataFrame(data)

    # display a histogram of track popularity
    fig_popularity = px.histogram(df, x="Popularity", nbins=20, title="Track Popularity Distribution")
    st.plotly_chart(fig_popularity)


    # add a dropdown menu for bivariate analysis
    st.write("#### Bivariate Analysis")
    x_axis = st.selectbox("Select a variable for the x-axis:", ["Popularity", "Duration (ms)","Release Date"])
    y_axis = st.selectbox("Select a variable for the y-axis:", ["Popularity", "Duration (ms)", "Release Date"])
    fig_bivariate = px.scatter(df, x=x_axis, y=y_axis, title=f"{x_axis} vs. {y_axis}")
    st.plotly_chart(fig_bivariate)

    # add a dropdown menu for multivariate analysis
    st.write("#### Multivariate Analysis")
    color_by = st.selectbox("Select a variable to color by:", ["Artist", "Album", "Release Date"])
    size_by = st.selectbox("Select a variable to size by:", ["Popularity", "Duration (ms)"])
    fig_multivariate = px.scatter(df, x="Duration (ms)", y="Popularity", color=color_by, size=size_by, hover_name="Name", title="Duration vs. Popularity Colored by Artist")
    st.plotly_chart(fig_multivariate)

    # add a summary of the playlist data
    st.write("")
    st.write("### Playlist Summary")
    st.write(f"**Most popular track:** {df.iloc[df['Popularity'].idxmax()]['Name']} by {df.iloc[df['Popularity'].idxmax()]['Artist']} ({df['Popularity'].max()} popularity)")
    st.write(f"**Least popular track:** {df.iloc[df['Popularity'].idxmin()]['Name']} by {df.iloc[df['Popularity'].idxmin()]['Artist']} ({df['Popularity'].min()} popularity)")
    

# display a bar chart of the top 10 most popular artists in the playlist
    st.write("#### Top 10 Artists")
    st.write("The bar chart below shows the top 10 most popular artists in the playlist.")
    # Ensure 'Popularity' is numeric
    df['Popularity'] = pd.to_numeric(df['Popularity'], errors='coerce')

# Drop rows with invalid 'Popularity'
    df = df.dropna(subset=['Popularity'])

# Group by 'Artist' and calculate the top 10 by average popularity
    top_artists = (
        df.groupby("Artist", as_index=False)["Popularity"]
        .mean()
        .sort_values("Popularity", ascending=False)
        .head(10)
   )

# Plot the bar chart
    fig_top_artists = px.bar(top_artists, x="Artist", y="Popularity", title="Top 10 Artists")
    st.plotly_chart(fig_top_artists)

# display a bar chart of the top 10 most popular songs in the playlist
    st.write("#### Top 10 Songs")
    st.write("The bar chart below shows the top 10 most popular songs in the playlist.")
    # Ensure 'Popularity' is numeric
    df['Popularity'] = pd.to_numeric(df['Popularity'], errors='coerce')

# Drop rows with invalid 'Popularity'
    df = df.dropna(subset=['Popularity'])

# Group by 'Name' and calculate the top 10 by average popularity
    top_songs = (
        df.groupby("Name", as_index=False)["Popularity"]
        .mean()
        .sort_values("Popularity", ascending=False)
        .head(10)
    )

# Plot the bar chart
    fig_top_songs = px.bar(top_songs, x="Name", y="Popularity", title="Top 10 Songs")


    st.plotly_chart(fig_top_songs)    

    # display a line chart of track release date vs. popularity
    st.write("#### Release Date vs. Popularity")
    st.write("The line chart below shows the relationship between track release date and popularity.")
    st.write("It seems that newer tracks are generally more popular than older tracks.")
    # Ensure 'Release Date' is in a valid datetime format
    df["Release Date"] = pd.to_datetime(df["Release Date"], errors="coerce")

# Drop rows with invalid 'Release Date' or 'Popularity'
    df = df.dropna(subset=["Release Date", "Popularity"])

# Extract the release year
    df["Release Year"] = df["Release Date"].dt.year

# Ensure 'Popularity' is numeric
    df["Popularity"] = pd.to_numeric(df["Popularity"], errors="coerce")

# Drop rows with invalid 'Popularity'
    df = df.dropna(subset=["Popularity"])

# Group by 'Release Year' and calculate average popularity
    popularity_by_year = (
        df.groupby("Release Year", as_index=False)["Popularity"]
        .mean()
        .sort_values("Release Year")
    )

# Plot the line chart
    fig_release_date_popularity = px.line(
        popularity_by_year,
        x="Release Year",
        y="Popularity",
        title="Release Date vs. Popularity"
    )
    st.plotly_chart(fig_release_date_popularity)

    # perform a bivariate analysis of popularity vs. release year and duration vs. release year
    st.write("")
    st.write("### Bivariate Analysis")

    # create a scatter plot of popularity vs. release year
    st.write("#### Popularity vs. Release Year")
    st.write("The scatter plot below shows the relationship between track popularity and release year.")
    fig_popularity_release_year = px.scatter(df, x="Release Year", y="Popularity", title="Popularity vs. Release Year")
    st.plotly_chart(fig_popularity_release_year)

    # create a scatter plot of duration vs. release year
    st.write("#### Duration vs. Release Year")
    st.write("The scatter plot below shows the relationship between track duration and release year.")
    fig_duration_release_year = px.scatter(df, x="Release Year", y="Duration (ms)", title="Duration vs. Release Year")
    st.plotly_chart(fig_duration_release_year)

    # perform a multivariate analysis of popularity, duration, and release year
    st.write("")
    st.write("### Multivariate Analysis")

    # create a 3D scatter plot of popularity, duration, and release year
    st.write("#### Popularity, Duration, and Release Year")
    st.write("The 3D scatter plot below shows the relationship between track popularity, duration, and release year.")
    fig_3d = px.scatter_3d(df, x="Release Year", y="Duration (ms)", z="Popularity", title="Popularity, Duration, and Release Year")
    st.plotly_chart(fig_3d)


    st.write("### Further Analysis")
    st.write("This app only scratches the surface of what can be done with Spotify data. With more time and resources, there are many interesting questions that could be explored. Here are a few examples:")
    st.write("- Are there certain times of day or days of the week when this playlist is most frequently played?")
    st.write("- What other playlists are most similar to this one, and what songs/artists do they have in common?")
    st.write("- Are there any interesting patterns in the lyrics or musical structure of the songs in this playlist?")
    st.write("")
    st.write("If you're interested in exploring these questions further, or have any other ideas for analysis, feel free to reach out!")

    st.write("---")
    st.write("Created by Chukwuebuka Ezeokeke")
    st.write("Check out the code on [GitHub](https://github.com/Chukwuebuka-2003/spotify-playlist-analyzer).")
    st.write("Powered by [Streamlit](https://streamlit.io/), [Spotipy](https://spotipy.readthedocs.io/en/2.19.0/), [Pandas](https://pandas.pydata.org/), and [Plotly](https://plotly.com/).")
    st.write("Data provided by the [Spotify API](https://developer.spotify.com/documentation/web-api/).")

