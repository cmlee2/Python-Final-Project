# Python-Final-Project
NOTE: YOU NEED TO HAVE THE LAST FM API KEY

Run these lines:

In a separate terminal:
pipenv shell

hypercorn main:app --bind 127.0.0.1:8000


Then run last_fm_frontend.py in main terminal


Project idea #1: 
I want to have a project where users can rate their favorite artists and songs and get music recommendations based on rankings. It would have methods to:
- Have users input their favorite artists, songs, or albums and rate them relative to other artists, songs, or albums
- Have users tag songs based on the mood/vibe
- Utilize the API of last.fm, spotify API, Discog and others to help pull music artists and related tracks
- Create custom playlists based on song groupings and tags
- Create live data visualizations based on genre and tags that display user listening preferences
- Users will be able to see graphical representations of the music they listen to

I will start by researching API functionality. I would find it cool to connect to someone’s Spotify account, but might find connecting difficult. Additionally, I want to see which music API has the most flexibility. Afterwards, I would find a way to create a dynamic ranking system.


# To-Do-List
- By week 4, I want to explore basic webframeworks that will allow me to take user input.
- By week 5, I want to have explored Spotify API and music APIS to see the flexibility of adding them to my webpage.
- By week 6, I will have functionality to take in a user's favorite songs, artist and albums and rate them in relation to others songs, artists and albums. They will also be able to categorize the songs based on a variety of tags, and implement thier own.
- By week 7, I will have my webpage give recommendations for songs, where they can listen and rate to see if those recommendations are accurate.
- By week 8, I will incorporate live data models that will highlight a user's listening habits based on favorites. 
- By week 9, I want to polish the functions of my webpage. Make sure that I test for bugs and ensure the webpage and all of its features are functionable. 