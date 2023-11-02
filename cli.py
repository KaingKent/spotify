import api

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
    result = api.search_artist(token, user_artist)
    artist_name = result["name"]
    artist_id = result["id"]

    user_input = int(input("Choose one of the following:\n1. Top songs \n2. Albums\nChoosing: "))
    
    if user_input == 1:
        songs = api.get_songs_by_artist(token, artist_id)
        print(f"Top 10 songs by {artist_name}: \n")
        list(songs)
    elif user_input == 2:
        albums = api.get_albums_by_artist(token, artist_id)
        print(f"=========\n{artist_name} Albums: \n")
        list(albums)

def main():
    token = api.get_token()
    
    while True:
        t = get_user_input(token)
        if t == False:
            return


main()