# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# 📅 Copyright © 2022 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by ItzShukla
# -----------------------------------------------

import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# Load environment variables
load_dotenv()

# Required credentials
def _int_env(name: str, default: int) -> int:
    value = getenv(name)
    if value in (None, ""):
        return default
    try:
        return int(value)
    except ValueError:
        return default


API_ID = _int_env("API_ID", 0)
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN")

# Bot and owner info
OWNER_USERNAME = getenv("OWNER_USERNAME", "ik_ares")
BOT_USERNAME = getenv("BOT_USERNAME", "Rose_x_musicbot")
BOT_NAME = getenv("BOT_NAME", "˹Rᴏꜱᴇ ꭙ ᴍᴜꜱɪᴄ 🕊")
ASSUSERNAME = getenv("ASSUSERNAME", "")

# AI Chatbot
GROQ_API_KEY = getenv("GROQ_API_KEY", None)

# Google / YouTube Data API key (used for /tg and /spg search commands)
YOUTUBE_API_KEY = getenv("YOUTUBE_API_KEY", "")
YOUTUBE_COOKIES_FILE = getenv("YOUTUBE_COOKIES_FILE", "")


# MongoDB
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# Limits and IDs
DURATION_LIMIT_MIN = _int_env("DURATION_LIMIT", 17000)
LOGGER_ID = _int_env("LOGGER_ID", 0)
OWNER_ID = _int_env("OWNER_ID", 6670240589)

# Heroku
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# Git
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/samxusa/Tg_music")
MINIAPP_URL = getenv("MINIAPP_URL", "https://t.me/aresxcores")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)

# Support
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/aresxcores")   # Updates channel
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/roseysupport")         # Support group

# Assistant settings
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")
AUTO_LEAVE_ASSISTANT_TIME = _int_env("ASSISTANT_LEAVE_TIME", 9000)


# Server limits and configurations - These can be set based on your server configurations
SERVER_PLAYLIST_LIMIT = _int_env("SERVER_PLAYLIST_LIMIT", 3000)
PLAYLIST_FETCH_LIMIT = _int_env("PLAYLIST_FETCH_LIMIT", 25)
SONG_DOWNLOAD_DURATION = _int_env("SONG_DOWNLOAD_DURATION", 9999999)
SONG_DOWNLOAD_DURATION_LIMIT = _int_env("SONG_DOWNLOAD_DURATION_LIMIT", 9999999)

# Spotify
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "")

# Telegram file limits
TG_AUDIO_FILESIZE_LIMIT = _int_env("TG_AUDIO_FILESIZE_LIMIT", 5242880000)
TG_VIDEO_FILESIZE_LIMIT = _int_env("TG_VIDEO_FILESIZE_LIMIT", 5242880000)

# Session strings
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)
STRING6 = getenv("STRING_SESSION6", None)
STRING7 = getenv("STRING_SESSION7", None)

# Miscellaneous
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# Debugging
DEBUG_IGNORE_LOG = getenv("DEBUG_IGNORE_LOG", "False").lower() == "true"

# Additional group/channel IDs
LOG_GROUP_ID = _int_env("LOG_GROUP_ID", LOGGER_ID)
SUPPORT_GROUP = getenv("SUPPORT_GROUP", SUPPORT_CHAT)

# Image URLs
SHASHANK_IMG = getenv("SHASHANK_IMG", "https://files.catbox.moe/ky6ln3.jpg").split(",") if "," in getenv("SHASHANK_IMG", "") else [getenv("SHASHANK_IMG", "https://files.catbox.moe/ky6ln3.jpg")]

# Rotating start photos (used by start command and home callbacks)
START_PICS = [
    "https://files.catbox.moe/43725g.png",
    "https://files.catbox.moe/43725g.png",
    "https://files.catbox.moe/43725g.png",
    "https://files.catbox.moe/43725g.png",
    "https://files.catbox.moe/43725g.png",
    "https://files.catbox.moe/43725g.png",
    "https://files.catbox.moe/43725g.png",
    "https://files.catbox.moe/43725g.png",
]

PING_IMAGE_URL = getenv("PING_IMAGE_URL""https://files.catbox.moe/43725g.png")

START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/43725g.png")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/43725g.png")
PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://files.catbox.moe/43725g.png")
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://files.catbox.moe/43725g.png")
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://files.catbox.moe/ifgkkl.jpg")
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://files.catbox.moe/qm6b0n.jpg")
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://files.catbox.moe/ap3m1t.png")
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://files.catbox.moe/0k863e.png")
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://files.catbox.moe/vp5hg5.png")
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://files.catbox.moe/ky6ln3.jpg")
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://files.catbox.moe/booqz5.jpg")
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://files.catbox.moe/qlq89x.jpg")


# Helper function
def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

# Calculate total duration limit in seconds
DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# Validate URLs
if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit(
        "[ERROR] - Your SUPPORT_CHANNEL url is invalid. It must start with https://"
    )

if SUPPORT_CHAT and not re.match(r"(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit(
        "[ERROR] - Your SUPPORT_CHAT url is invalid. It must start with https://"
    )
