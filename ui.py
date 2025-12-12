import os
import time
import shutil
import random

# Check terminal size for adaptive layout
TERMINAL_WIDTH = shutil.get_terminal_size((80, 20)).columns


# -------------- COLOR SUPPORT -----------------

class COLORS:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"


def color(text, c):
    """Wrap text in color codes."""
    return f"{c}{text}{COLORS.RESET}"


# -------------- CLEAR SCREEN ------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


# -------------- BIG BANNER ---------------------

def banner(text):
    clear()
    width = TERMINAL_WIDTH

    bar = "*" * width
    print(bar)
    print(text.center(width))
    print(bar)
    print()


# -------------- BOX TEXT -----------------------

def box(text):
    text = f" {text} "
    print(f"┌{'─' * len(text)}┐")
    print(f"│{text}│")
    print(f"└{'─' * len(text)}┘")


# -------------- LOADING ANIMATION --------------

def loading(msg="Loading...", duration=1.5):
    print(msg, end="", flush=True)
    for _ in range(8):
        print(".", end="", flush=True)
        time.sleep(duration / 8)
    print()


# -------------- ASCII WAVEFORM VISUALIZER ------

def waveform(intensity=15, length=40):
    """
    Draws a random waveform bar.
    Used during MP3 playback simulation.
    """
    bars = []
    for _ in range(length):
        height = random.randint(1, intensity)
        bars.append("*" * height)
    return " ".join(bars)


def display_waveform(seconds=3):
    """Simulated waveform animation."""
    for _ in range(seconds * 5):  # 5 frames per second
        clear()
        print(waveform())
        time.sleep(0.2)


# -------------- ALBUM COVER TO ASCII -----------

def ascii_cover(path="assets/default_cover.txt"):
    """Reads a pre-made ASCII cover file."""
    try:
        with open(path, "r", encoding="utf8") as f:
            return f.read()
    except FileNotFoundError:
        return "[ NO ALBUM ART AVAILABLE ]"


def show_cover(path="assets/default_cover.txt"):
    """Prints the ASCII cover."""
    print(ascii_cover(path))


# -------------- PROMPT INPUT -------------------

def prompt(text):
    """Styled user input box."""
    print()
    box(text)
    return input("> ")


# -------------- SMALL HELPERS ------------------

def line():
    print("─" * TERMINAL_WIDTH)


def title(text):
    print()
    print(text.center(TERMINAL_WIDTH))
    print()


# -------------- MENU RENDERER -------------------

def menu(title_text, options):
    """
    Render a menu:
    options = ["Login", "Exit", ...]
    Returns selected index (1-based)
    """
    banner(title_text)

    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")

    print()
    choice = input("Enter choice: ")

    if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
        return None
    return int(choice)
