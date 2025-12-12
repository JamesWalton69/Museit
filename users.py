import hashlib
import time
from database import load_users, save_users
from ui import box, banner, prompt


# -------------------------------------------------------------
# MUSIT 5.0 — USER ACCOUNT SYSTEM
# -------------------------------------------------------------


# ---------------- PASSWORD HASHING ----------------------------

def encode_password(password):
    """
    Securely hash a password using SHA256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- USER DATABASE HELPERS -----------------------

def get_users():
    return load_users()


def save_user_db(users):
    save_users(users)


# ---------------- CREATE ACCOUNT ------------------------------

def create_account():
    banner(" CREATE NEW ACCOUNT ")

    users = get_users()
    username = prompt("Choose a username")

    if username in users:
        box("Username already exists.")
        return None

    password = prompt("Choose a password")
    hashed = encode_password(password)

    users[username] = {
        "password": hashed,
        "created": time.time(),
        "is_admin": False,
        "preferences": {},
    }

    save_user_db(users)
    box("Account created successfully!")
    return username


# ---------------- LOGIN SYSTEM --------------------------------

def login():
    banner(" LOGIN ")

    users = get_users()
    username = prompt("Username")

    if username not in users:
        box("User not found.")
        return None

    password = prompt("Password")
    hashed = encode_password(password)

    if hashed != users[username]["password"]:
        box("Incorrect password.")
        return None

    box(f"Welcome back, {username}!")
    return username


# ---------------- ADMIN ACCOUNT BOOSTER ------------------------

def ensure_admin_exists():
    """
    Creates a default admin account if none exists.
    """
    users = get_users()
    if "admin" not in users:
        users["admin"] = {
            "password": encode_password("admin123"),
            "is_admin": True,
            "created": time.time(),
            "preferences": {}
        }
        save_user_db(users)


# ---------------- IS ADMIN? -----------------------------------

def is_admin(username):
    users = get_users()
    if username not in users:
        return False
    return users[username].get("is_admin", False)


# ---------------- CHANGE PASSWORD ------------------------------

def change_password(username):
    users = get_users()
    if username not in users:
        box("User not found.")
        return False

    banner(" CHANGE PASSWORD ")

    old = prompt("Old password")
    if encode_password(old) != users[username]["password"]:
        box("Incorrect old password.")
        return False

    new = prompt("New password")
    users[username]["password"] = encode_password(new)

    save_user_db(users)
    box("Password updated!")
    return True


# ---------------- USER PREFERENCES -----------------------------

def set_preference(username, key, value):
    users = get_users()
    if username not in users:
        return

    users[username]["preferences"][key] = value
    save_user_db(users)


def get_preference(username, key, default=None):
    users = get_users()
    if username not in users:
        return default

    return users[username]["preferences"].get(key, default)
