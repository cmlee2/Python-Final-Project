import requests
import json

# This is my base URL, change if not working
BASE_URL = "http://127.0.0.1:8000"  

def add_item():
    '''Prompt user for item details and send request to add a song, album, or artist.'''
    # Ask for item type, title and artist
    item_type = input("Enter type (song/album/artist): ").strip().lower()
    if item_type not in ['song','album', 'artist']:
        raise NameError('Enter a valid format (song, album, artist)')
    title = input("Enter title: ").strip() if item_type != "artist" else ''
    artist = input("Enter artist:").strip()


    # Format of the Base model I am sending
    payload = {"item_type": item_type, "title": title, "artist": artist}
    
    # Post to my API
    response = requests.post(f"{BASE_URL}/add_item/", json=payload)


    # Save response
    data = response.json()
    

    # See if you can make a comparison
    try:
        # Get item_id, comparison id and names from file
        item_id = data.get("item_id")
        item_name = data.get("name", "Unknown Item")
        compare_with = data.get("compare_with")
        compare_with_name = data.get("compare_with_name", "Unknown")

        print(f"\n {item_name} added successfully!")

        # If you can compare, say what the comparison is
        if compare_with:
            print(f"Compare with: {compare_with_name}")
            return item_type, item_id, item_name, compare_with  
    
    # Return None if no need to add
    except:
        print("Added to Database (No Ranking needed)")
        return None, None, None, None
    
def update_ranking(item_type, item_id, item_name):
    """Loop through ranking comparisons until the item is placed."""
    # Run a while look to keep comparing
    while True:
        # Call to API to run the next comparison
        response = requests.post(f"{BASE_URL}/get_next_comparison/", json={"item_type": item_type, "item_id": item_id})
        data = response.json()


        # If you can't find anything to compare with, ranking is done
        if "compare_with" not in data or not data["compare_with"]:
            print("\n Ranking is complete!")

        # Get comparison id and name
        comparison_id = data["compare_with"]
        comparison_name = data.get("compare_with_name", "Unknown Comparison")

        # See which user prefers
        print(f"\n Compare '{item_name}' with '{comparison_name}'")
        user_choice = input("Is the new item (better/worse) this one? ").strip().lower()

        # Confirm that user submitted right data
        if user_choice not in ["better", "worse"]:
            print("Invalid input! Please type 'better' or 'worse'.")
            continue

        # Send payload in format provided
        payload = {
            "item_type": item_type,
            "item_id": item_id,
            "comparison_id": comparison_id,
            "user_preference": user_choice
        }
        # Send Post Request to get Data
        response = requests.post(f"{BASE_URL}/update_ranking/", json=payload)
        data = response.json()

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("There was an error")
            return
        
        if "message" in data and data["message"] == "Ranking complete":
            print("\n Ranking Completed")
            break  # End


def return_rankings():
    """Prompt user for item details and return rankings."""
    # Ask what ranking they want to see
    item_type = input("Enter type (song/album/artist): ").strip().lower()

    if item_type not in ['song','album', 'artist']:
        raise NameError('Enter a valid format (song, album, artist)')
    # Send payload
    payload = {"item_type": item_type}
    
    # Pull Response
    response = requests.post(f"{BASE_URL}/ranked/", json=payload)


    # Save ranking data
    rankings = response.json()

    # If ranking is empty
    if not rankings:
        print('No rankings found, please try entering more data')

    # Loop through data and print rankings
    for index, rank in enumerate(rankings, start = 1):
        if item_type == 'song':
            print(f"{index}: {rank['song_name']} - {rank['artist']} ({rank['album']})")
        elif item_type == 'album':
            print(f"{index}: {rank['album_name']} - {rank['artist']}")
        elif item_type == 'artist':
            print(f"{index}: {rank['artist_name']}")
    return 

def return_recommendations():
    """Prompt user for item details and send request to recommend a song"""
    # Ask for song title and artist for recs
    title = input("Enter song title for recommendations: ").strip()
    artist = input("Enter artist: ")

    # Send payload
    payload = { "track": title, "artist": artist}
    
    # Post Request
    response = requests.post(f"{BASE_URL}/recommendations/", json=payload)


    # If response is empty say it didn't work
    if not response.json():
        print ('No Recommendations Found, Please try again')
        return

    # Return Recommendations
    recommendations = response.json()
    for recs in recommendations:
        print(f"artist: {recs[0]}, song: {recs[1]}")
        
    return 

    
def main():
    # User input and command line prompt
    print("\n Welcome to Song/Album/Artist Ranking!")
    while True:
        # Print options
        print("\nOptions:")
        print("1  Add a new item (song/album/artist)")
        print("2  Return Rankings (song/album/artist)")
        print("3  Return Recommendations (for songs)")
        print("4  Exit")

        # Get user input
        choice = input("\nSelect an option: ").strip()

        # Run function based on user input
        if choice == "1":
            item_type, item_id, item_name, compare_with = add_item()
            if item_id:
                update_ranking(item_type, item_id,item_name)
        elif choice == "2":
            return_rankings()
        elif choice == "3":
            return_recommendations()
        elif choice == "4":
            print("Ending Session")
            break
        else:
            print("Invalid choice! Please enter 1, 2, 3 or 4.")

if __name__ == "__main__":
    main()
