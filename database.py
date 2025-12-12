import json
import os

DATA_DIR = "data"
SONG_FILE = os.path.join(DATA_DIR, "songs.json")
USER_FILE = os.path.join(DATA_DIR, "users.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
PLAYLIST_FILE = os.path.join(DATA_DIR, "playlists.json")


def ensure_data_structure():
    """Create necessary folders + files if missing."""
    os.makedirs(DATA_DIR, exist_ok=True)

    defaults = {
        SONG_FILE: [],
        USER_FILE: {},
        HISTORY_FILE: {},
        PLAYLIST_FILE: {}
    }

    for path, default_value in defaults.items():
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump(default_value, f, indent=4)


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# SONGS ----------------------------------------------------

def load_songs():
    return load_json(SONG_FILE)


def save_songs(songs):
    save_json(SONG_FILE, songs)


# USERS -----------------------------------------------------

def load_users():
    return load_json(USER_FILE)


def save_users(data):
    save_json(USER_FILE, data)


# HISTORY ---------------------------------------------------

def load_history():
    return load_json(HISTORY_FILE)


def save_history(data):
    save_json(HISTORY_FILE, data)


# PLAYLISTS -------------------------------------------------

def load_playlists():
    return load_json(PLAYLIST_FILE)


def save_playlists(data):
    save_json(PLAYLIST_FILE, data)
