# spotify-playlist-analyzer
 Spotify Playlist Analyzer code built with Python allows users to analyze the data of a Spotify playlist using Streamlit and Plotly

The Spotify Playlist Analyzer is a Streamlit app that allows users to analyze a Spotify playlist using data visualization tools. The app uses the Spotipy library to access data from the Spotify API and the Plotly library to create interactive charts.

To use the app, the user inputs the name of the Spotify playlist they wish to analyze in a text input box on the sidebar. The app then searches for the playlist ID based on the input name and retrieves the playlist data from the Spotify API. The playlist data is displayed in a table that shows the track name, artist name, album name, release date, popularity, and duration in milliseconds for each track in the playlist.

The app also provides three types of analysis for the playlist data:

Track Popularity Distribution - a histogram that shows the distribution of track popularity in the playlist.
Bivariate Analysis - a scatter plot that allows the user to select two variables (popularity and duration in milliseconds) to plot against each other.
Multivariate Analysis - a scatter plot that allows the user to select one variable to color the data points by (artist name, album name, or release date) and one variable to size the data points by (popularity or duration in milliseconds).
In addition to the data visualizations, the app also provides a playlist summary that shows the most popular and least popular tracks in the playlist and a bar chart that displays the top 10 most popular artists in the playlist.

Overall, the Spotify Playlist Analyzer is a useful tool for anyone who wants to explore the data behind their favorite Spotify playlists and gain insights into their music preferences.
