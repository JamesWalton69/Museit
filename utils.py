import random
import math
from ui import box


# -------------------------------------------------------------
# MUSIT 5.0 — UTILITY MODULE
# -------------------------------------------------------------


# -------------------- TIME HELPERS ----------------------------

def format_time(seconds):
    """
    Convert 180 -> "3:00"
    """
    seconds = int(seconds)
    m = seconds // 60
    s = seconds % 60
    return f"{m}:{s:02d}"


# -------------------- SAFE INPUT -------------------------------

def input_int(prompt_text, default=None):
    """
    Get integer input safely.
    Returns default on invalid input.
    """
    try:
        return int(input(prompt_text))
    except:
        if default is not None:
            return default
        box("Invalid number.")
        return None


# ------------------- SONG LOOKUP -------------------------------

def find_song(songs, song_id):
    """
    Find song by ID.
    """
    for s in songs:
        if s["MusicID"] == song_id:
            return s
    return None


def find_song_by_title(songs, title):
    """
    Case-insensitive title search.
    """
    title = title.lower()
    for s in songs:
        if s["Title"].lower() == title:
            return s
    return None


# -------------------- RANDOM UTILITIES --------------------------

def random_choice(lst):
    """
    Safe random choice: returns None if list empty.
    """
    return random.choice(lst) if lst else None


# -------------------- NUMERIC HELPERS ---------------------------

def clamp(x, a, b):
    """
    Clamp x to range [a, b].
    """
    return max(a, min(b, x))


def lerp(a, b, t):
    """
    Linear interpolation.
    """
    return a + (b - a) * t


# -------------------- SORTING HELPERS ---------------------------

def sort_songs_by_title(songs):
    return sorted(songs, key=lambda s: s["Title"])


def sort_songs_by_duration(songs):
    return sorted(songs, key=lambda s: s["Duration"])


def sort_songs_by_artist(songs):
    return sorted(songs, key=lambda s: s["Artist"])


# -------------------- MOOD NORMALIZATION -------------------------

def normalize_mood(mood: str):
    mood = mood.strip().lower()
    synonyms = {
        "sad": "Sad",
        "depressed": "Sad",
        "down": "Sad",

        "chill": "Chill",
        "relaxed": "Chill",
        "calm": "Chill",

        "hype": "Hype",
        "party": "Hype",
        "energetic": "Energetic",
        "workout": "Energetic",

        "love": "Love",
        "romantic": "Love"
    }

    return synonyms.get(mood, mood.capitalize())


# -------------------- HUMAN READABLE ----------------------------

def hr_duration(seconds):
    """
    Convert 185 -> "185 sec (3:05)"
    """
    return f"{seconds} sec ({format_time(seconds)})"


def hr_song(song):
    """
    Return human-readable song description.
    """
    return f"{song['Title']} - {song['Artist']} [{song['Genre']}] {format_time(song['Duration'])}"


# -------------------- SAFE EXECUTION ----------------------------

def safe_run(func, *args, **kwargs):
    """
    Execute a function and catch exceptions silently.
    Useful for risky actions.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        box(f"Error: {e}")
        return None
