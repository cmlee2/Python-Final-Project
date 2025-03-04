# Import dependencies
from fastapi import FastAPI
from pydantic import BaseModel
from database import DataBase
from models import Song, SongRequest


# Create App and database
app = FastAPI()
app.db = DataBase()




# Basic test for hello world
@app.
def add_song(song: SongRequest)
    return {"hello": "world"}

# Return list of players
@app.get('/player')
def get_players():
    return app.db.all()

# Return specific player
@app.get('/player/{player_name}')
def get_player(player_name: str):
    # Clean string to ensure there is some consistency
    return app.db.get(player_name.lower().replace(" ","_"))

# Add specific player
@app.post('/player')
def add_player(player: Player):
    # Add person to app
    app.db.put(player.name.lower().replace(" ","_"), player.model_dump())
    return app.db.get(player.name.lower().replace(" ","_"))

# Delete Player
@app.delete('/player/{player_name}')
def delete_player(player_name: str):
    # Clean string to ensure it is the correct person
    app.db.delete(player_name.lower().replace(" ","_"))
    return {}