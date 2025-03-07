from pydantic import BaseModel

# What the update Ranking Request Receives
class UpdateRankingRequest(BaseModel):
    item_type: str # "song", "album", or "artist"
    item_id: str
    comparison_id: str
    user_preference: str  # "better" or "worse"


# Ask to add item
class AddItemRequest(BaseModel):
    item_type: str  # "song", "album", or "artist"
    title: str = None # Can be none if it's just finding the artist
    artist: str 

# Find next comparison
class GetComparisonRequest(BaseModel):
    item_type: str # "song", "album", or "artist"
    item_id: str

# Ask for the ranking list
class RankingList(BaseModel):
    item_type: str # "song", "album", or "artist"

# Ask for Recommendation
class RecommendationRequest(BaseModel):
    artist: str
    track: str
