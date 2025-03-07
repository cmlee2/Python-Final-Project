# Import Dependencies
import constants 
import pylast

# Import API Keys
my_client_id = constants.last_fm_id
my_client_secret = constants.last_fm_secret

# Connect to LastFM
lastfm  = pylast.LastFMNetwork(api_key= my_client_id, api_secret= my_client_secret)

# Function to get track info
def get_track_info (track = None,artist = None):
    '''Get Track info, returned as dictionary'''
    # Ensure artist and track is filled
    if artist is not None and track is not None:
        # Try statement
        try:
            # Find track and get tags, albums, album cover
            track = lastfm.get_track(title=track, artist=artist)
            tags = track.get_top_tags()
            tag_list = [(tag.item.name, tag.weight) for tag in tags[:5]]
            album = track.get_album()
            album_name = album.get_name() if album else 'Unknown'
            
            image_url = album.get_cover_image() if album else 'No Image Available'

            # Save as dictionary
            song = {
                    'song_name' : str(track.get_title()),
                    'artist' : str(track.get_artist()),
                    'album' : str(album_name),
                    'album_cover' : str(image_url),
                    'tags' : tag_list,
                    'duration_s' : round(track.get_duration() / 1000, 2),
                    'total_plays' :int(track.get_playcount())

            }
            # Return dictionary
            return song
        # Print error if something goes wrong
        except pylast.WSError as e:
            print(f'Error: {e}')

    # Return None if did not find anything
    return None


def find_recommendations(track = None, artist = None):
    '''Find recommendations based on a song and artist, returned as list
    A lot of modern songs do not have recommendations!!!
    '''
    # Ensure data is filled out
    if artist is not None and track is not None:
        # Get track that you want recommendations for
        track = lastfm.get_track(title = track, artist = artist)
        # Find 5 similar tracks
        similars = track.get_similar(limit= 5)
        # See if the list has entries
        if len(similars) > 0:
            # If has entries, return a list of the similar songs
            similar_songs = [(similar.item.artist.name, similar.item.title) for similar in similars]
            return similar_songs
        else:
            # Return None if no recommendations found
            return None
    # Return None if data was not filled out
    return None


def get_artist_info(artist = None):
    '''Function to get artist info, specifically their top tracks and listener counts'''
    # Ensure that value was filled out
    if artist is not None:
        # Get artist data and top tracks
        artist_data = lastfm.get_artist(artist_name= artist)
        top_tracks = artist_data.get_top_tracks()
        track_list = [(track.item.title, track.weight) for track in top_tracks[:5]]

        # Dictionary to store data
        artist = {
            'artist_name': str(artist_data.name),
            'listener_count': int(artist_data.get_listener_count()),
            'top_tracks' : track_list,

        }
        # Return Data
        return artist
    # Return None if data not filled out
    return None

def get_album_info(artist = None, album = None):
    '''Get album info using artist name and album name, Returns album cover, album name, artist,and track list'''
    # Ensure data was filled out correctly
    if artist is not None and album is not None:
        # Find the album and get the tracks
        album_data = lastfm.get_album(artist=artist, title= album)
        tracks = album_data.get_tracks()
        track_list = [(track.title) for track in tracks]
        # Dictionary to store data
        album_data = {
            'album_name' : str(album_data.get_name()),
            'album_cover' : str(album_data.get_cover_image()),
            'artist': str(album_data.get_artist()),
            'track_list' : track_list,

        }
        # Return Album Data
        return album_data
    
    # Return None if not found
    return None
