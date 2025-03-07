# Import dependencies
from fastapi import FastAPI
from database import DataBase
from models import UpdateRankingRequest, AddItemRequest, GetComparisonRequest, RankingList, RecommendationRequest
from contextlib import asynccontextmanager

# To ensure that database is loaded and saved when we end Fast API
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event to initialize and cleanup resources."""
    print("Starting FastAPI... Initializing database.")
    # Start Database
    app.db = DataBase() 
    # Wait until database ends
    yield  
    print("Shutting down FastAPI...")

# Start FastAPI
app = FastAPI(lifespan=lifespan)

# Add song, artist, or album
@app.post("/add_item/")
def add_item(request: AddItemRequest):
    """
    Add a song, album, or artist and return the first comparison item.
    """
    # Get result
    result = app.db.add_item(request.item_type, request.title, request.artist)

    # If result is not there, send error message
    if not result:
        return {"error": "Item not found or failed to fetch data"}

    # Return Result
    return result

# Update rankings
@app.post("/update_ranking/")
def update_ranking(request: UpdateRankingRequest):
    """
    Update ranking based on user input and return the next comparison.
    """
    # Get next comparison based on update ranking call
    next_comparison = app.db.update_ranking(
        request.item_type, request.item_id, request.comparison_id, request.user_preference
    )

    # See if there is a next comparison
    if next_comparison:
        return {
            "next_comparison": next_comparison,
            "next_comparison_name": app.db._data[request.item_type].get(next_comparison, {}).get(
                "song_name" if request.item_type == "song" else "album_name" if request.item_type == "album" else "artist_name",
                "Unknown"
            )
        }
    
    # Return message if done
    else:
        return {"message": "Ranking complete"} 

# Fetch next comparison
@app.post("/get_next_comparison/")
def get_next_comparison(request: GetComparisonRequest):
    """
    Fetch the next item for ranking comparison.
    """
    # Get new ID
    comparison_id = app.db.get_next_comparison(request.item_type, request.item_id)

    # Get the name of the new song, artist, or album
    if comparison_id:
        # Fetch the comparison item's name
        comparison_name = app.db._data[request.item_type].get(comparison_id, {}).get(
            "song_name" if request.item_type == "song" else "album_name" if request.item_type == "album" else "artist_name",
            "Unknown"
        )
        # Return the comparison data
        return {
            "compare_with": comparison_id,
            "compare_with_name": comparison_name
        }

    # Ensure "compare_with" is included 
    return {
        "message": "Ranking complete",
        "compare_with": None,
        "compare_with_name": None
    }

# Get for the new rankings
@app.post('/ranked/')
def get_rankings(request: RankingList):
    '''Return the updated rankings'''
    return app.db.display_rankings(request.item_type)

@app.post('/recommendations/')
def get_recommendations(request: RecommendationRequest):
    '''Return recommendations'''
    return app.db.get_recommendations(track=request.track, artist=request.artist)
