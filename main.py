import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load web page
get_date = input("Which date would you like to travel to? Type date in YYYY-MM-DD format: ")
year = get_date.split('-')[0]
my_link = f"https://www.billboard.com/charts/hot-100/{get_date}/"
respond = requests.get(my_link)
web_page = respond.text
print(my_link)

# Scraping songs and authors data
soup = BeautifulSoup(web_page, "html.parser")
song_data = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
author_data = soup.find_all(name="span", class_="a-no-trucate")
list_authors = [author.text.replace("\n", "").replace("\t", "") for author in author_data]
list_songs = [movie.text.replace("\n", "").replace("\t", "") for movie in song_data]
print(list_authors)
print(list_songs)

# Connect Spotipy API
MY_APP_CLIENT_ID = "0230baf7815f4658b9731a197440545e"
MY_APP_CLIENT_SECRET = "cca73f0159aa4a17bf6a10ab6e62a744"
MY_APP_REDIRECT_URI = "http://example.com"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=MY_APP_CLIENT_ID,
                                               client_secret=MY_APP_CLIENT_SECRET,
                                               redirect_uri=MY_APP_REDIRECT_URI,
                                               scope="playlist-modify-public"))
USER_ID = sp.current_user()["id"]

# Extract id of tracks and append it to the list
tracks_id = []
items = []
for i in range(100):
    results = sp.search(q=f'song: {list_songs[i]}, author: {list_authors[i]}', type='track', limit=1)
    items.append(results['tracks']['items'])
for item in items:
    id_to_append = item[0]["id"]
    tracks_id.append(id_to_append)
# Create a playlist and add tracks
new_playlist = sp.user_playlist_create(user=USER_ID, name=f"Coded(by me) Billboard100 {year}", public=True, description="nice")
playlist_id = new_playlist["id"]
sp.user_playlist_add_tracks(USER_ID, playlist_id, tracks_id, position=None)
