from pydantic import BaseModel

# Class with data I want to store
class Song(BaseModel):
    song_name: str
    artist: str
    song_id: str
    album: str
    album_cover: str
    tags: list
    duration_s: float 
    total_plays: int

class SongRequest(BaseModel):
    artist: str
    title: str

class SongResponse(BaseModel):
    song_name: str
    artist: str
    song_id: str
    album: str
    album_cover: str
    tags: list
    duration_s: float 
    total_plays: int
    reference_song_id : str
