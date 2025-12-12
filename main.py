# -------------------------------------------------------------
# MUSIT 5.0 - GOD EDITION
# main.py - Part 1/9
# System Initialization, Imports, Data Loading
# -------------------------------------------------------------

import time
import random
import os

from ui import (
    banner, box, prompt, menu, clear, title,
    ascii_cover, show_cover, waveform
)

from ai import (
    fuzzy_search, recommend_ai, recommend_by_mood,
    similar_songs, predict_next
)

from audio import (
    play_audio, stop_audio, pause_audio,
    resume_audio, match_mp3
)

from database import (
    ensure_data_structure, load_songs, save_songs,
    load_history, save_history, load_users
)

from playlists import (
    print_playlists, create_playlist, delete_playlist,
    rename_playlist, add_to_playlist, remove_from_playlist,
    add_favorite, remove_favorite, get_user_playlists
)

from users import (
    login, create_account, ensure_admin_exists,
    is_admin, change_password
)

from utils import (
    find_song, find_song_by_title, input_int,
    sort_songs_by_artist, sort_songs_by_title,
    sort_songs_by_duration, hr_song, normalize_mood
)

# -------------------------------------------------------------
# INITIALIZATION
# -------------------------------------------------------------

# ensure /data folder and json files exist
ensure_data_structure()

# ensure admin user exists
ensure_admin_exists()

# Load songs and history from JSON
SONGS = load_songs()
HISTORY = load_history()

# Current session
CURRENT_USER = None  # username string
CURRENT_SONG = None  # last played song dict


def save_all():
    """Save all persistent data."""
    save_songs(SONGS)
    save_history(HISTORY)

# -------------------------------------------------------------
# main.py - Part 2/9
# USER LOGIN + ACCOUNT CREATION FLOW
# -------------------------------------------------------------

def welcome_screen():
    """Show the MUSIT 5.0 welcome animation + menu."""
    banner(" WELCOME TO MUSIT 5.0 - GOD EDITION ")

    while True:
        choice = menu(
            "MAIN MENU",
            ["Login", "Create Account", "Exit"]
        )

        if choice == 1:
            return login_flow()
        elif choice == 2:
            user = create_account()
            if user:
                box("Account created. You can now login.")
        elif choice == 3:
            clear()
            banner(" THANK YOU FOR USING MUSIT 5.0 ")
            exit()
        else:
            box("Invalid choice. Try again.")


def login_flow():
    """Handle user login and return username."""
    global CURRENT_USER

    while True:
        user = login()
        if user:
            CURRENT_USER = user
            box(f"Logged in as: {CURRENT_USER}")
            time.sleep(1)
            return user

        # failed login
        retry = prompt("Login failed. Retry? (y/n)")
        if retry.lower() != "y":
            welcome_screen()


def logout_flow():
    """Logs out the current user and returns to welcome menu."""
    global CURRENT_USER
    CURRENT_USER = None
    banner(" LOGGED OUT ")
    time.sleep(1)
    welcome_screen()
# -------------------------------------------------------------
# main.py - Part 3/9
# USER DASHBOARD MENU
# -------------------------------------------------------------

def user_dashboard():
    """Main user interaction menu."""
    global CURRENT_USER

    while True:
        choice = menu(
            f"USER DASHBOARD - {CURRENT_USER}",
            [
                "Song Library",
                "Search",
                "Play Song",
                "AI Recommendation",
                "Mood-Based Recommendation",
                "Similar Songs to Last Played",
                "Playlists",
                "Favorites",
                "History",
                "Account Settings",
                "Logout"
            ]
        )

        if choice == 1:
            song_library()

        elif choice == 2:
            search_menu()

        elif choice == 3:
            play_song_menu()

        elif choice == 4:
            ai_recommendation_menu()

        elif choice == 5:
            mood_recommendation_menu()

        elif choice == 6:
            similar_song_menu()

        elif choice == 7:
            playlist_menu()

        elif choice == 8:
            favorites_menu()

        elif choice == 9:
            history_menu()

        elif choice == 10:
            account_settings_menu()

        elif choice == 11:
            logout_flow()

        else:
            box("Invalid choice.")

# -------------------------------------------------------------
# main.py - Part 4/9
# SONG LIBRARY + SEARCH SYSTEM
# -------------------------------------------------------------

def print_song_table(song_list):
    """Pretty table for song display."""
    if not song_list:
        box("No songs found.")
        return

    print("\nID │ Title                          │ Artist                │ Genre         │ Dur")
    print("───┼──────────────────────────────┼──────────────────────┼──────────────┼──────")

    for s in song_list:
        print(f"{s['MusicID']:3}│ "
              f"{s['Title'][:28]:28} │ "
              f"{s['Artist'][:20]:20} │ "
              f"{s['Genre'][:12]:12} │ "
              f"{s['Duration']:4}s")

    print()


# ---------------- SONG LIBRARY MENU -----------------------------

def song_library():
    """Display and sort the full list of songs."""
    global SONGS

    while True:
        choice = menu(
            "SONG LIBRARY",
            [
                "View All Songs",
                "Sort by Title",
                "Sort by Artist",
                "Sort by Duration",
                "Back"
            ]
        )

        if choice == 1:
            print_song_table(SONGS)

        elif choice == 2:
            print_song_table(sort_songs_by_title(SONGS))

        elif choice == 3:
            print_song_table(sort_songs_by_artist(SONGS))

        elif choice == 4:
            print_song_table(sort_songs_by_duration(SONGS))

        elif choice == 5:
            return

        else:
            box("Invalid choice.")


# ---------------- SEARCH MENU -----------------------------------

def search_menu():
    global SONGS

    while True:
        choice = menu(
            "SEARCH",
            [
                "Search by ID",
                "Search by Title",
                "Search by Artist",
                "Search by Genre",
                "Fuzzy Search (Smart)",
                "Back"
            ]
        )

        if choice == 1:
            sid = input_int("Enter Music ID: ")
            song = find_song(SONGS, sid)
            print_song_table([song] if song else [])

        elif choice == 2:
            title_text = prompt("Enter Title")
            song = find_song_by_title(SONGS, title_text)
            print_song_table([song] if song else [])

        elif choice == 3:
            artist = prompt("Enter Artist").lower()
            results = [s for s in SONGS if artist in s["Artist"].lower()]
            print_song_table(results)

        elif choice == 4:
            genre = prompt("Enter Genre").lower()
            results = [s for s in SONGS if genre in s["Genre"].lower()]
            print_song_table(results)

        elif choice == 5:
            query = prompt("Search anything")
            results = fuzzy_search(query, SONGS)
            print_song_table(results)

        elif choice == 6:
            return

        else:
            box("Invalid option.")

# -------------------------------------------------------------
# main.py - Part 5/9
# PLAY SONG + AUDIO CONTROLS + HISTORY LOGGING
# -------------------------------------------------------------

def log_play(song):
    """Store song play into HISTORY JSON."""
    global HISTORY

    entry = {
        "id": song["MusicID"],
        "title": song["Title"],
        "artist": song["Artist"],
        "genre": song["Genre"],
        "duration": song["Duration"],
        "timestamp": time.time(),
        "user": CURRENT_USER
    }

    # Append to history
    if CURRENT_USER not in HISTORY:
        HISTORY[CURRENT_USER] = []

    HISTORY[CURRENT_USER].append(entry)
    save_history(HISTORY)


# ------------------- PLAY SONG MENU ----------------------------

CURRENT_SONG = None  # last played song object
AUDIO_PAUSED = False


def play_song_menu():
    """Select a song by ID and play it."""
    global CURRENT_SONG, AUDIO_PAUSED

    sid = input_int("Enter Music ID: ")
    if sid is None:
        return

    song = find_song(SONGS, sid)
    if not song:
        box("Song not found.")
        return

    # Save last played
    CURRENT_SONG = song

    # Log the play
    log_play(song)

    # Try to find corresponding MP3 file
    mp3_file = match_mp3(song["Title"])
    cover_path = f"assets/{song['Genre'].lower()}.txt"  # optional genre-based covers

    # If no MP3, still show visual playback
    if mp3_file:
        play_audio(mp3_file, duration=song["Duration"], cover_path=cover_path)
    else:
        # Fallback: just simulate waveform
        banner(f" PLAYING - {song['Title']} ")
        show_cover()
        print(f"\nArtist: {song['Artist']}")
        print(f"Genre:  {song['Genre']}")
        print(f"Duration: {song['Duration']} sec")
        print("\nNo MP3 file found → Showing waveform only.\n")
        time.sleep(1.5)

        # Fake waveform playback
        for _ in range(10):
            print(waveform(10, 30))
            time.sleep(0.15)

    # After song ends → ask user
    post_play_options()


# ------------------- AFTER-PLAY OPTIONS -------------------------

def post_play_options():
    """After finishing a song playback, ask user what to do next."""
    global CURRENT_SONG, AUDIO_PAUSED

    while True:
        choice = menu(
            "AUDIO OPTIONS",
            [
                "Pause",
                "Resume",
                "Stop",
                "Play Similar Song",
                "AI Auto-Recommended Next Song",
                "Back"
            ]
        )

        if choice == 1:   # pause
            pause_audio()
            AUDIO_PAUSED = True
            box("Paused.")

        elif choice == 2: # resume
            if AUDIO_PAUSED:
                resume_audio()
                AUDIO_PAUSED = False
                box("Resumed.")
            else:
                box("Audio is not paused.")

        elif choice == 3: # stop
            stop_audio()
            box("Stopped.")
            return

        elif choice == 4: # similar song
            if CURRENT_SONG:
                similar = similar_songs(CURRENT_SONG, SONGS, top_n=3)
                if similar:
                    print_song_table(similar)
                    sid = input_int("Play which song ID?")
                    if sid:
                        play_song_menu()
                else:
                    box("No similar songs found.")

        elif choice == 5: # AI autoplay
            if CURRENT_USER in HISTORY:
                next_song = predict_next(SONGS, HISTORY[CURRENT_USER])
                if next_song:
                    box("Next song (AI Auto-play):")
                    print_song_table([next_song])
                    time.sleep(1)
                    # autoplay
                    log_play(next_song)
                    mp3_file = match_mp3(next_song["Title"])
                    if mp3_file:
                        play_audio(mp3_file, duration=next_song["Duration"])
                    else:
                        box("MP3 missing → waveform simulation only.")
                        for _ in range(10):
                            print(waveform(10, 30))
                            time.sleep(0.15)
                else:
                    box("AI could not determine a next song.")
            else:
                box("No history found.")

        elif choice == 6:
            return

        else:
            box("Invalid choice.")

# -------------------------------------------------------------
# main.py - Part 6/9
# AI RECOMMENDATION + MOOD ENGINE + SIMILAR SONGS
# -------------------------------------------------------------

def ai_recommendation_menu():
    """AI recommendation based on listening history + AI weights."""
    global CURRENT_USER

    banner(" AI RECOMMENDATION ")

    if CURRENT_USER not in HISTORY or len(HISTORY[CURRENT_USER]) < 5:
        box("Listen to at least 5 songs first.")
        return

    recommended = recommend_ai(SONGS, HISTORY[CURRENT_USER])

    if not recommended:
        box("AI could not find a good recommendation.")
        return

    box("AI thinks you'll like this:")
    print_song_table([recommended])

    # Ask to play
    play = prompt("Play this song? (y/n)").lower()
    if play == "y":
        log_play(recommended)
        mp3 = match_mp3(recommended["Title"])
        cover = f"assets/{recommended['Genre'].lower()}.txt"
        play_audio(mp3, duration=recommended["Duration"], cover_path=cover) if mp3 \
            else box("MP3 missing → waveform only.")
    else:
        box("Returning to AI menu.")


# ------------------- MOOD RECOMMENDATION -----------------------

def mood_recommendation_menu():
    global CURRENT_USER

    banner(" MOOD-BASED RECOMMENDATION ")

    mood = prompt("Enter mood (sad, chill, hype, energetic, love):")
    mood = normalize_mood(mood)

    results = recommend_by_mood(mood, SONGS)

    if not results:
        box("No songs match this mood.")
        return

    print_song_table(results[:10])

    play = prompt("Play a song from these? Enter ID or 'n'")

    if play.lower() == "n":
        return

    try:
        sid = int(play)
        song = find_song(SONGS, sid)
        if song:
            log_play(song)
            mp3 = match_mp3(song["Title"])
            cover = f"assets/{song['Genre'].lower()}.txt"
            play_audio(mp3, duration=song["Duration"], cover_path=cover) if mp3 \
                else box("MP3 missing → waveform only.")
        else:
            box("Invalid ID.")
    except:
        box("Invalid input.")


# ------------------- SIMILAR SONGS MENU ------------------------

def similar_song_menu():
    """Find songs similar to the last played track."""
    global CURRENT_SONG

    if not CURRENT_SONG:
        box("You haven't played any song yet.")
        return

    banner(f" SIMILAR SONGS TO: {CURRENT_SONG['Title']} ")

    results = similar_songs(CURRENT_SONG, SONGS, top_n=5)

    if not results:
        box("No similar songs found.")
        return

    print_song_table(results)

    # Play one?
    sid = prompt("Enter a song ID to play or 'n' to cancel:")
    if sid.lower() == "n":
        return

    try:
        sid = int(sid)
        song = find_song(SONGS, sid)
        if song:
            log_play(song)
            mp3 = match_mp3(song["Title"])
            cover = f"assets/{song['Genre'].lower()}.txt"
            play_audio(mp3, duration=song["Duration"], cover_path=cover) if mp3 \
                else box("MP3 missing → waveform only.")
        else:
            box("Song not found.")
    except:
        box("Invalid input.")

# -------------------------------------------------------------
# main.py - Part 7/9
# PLAYLIST SYSTEM + FAVORITES SYSTEM
# -------------------------------------------------------------

def playlist_menu():
    """Main playlist interaction panel."""
    global CURRENT_USER

    while True:
        choice = menu(
            "PLAYLISTS",
            [
                "View Playlists",
                "Create Playlist",
                "Add Song to Playlist",
                "Remove Song from Playlist",
                "Rename Playlist",
                "Delete Playlist",
                "Play from Playlist",
                "Back"
            ]
        )

        if choice == 1:
            print_playlists(CURRENT_USER, SONGS)

        elif choice == 2:
            name = prompt("Enter playlist name")
            ok, msg = create_playlist(CURRENT_USER, name)
            box(msg)

        elif choice == 3:
            name = prompt("Enter playlist name")
            sid = input_int("Enter song ID")
            ok, msg = add_to_playlist(CURRENT_USER, name, sid)
            box(msg)

        elif choice == 4:
            name = prompt("Enter playlist name")
            sid = input_int("Enter song ID")
            ok, msg = remove_from_playlist(CURRENT_USER, name, sid)
            box(msg)

        elif choice == 5:
            old = prompt("Old playlist name")
            new = prompt("New playlist name")
            ok, msg = rename_playlist(CURRENT_USER, old, new)
            box(msg)

        elif choice == 6:
            name = prompt("Enter playlist name")
            ok, msg = delete_playlist(CURRENT_USER, name)
            box(msg)

        elif choice == 7:
            play_from_playlist()

        elif choice == 8:
            return

        else:
            box("Invalid choice.")


# --------------- PLAY FROM PLAYLIST ----------------------------

def play_from_playlist():
    global CURRENT_USER, CURRENT_SONG

    playlists = get_user_playlists(CURRENT_USER)
    if not playlists:
        box("You have no playlists.")
        return

    name = prompt("Enter playlist name")
    if name not in playlists:
        box("Playlist not found.")
        return

    if not playlists[name]:
        box("This playlist is empty.")
        return

    # Show playlist songs
    songs_in_pl = [find_song(SONGS, sid) for sid in playlists[name] if find_song(SONGS, sid)]

    print_song_table(songs_in_pl)

    sid = input_int("Enter ID to play:")
    song = find_song(SONGS, sid)

    if song:
        CURRENT_SONG = song
        log_play(song)

        mp3 = match_mp3(song["Title"])
        cover = f"assets/{song['Genre'].lower()}.txt"

        play_audio(mp3, duration=song["Duration"], cover_path=cover) if mp3 \
            else box("MP3 missing → waveform only.")
    else:
        box("Song not found.")


# -------------------------------------------------------------
# FAVORITES SYSTEM
# -------------------------------------------------------------

def favorites_menu():
    global CURRENT_USER

    while True:
        choice = menu(
            "FAVORITES",
            [
                "View Favorites",
                "Add Song to Favorites",
                "Remove Song from Favorites",
                "Play from Favorites",
                "Back"
            ]
        )

        if choice == 1:
            # Show playlist named "Favorites"
            playlists = get_user_playlists(CURRENT_USER)
            fav = playlists.get("Favorites", [])
            songs_in_fav = [find_song(SONGS, sid) for sid in fav]
            print_song_table(songs_in_fav)

        elif choice == 2:
            sid = input_int("Enter song ID")
            ok, msg = add_favorite(CURRENT_USER, sid)
            box(msg)

        elif choice == 3:
            sid = input_int("Enter song ID")
            ok, msg = remove_favorite(CURRENT_USER, sid)
            box(msg)

        elif choice == 4:
            play_from_playlist_favorites()

        elif choice == 5:
            return

        else:
            box("Invalid choice.")


# --------------- PLAY A SONG FROM FAVORITES ---------------------

def play_from_playlist_favorites():
    global CURRENT_USER, CURRENT_SONG

    playlists = get_user_playlists(CURRENT_USER)

    fav = playlists.get("Favorites", [])
    if not fav:
        box("Favorites is empty.")
        return

    songs_in_fav = [find_song(SONGS, sid) for sid in fav if find_song(SONGS, sid)]
    print_song_table(songs_in_fav)

    sid = input_int("Enter ID to play:")
    song = find_song(SONGS, sid)

    if song:
        CURRENT_SONG = song
        log_play(song)
        mp3 = match_mp3(song["Title"])
        cover = f"assets/{song['Genre'].lower()}.txt"
        play_audio(mp3, duration=song["Duration"], cover_path=cover) if mp3 \
            else box("MP3 missing → waveform only.")
    else:
        box("Song not found.")

# -------------------------------------------------------------
# main.py - Part 8/9
# HISTORY PANEL + ACCOUNT SETTINGS
# -------------------------------------------------------------

def history_menu():
    """Show the user’s listening history."""
    global CURRENT_USER, HISTORY

    banner(" LISTENING HISTORY ")

    if CURRENT_USER not in HISTORY or len(HISTORY[CURRENT_USER]) == 0:
        box("You have not listened to any songs yet.")
        return

    history_list = HISTORY[CURRENT_USER]

    # Table header
    print("\nID │ Title                          │ Artist                │ Genre         │ When")
    print("───┼──────────────────────────────┼──────────────────────┼──────────────┼────────────")

    for h in history_list:
        timestamp = time.strftime("%d-%b %H:%M", time.localtime(h["timestamp"]))
        print(f"{h['id']:3}│ "
              f"{h['title'][:28]:28} │ "
              f"{h['artist'][:20]:20} │ "
              f"{h['genre'][:12]:12} │ "
              f"{timestamp}")

    print()

    # submenu
    choice = menu(
        "HISTORY OPTIONS",
        [
            "Play a Song Again",
            "Clear History",
            "Back"
        ]
    )

    if choice == 1:
        sid = input_int("Enter ID to replay:")
        song = find_song(SONGS, sid)
        if song:
            log_play(song)
            mp3 = match_mp3(song["Title"])
            cover = f"assets/{song['Genre'].lower()}.txt"
            play_audio(mp3, duration=song["Duration"], cover_path=cover) if mp3 \
                else box("MP3 missing → waveform only.")
        else:
            box("Song not found.")

    elif choice == 2:
        clear_history()

    elif choice == 3:
        return


# -------------------- CLEAR HISTORY ---------------------------

def clear_history():
    """Clear only the current user's history."""
    global HISTORY, CURRENT_USER

    confirm = prompt("Are you sure? Type 'yes' to confirm:")
    if confirm.lower() != "yes":
        box("Cancelled.")
        return

    HISTORY[CURRENT_USER] = []
    save_history(HISTORY)
    box("History cleared.")


# -------------------------------------------------------------
# ACCOUNT SETTINGS
# -------------------------------------------------------------

def account_settings_menu():
    global CURRENT_USER

    while True:
        choice = menu(
            f"ACCOUNT SETTINGS - {CURRENT_USER}",
            [
                "Change Password",
                "View User Info",
                "Back"
            ]
        )

        if choice == 1:
            change_password(CURRENT_USER)

        elif choice == 2:
            view_user_info()

        elif choice == 3:
            return

        else:
            box("Invalid choice.")


def view_user_info():
    """Display detailed info about current user."""
    banner(" USER INFORMATION ")

    users = load_users()
    user = users.get(CURRENT_USER, None)

    if not user:
        box("User not found.")
        return

    print(f"Username:   {CURRENT_USER}")
    print(f"Created On: {time.strftime('%d %B %Y %H:%M', time.localtime(user['created']))}")
    print(f"Admin:      {user.get('is_admin', False)}")
    print(f"Preferences: {user.get('preferences', {})}")
    print()

    prompt("Press Enter to continue...")

# -------------------------------------------------------------
# main.py - Part 9/9
# MAIN APPLICATION LOOP - ENTRY POINT
# -------------------------------------------------------------

def main():
    clear()
    banner(" MUSIT 5.0 - GOD EDITION ")

    # Start at welcome screen
    welcome_screen()

    # Once logged in → go to dashboard
    while True:
        if CURRENT_USER:
            user_dashboard()
        else:
            welcome_screen()


# -------------------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        banner(" EXITING MUSIT 5.0 ")
        save_all()
        print("\nGoodbye!\n")
        time.sleep(1)

