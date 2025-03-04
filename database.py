from models import Song


# New Database class
class DataBase():
    # Initialize class
    def  __init__(self):
        self._data = {}
        self._rankings = []
        self._pending_rankings = {}

    def add_song(self, song: Song):
        self._data[song.song_id] = song
        if not self._rankings:
            self._rankings.append(song.song_id)
        # else: 
        #     self.insert_song(song.song_id)

    def start_ranking(self, song_id: str):
        if song_id in self._pending_rankings:
            return self._pending_rankings[song_id]
        
        if not self._rankings:
            self._rankings.append(song_id)
            return None
        
        self._pending_rankings[song_id] = {'low': 0, 'high': len(self._rankings) - 1}
        return self.get_next_comparison(song_id)
    
    def get_next_comparison(self, song_id: str):
        if song_id not in self._pending_rankings:
            return None
        
        state =  self._pending_rankings[song_id]

        low, high = state['low'], state['high']

        if low > high:
            position = low
            self._rankings.insert(position, song_id)
            del self._pending_rankings[song_id]
            return None
        
        mid = (low+high) // 2
        reference_song_id = self._rankings[mid]
        return reference_song_id
    
    def update_ranking(self, song_id: str, reference_song_id: str, preffered: bool):
        if song_id not in self._pending_rankings:
            return False
        
        state = self._pending_rankings[song_id]
        ref_index = self._rankings(reference_song_id)

        if preffered:
            state['high'] = ref_index - 1
        
        else:
            state['low'] = ref_index + 1


        return self.get_next_comparison(song_id)

    def get_ranking(self):
        return [self._data[song_id] for song_id in self._rankings]

    # # Return value when given key
    # def get(self, key):
    #     return self._data[key]
    
    # # Add entry to data
    # def put(self, key, value):
    #     self._data[key] = value

    # # Return all
    # def all(self):
    #     return self._data
    
    # # Delete from data
    # def delete(self, key):
    #     self._data.pop(key)
    