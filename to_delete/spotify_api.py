# Import Dependencies
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import constants 
from models import Song


# Import API Data
my_client_id = constants.Client_ID
my_client_secret = constants.Client_Secret

# Utilize Spotipy to create instance
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=my_client_id, client_secret=my_client_secret))

# Get track info
def get_track_data(artist = None, track = None):
    # Ensure Data is filled
    if artist is not None and track is not None:
        # Search for Artist
        track_info = sp.search(q='artist:' + artist + ' track:' + track, type='track')
        
        # Try to make sure there are itmes
        
        if not track_info['tracks']['items']:
            return 'No track found. Please check your track title and artist name'
        
        # Get first track
        first_result = track_info['tracks']['items'][0]

        # Image URL save
        image_url = first_result['album']['images'][1]['url'] if len(first_result['album']['images']) > 1 else ''


        # Save as class
        song = Song(
            song_name = first_result['name'],
            picture = image_url,
            artist = first_result['artists'][0]['name'],
            song_id = first_result['id'],
            album = first_result['album']['name'] 
        )
        # Return song
        return song

    # If they did not enter right data
    return 'Please enter a track and artist to search'


    