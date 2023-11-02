from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded" 
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_headers(token):
    return {"Authorization": "Bearer " + token}

def search_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_headers(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("no artist found")
        return None 
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album,single&limit=30"
    headers = get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['items']
    #print(json_result)
    return json_result

def list(thing):
    for i , t in enumerate(thing):
        print(f"{i+1}. {t['name']}")

def get_user_input(token):
    user_input = input("What would you like to do?\n1. Search Artist \n2. Search Album\nQuit\nChoosing: ").lower()
    match user_input:
        case "1":
            get_artist(input("What artist would you like to seach?: "), token)
        case "quit":
            return False
        case _:
            print("unlucky")

def get_artist(user_artist, token):
    result = search_artist(token, user_artist)
    artist_name = result["name"]
    artist_id = result["id"]

    user_input = int(input("Choose one of the following:\n1. Top songs \n2. Albums\nChoosing: "))
    
    if user_input == 1:
        songs = get_songs_by_artist(token, artist_id)
        print(f"Top 10 songs by {artist_name}: \n")
        list(songs)
    elif user_input == 2:
        albums = get_albums_by_artist(token, artist_id)
        print(f"=========\n{artist_name} Albums: \n")
        list(albums)

def main():
    token = get_token()
    
    while True:
        t = get_user_input(token)
        if t == False:
            return


main()