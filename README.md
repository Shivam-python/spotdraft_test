# spotdraft_test

# to run the project : 
1. Create virtual env using : python -m venv spot
2. Install dependencies : pip install -r requirements.txt
3. Admin creds : username = sam, password = 1234
4. To create new user run : python manage.py createsuperuser and follow the instructions (Add username, passowrd etc)
4. Finally use command to run the server : python manage.py runserver

# Postman collection can be imported using the link below, documentation added wherever required. :
https://www.getpostman.com/collections/c746a20eaccc56ad2cc8


# Requirements : 

"""
The code should be clean, have tests, & be well documented.
Using backend framework (Preferred- Django), make a simple Favourites app that exposes REST APIs for Star Wars data.

The app:
- MUST load planets and movies from the JSON API provided by https://swapi.dev/

- MUST expose list APIs - one for movies and one for planets
- MUST expose APIs to add a movie and planet as a favourite
- The favourite API should also allow setting a custom title/name to the movie/planet
- The favourites must be stored per user (user_id can simply be passed in the request, there is no need for authentication)
- The planet list API must return the name, created, updated, url and is_favourite fields
- The movies list API must return the title, release_date, created, updated, url and is_favourite fields
- If the custom name is set by the user then that should be returned as the name/title and it should be used when searching
- Additionally the list APIs must support searching by title/name

In addition to the functionality listed above, please add features that you think might be useful.

Added Favourite Update and Delete API.
"""
