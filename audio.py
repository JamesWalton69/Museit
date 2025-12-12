import os
import time
import pygame # type: ignore
from ui import clear, waveform, ascii_cover, show_cover, display_waveform


# --------------------------------------------------------------
# MUSIT 5.0 — AUDIO ENGINE
# --------------------------------------------------------------

MP3_DIR = "mp3"


# ---------------------- INITIALIZE MIXER ----------------------

pygame.mixer.init()


# ---------------------- LOAD MP3 FILE -------------------------

def load_mp3(filename):
    """
    Loads and prepares an MP3 file for playback.
    """
    path = os.path.join(MP3_DIR, filename)
    if not os.path.exists(path):
        print(f"[ERROR] MP3 file not found: {path}")
        return False

    pygame.mixer.music.load(path)
    return True


# ---------------------- PLAY SONG -----------------------------

def play_audio(filename, duration=None, volume=0.7, cover_path=None):
    """
    Plays an MP3 file with visual waveform.
    duration: optional override for progress bar (in seconds)
    """

    if not load_mp3(filename):
        return

    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()

    clear()
    print(ascii_cover(cover_path) if cover_path else ascii_cover())

    # If duration not provided, try reading from pygame (not very accurate)
    if duration is None:
        duration = 180  # fallback default

    print(f"\nPlaying: {filename}")
    print(f"Duration: {duration} sec")
    print("Press CTRL+C to stop.\n")

    start = time.time()

    try:
        while pygame.mixer.music.get_busy():
            elapsed = time.time() - start
            progress = min(elapsed / duration, 1)

            # Progress Bar
            bar_len = 40
            filled = int(bar_len * progress)
            bar = "█" * filled + "-" * (bar_len - filled)

            clear()
            print(ascii_cover(cover_path) if cover_path else ascii_cover())
            print(f"\n[{bar}] {int(progress*100)}%  {int(elapsed)}s / {duration}s\n")

            # Waveform animation
            print(waveform(10, 30))

            time.sleep(0.15)

    except KeyboardInterrupt:
        stop_audio()


# ---------------------- PAUSE / RESUME / STOP ----------------

def pause_audio():
    pygame.mixer.music.pause()


def resume_audio():
    pygame.mixer.music.unpause()


def stop_audio():
    pygame.mixer.music.stop()


# ---------------------- VOLUME CONTROL ------------------------

def set_volume(level):
    """
    level: 0.0 to 1.0
    """
    pygame.mixer.music.set_volume(level)


# ---------------------- SCAN MP3 DIRECTORY --------------------

def available_mp3():
    """
    Returns list of MP3 files in /mp3/.
    """
    if not os.path.exists(MP3_DIR):
        return []

    return [f for f in os.listdir(MP3_DIR) if f.lower().endswith(".mp3")]


# ---------------------- MATCH MP3 TO SONG TITLE ---------------

def match_mp3(song_title):
    """
    Best-effort match: try to find an MP3 file with similar name.
    """
    files = available_mp3()
    low_title = song_title.lower().replace(" ", "")

    for f in files:
        if low_title in f.lower().replace(" ", ""):
            return f

    return None
