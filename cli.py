import api

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

    user_input = int(input("Choose one of the following:\n1. Top songs \n2. Albums\n3. Appears on\nChoosing: "))
    
    if user_input == 1:
        songs = api.get_songs_by_artist(token, artist_id)
        print(f"Top 10 songs by {artist_name}: \n")
        list(songs)
    elif user_input == 2:
        albums = api.get_albums_by_artist(token, artist_id)
        print(f"=========\n{artist_name} Albums: \n")
        list(albums)
    elif user_input == 3:
        appears_on = api.get_appears_on_by_artist(token, artist_id)
        print(f"=========\n{artist_name} appears on: \n")
        #albums = get_album(appears_on,token)

        for i , t in enumerate(appears_on):
            get_album(t['name'],token)
        #list(appears_on)

def get_album(user_album, token):
    #print("")
    result = api.search_album(token, user_album)
    album_name = result["name"]
    album_id = result["id"]
    print(album_id)
    api.get_song_from_album(token, album_id)

def main():
    token = api.get_token()
    while True:
        t = get_user_input(token)
        if t == False:
            return


main()