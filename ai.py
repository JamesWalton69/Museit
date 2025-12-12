import random
import math
import time
from difflib import get_close_matches


# -------------------------------------------------------------
# MUSIT 5.0 — AI Brain
# -------------------------------------------------------------


# -------------------- FUZZY SEARCH ----------------------------

def fuzzy_search(query, songs, cutoff=0.55):
    """
    Fuzzy match song titles or artists.
    Returns list of matching songs.
    """
    titles = {s["Title"]: s for s in songs}
    artists = {s["Artist"]: s for s in songs}

    matches_titles = get_close_matches(query, titles.keys(), cutoff=cutoff)
    matches_artists = get_close_matches(query, artists.keys(), cutoff=cutoff)

    results = []

    for t in matches_titles:
        results.append(titles[t])

    for a in matches_artists:
        results.append(artists[a])

    # remove duplicates while preserving order
    final = []
    seen = set()
    for s in results:
        mid = s["MusicID"]
        if mid not in seen:
            seen.add(mid)
            final.append(s)

    return final



# ------------------ MOOD ENGINE -------------------------------

MOOD_MAP = {
    "Sad":      ("Indie", "Retro"),
    "Chill":    ("Indie", "Pop", "International"),
    "Hype":     ("Phonk", "Pop"),
    "Energetic":("Phonk", "International"),
    "Love":     ("Pop", "Indie"),
}

def recommend_by_mood(mood, songs):
    """
    Recommend based on the chosen mood category.
    """
    mood = mood.capitalize()
    if mood not in MOOD_MAP:
        return []

    preferred = MOOD_MAP[mood]
    return [s for s in songs if s["Genre"] in preferred]



# ------------------ SIMILARITY ENGINE -------------------------

def similarity(songA, songB):
    """
    Computes similarity between two songs (0 to 1).
    Factors: Genre, Artist, Duration
    """
    score = 0

    # genre match
    if songA["Genre"] == songB["Genre"]:
        score += 0.5

    # artist match
    if songA["Artist"] == songB["Artist"]:
        score += 0.3

    # duration similarity
    diff = abs(songA["Duration"] - songB["Duration"])
    score += max(0, 0.2 - diff / 300)

    return score



def similar_songs(target_song, songs, top_n=5):
    """
    Return top N most similar songs.
    """
    scored = []
    for s in songs:
        if s["MusicID"] == target_song["MusicID"]:
            continue
        scored.append((similarity(target_song, s), s))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [s for _, s in scored[:top_n]]



# ------------------ FULL AI WEIGHTED RECOMMENDER --------------

def ai_score(song, history, genre_freq, artist_freq, avg_duration):
    """
    Computes weighted AI score for each song.
    """
    score = 0

    # 1) Genre frequency weight
    score += 5 * genre_freq.get(song["Genre"], 0)

    # 2) Artist frequency weight
    score += 3 * artist_freq.get(song["Artist"], 0)

    # 3) Duration closeness
    score += max(0, 2 - abs(song["Duration"] - avg_duration) / 50)

    # 4) Recency bias (avoid recommending the SAME last song)
    if history and history[-1]["id"] == song["MusicID"]:
        score -= 5

    return score



def recommend_ai(songs, history):
    """
    Full AI recommender using weighted scores.
    """
    if len(history) < 5:
        return None  # AI needs more data

    genre_freq = {}
    artist_freq = {}
    durations = []

    for h in history:
        genre_freq[h["genre"]] = genre_freq.get(h["genre"], 0) + 1
        artist_freq[h["artist"]] = artist_freq.get(h["artist"], 0) + 1
        durations.append(h["duration"])

    avg_duration = sum(durations) / len(durations)

    scored = [(ai_score(s, history, genre_freq, artist_freq, avg_duration), s) for s in songs]
    best_score = max(scored, key=lambda x: x[0])[0]

    best_candidates = [s for sc, s in scored if sc == best_score]

    return random.choice(best_candidates)



# ------------------ AUTO NEXT SONG PREDICTOR ------------------

def predict_next(songs, history):
    """
    Predict the next song based on last played.
    Combines similarity + AI.
    """
    if not history:
        return random.choice(songs)

    last = history[-1]
    last_song = next((s for s in songs if s["MusicID"] == last["id"]), None)

    if not last_song:
        return random.choice(songs)

    # Mix: 60% similar songs, 40% AI recommendation
    similar = similar_songs(last_song, songs)
    ai_result = recommend_ai(songs, history)

    combined = similar + ([ai_result] if ai_result else [])

    combined = [c for c in combined if c]  # remove None

    return random.choice(combined) if combined else random.choice(songs)

