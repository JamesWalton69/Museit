import json
from database import load_playlists, save_playlists
from ui import box, banner


# -------------------------------------------------------------
# MUSIT 5.0 — PLAYLIST ENGINE
# -------------------------------------------------------------


# --------------------- LOAD / SAVE ---------------------------

def get_user_playlists(username):
    data = load_playlists()
    return data.get(username, {})


def save_user_playlists(username, playlists):
    data = load_playlists()
    data[username] = playlists
    save_playlists(data)


# --------------------- BASIC PLAYLIST OPS ---------------------

def create_playlist(username, name):
    playlists = get_user_playlists(username)

    if name in playlists:
        return False, "Playlist already exists."

    playlists[name] = []
    save_user_playlists(username, playlists)
    return True, f"Playlist '{name}' created."


def delete_playlist(username, name):
    playlists = get_user_playlists(username)

    if name not in playlists:
        return False, "Playlist does not exist."

    if name.lower() == "favorites":
        return False, "Cannot delete system playlist 'Favorites'."

    del playlists[name]
    save_user_playlists(username, playlists)
    return True, f"Playlist '{name}' deleted."


def rename_playlist(username, old, new):
    playlists = get_user_playlists(username)

    if old not in playlists:
        return False, "Original playlist not found."

    if new in playlists:
        return False, "New playlist name already exists."

    playlists[new] = playlists[old]
    del playlists[old]
    save_user_playlists(username, playlists)
    return True, f"Renamed '{old}' to '{new}'."


# --------------------- SONG MANAGEMENT ------------------------

def add_to_playlist(username, playlist_name, song_id):
    playlists = get_user_playlists(username)

    if playlist_name not in playlists:
        return False, "Playlist not found."

    if song_id in playlists[playlist_name]:
        return False, "Song already in playlist."

    playlists[playlist_name].append(song_id)
    save_user_playlists(username, playlists)
    return True, "Song added."


def remove_from_playlist(username, playlist_name, song_id):
    playlists = get_user_playlists(username)

    if playlist_name not in playlists:
        return False, "Playlist not found."

    if song_id not in playlists[playlist_name]:
        return False, "Song not in playlist."

    playlists[playlist_name].remove(song_id)
    save_user_playlists(username, playlists)
    return True, "Song removed."


# --------------------- FAVORITES --------------------------------

def add_favorite(username, song_id):
    playlists = get_user_playlists(username)

    if "Favorites" not in playlists:
        playlists["Favorites"] = []

    if song_id not in playlists["Favorites"]:
        playlists["Favorites"].append(song_id)
        save_user_playlists(username, playlists)
        return True, "Added to favorites."

    return False, "Already in favorites."


def remove_favorite(username, song_id):
    playlists = get_user_playlists(username)

    if "Favorites" in playlists and song_id in playlists["Favorites"]:
        playlists["Favorites"].remove(song_id)
        save_user_playlists(username, playlists)
        return True, "Removed from favorites."

    return False, "Not in favorites."


# --------------------- DISPLAY HELPERS ---------------------------

def print_playlists(username, songs):
    playlists = get_user_playlists(username)
    if not playlists:
        box("You have no playlists yet.")
        return

    banner(" YOUR PLAYLISTS ")

    for name, ids in playlists.items():
        print(f"\n{name.upper()}  ({len(ids)} songs)")
        print("-" * 40)

        if not ids:
            print("  [Empty playlist]")
            continue

        for mid in ids:
            song = next((s for s in songs if s["MusicID"] == mid), None)
            if song:
                print(f"  {song['MusicID']}. {song['Title']} - {song['Artist']}")
            else:
                print(f"  {mid} (Unknown song)")

    print("\n")
