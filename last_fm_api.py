# Import Dependencies
import constants 
from models import Song
import pylast
import shortuuid


# Import API Data
my_client_id = constants.last_fm_id
my_client_secret = constants.last_fm_secret

lastfm  = pylast.LastFMNetwork(api_key= my_client_id, api_secret= my_client_secret)

def get_track_info(artist = None, track = None):
    if artist is not None and track is not None:
        try:
            track = lastfm.get_track(artist, track)
            tags = track.get_top_tags()
            tag_list = [(tag.item.name, tag.weight) for tag in tags]
            album = track.get_album()
            album_name = album.get_name() if album else 'Unknown'
            
            image_url = album.get_cover_image() if album else 'No Image Available'

            song = Song(
                    song_name = str(track.get_title()),
                    artist = str(track.get_artist()),
                    song_id = shortuuid.uuid()[:6],
                    album = str(album_name),
                    album_cover = str(image_url),
                    tags = tag_list,
                    duration_s = round(track.get_duration() / 1000, 2),
                    total_plays = int(track.get_playcount())

            )
            return song

        except pylast.WSError as e:
            print(f'Error: {e}')

print(get_track_info(artist='Tyler, the Creator', track='St. Chroma'))