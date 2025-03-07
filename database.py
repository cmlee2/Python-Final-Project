# from models import Song
from last_fm_api import get_track_info, find_recommendations, get_album_info, get_artist_info
import uuid
import json
import os


# New Database class
class DataBase():
    # Initialize class
    def  __init__(self):
        # Ranking for Songs
        self._data = {
            'song': {},
            'album' : {},
            'artist' : {},
        }
        self._rankings = {
            'song': [],
            'album' : [],
            'artist' : [],            
        }
        self._ongoing_ranking = {}

        # Load rankings to see if there's any files
        self.load_rankings()

    # Load Rankings
    def load_rankings(self):
        # See if path exists
        if os.path.exists('rankings.json'):
            # try to load 
            try:
                # Open file and get necessary data
                with open('rankings.json', "r") as file:
                    data = json.load(file)
                    self._data['song'] = data.get("song_data", {})
                    self._rankings['song'] = data.get("song_rankings", [])
                    self._data['album'] = data.get("album_data", {})
                    self._rankings['album'] = data.get("album_rankings", [])
                    self._data['artist'] = data.get("artist_data", {})
                    self._rankings['artist'] = data.get("artist_rankings", [])
            # If load doesn't work start empy
            except json.JSONDecodeError:
                print('No JSON found, starting with empty ranings')

    # Save Rankings
    def save_rankings(self):
        # Open file
        with open('rankings.json', "w") as file:
            # Dump data into json
            json.dump(
                {
                    "song_data": self._data['song'],
                    "song_rankings": self._rankings['song'],
                    "album_data": self._data['album'],
                    "album_rankings": self._rankings['album'],
                    "artist_data": self._data['artist'],
                    "artist_rankings": self._rankings['artist'],
                },
                file,
                indent=4
            )
        # Print to confirm
        print("Rankings saved")


    def add_item(self, item_type, title = None, artist=None):
        '''Function to add items to the ranking system
        param item_type: 'song', 'artist', 'album
        param title: name of song or album
        param artist:n name of artist

        '''
        # Check user input
        if item_type not in ['song', 'album', 'artist']:
            raise ValueError('Must be song, album, or artist')
        
        # Get info depending on what the user asked for
        if item_type == 'song':
            item_info = get_track_info(artist=artist, track=title)
        elif item_type == 'album':
            item_info = get_album_info(artist=artist, album=title)
        elif item_type == 'artist':
            item_info = get_artist_info(artist=artist)
        
        # If None, return None
        if not item_info:
            return None
        
        # Get unique ID
        item_id = str(uuid.uuid4())
        # Store item info
        self._data[item_type][item_id] = item_info

        # If it's the first item, add it without comparison
        if len(self._rankings[item_type]) == 0:
            self._rankings[item_type].append(item_id)
            # Save rankings
            self.save_rankings()
            # Return and let them know what was added
            if item_type == 'song':
                print(self._data[item_type][item_id])
                return f'{self._data[item_type][item_id]['song_name']} added'
            elif item_type == 'album':
                return f'{self._data[item_type][item_id]['album_name']} added'
            elif item_type == 'artist':
                return f'{self._data[item_type][item_id]['artist_name']} added'
        
        # Start rankings
        self._ongoing_ranking[(item_type, item_id)] = {
            'low':0,
            'high': len(self._rankings[item_type]) - 1
        }

        # Get comparison id
        comparison_id = self.get_next_comparison(item_type, item_id)

        # Save ranking
        self.save_rankings()

        # Return what to compare with
        if item_type == 'song':
            return {
                'item_id': item_id,
                'name' : self._data[item_type][item_id]['song_name'],
                'compare_with': comparison_id,
                'compare_with_name' : self._data[item_type][comparison_id]['song_name']
            }
        elif item_type == 'album':
            return {
                'item_id': item_id,
                'item_name' : self._data[item_type][item_id]['album_name'],
                'compare_with': comparison_id,
                'compare_with_name' : self._data[item_type][comparison_id]['album_name']
            }
        elif item_type == 'artist':
            return {
                'item_id': item_id,
                'name' : self._data[item_type][item_id]['artist_name'],
                'compare_with': comparison_id,    
                'compare_with_name' : self._data[item_type][comparison_id]['artist_name']
            }
            
    def update_ranking(self, item_type, item_id, comparison_id, user_preference):
        """
        Updates the ranking based on user input and returns the next comparison.
        
        :param item_type: "song", "album", or "artist"
        :param item_id: ID of the item being ranked
        :param comparison_id: ID of the item it was compared with
        :param user_preference: "better" if item should be ranked higher, "worse" otherwise
        """
        # See if key is currently being ranked
        key = (item_type, item_id)

        if key not in self._ongoing_ranking:
            return None  


        # Get the index of the comparison item in the ranking list
        mid = self._rankings[item_type].index(comparison_id)

        # Adjust ranking boundaries based on the user's choice
        if user_preference == "better":
            self._ongoing_ranking[key]["high"] = mid - 1
        else:
            self._ongoing_ranking[key]["low"] = mid + 1

        # If low exceeds high, we have found the correct position
        if self._ongoing_ranking[key]["low"] > self._ongoing_ranking[key]["high"]:
            insert_position = self._ongoing_ranking[key]["low"]
            self._rankings[item_type].insert(insert_position, item_id)
            del self._ongoing_ranking[key]  # Remove from active ranking session
            self.save_rankings()
            return None  # Ranking is complete

        # Get the next comparison
        return self.get_next_comparison(item_type, item_id)

    def get_next_comparison(self, item_type, item_id):
        """Finds the next item for ranking comparison using binary search.
        params item_type: song, album, artist
        params item_id: uuid to identify the current song being looked at
        """
        # Key
        key = (item_type, item_id)

        # Check to see if key exists
        if key not in self._ongoing_ranking:
            return None  

        # Find the low and high of the new key
        low = self._ongoing_ranking[key]["low"]
        high = self._ongoing_ranking[key]["high"]

        # If low is higher than high, binary search is done
        if low > high:
            return None  

        # Find new midpoint
        mid = (low + high) // 2
        return self._rankings[item_type][mid] 

    def display_rankings(self, item_type):
        '''Display the rankings
        params item_type: song, artist, album
        '''
        # List comprehension to return ranking info
        ranked_info = [self._data[item_type][id] for id in self._rankings[item_type]]
        # Return ranked info
        return ranked_info

    def get_recommendations(self, artist=None, track = None):
        '''Get recommendations for a song
        params artist: artistn name
        params track: track name
        '''
        # check to see if there are recommendations
        recommendations = find_recommendations(artist=artist, track=track)
        # if no recommendations, return None
        if not recommendations:
            return None
        # Return recommendations
        return recommendations
    
    

    