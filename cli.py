import api
import json

def list(thing):
    for i , t in enumerate(thing):
        print(f"{i+1}. {t['name']}")
    print("\n")

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
    result = api.search_artist(token, user_artist)
    artist_name = result["name"]
    artist_id = result["id"]

    while True:
        user_input = input("Choose one of the following:\n1. Top songs \n2. Albums\n3. Appears on\n4. Related Artist\n 9. Back\nChoosing: ").lower()
        if user_input == "1":
            songs = api.get_songs_by_artist(token, artist_id)
            print(f"Top 10 songs by {artist_name}: \n")
            list(songs)
        elif user_input == "2":
            albums = api.get_albums_by_artist(token, artist_id)
            print(f"=========\n{artist_name} Albums: \n")
            list(albums)
        elif user_input == "3":
            appears_on = api.get_appears_on_by_artist(token, artist_id)
            print(f"=========\n{artist_name} appears on: \n")
            for i , t in enumerate(appears_on):
                get_album(t['id'],token, artist_name, t['name'])
        elif user_input == "4":
            related = api.get_related_artists()
        elif user_input == "back":
            break
    

def get_album(album_id, token, artist_name, album_name):
    json_result = api.get_song_from_album(token, album_id, artist_name)
    for i in range(len(json_result)):
        for x in range(len(json_result[i]["artists"])):
            if json_result[i]["artists"][x]["name"] == artist_name: 
                print("\nAlbum: " + album_name + "\nTrack: " + json_result[i]["name"] + "\nArtists: ")
                for j in range(len(json_result[i]["artists"])):
                    print(json_result[i]["artists"][j]["name"]) 

def main():
    token = api.get_token()
    while True:
        if get_user_input(token) == False:
            break

main()