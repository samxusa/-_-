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
import os
from os import path
import yt_dlp
from yt_dlp.utils import DownloadError
from config import YOUTUBE_COOKIES_FILE

def _cookies_file():
    if (
        YOUTUBE_COOKIES_FILE
        and os.path.isfile(YOUTUBE_COOKIES_FILE)
        and os.path.getsize(YOUTUBE_COOKIES_FILE) > 50
    ):
        return YOUTUBE_COOKIES_FILE
    return None


def _base_opts():
    opts = {
        "outtmpl": "downloads/%(id)s.%(ext)s",
        # format 18 = combined 360p H.264+AAC, no SABR/PO-token needed.
        # Falls back to bestaudio if format 18 is not available.
        "format": "18/bestaudio[ext=m4a]/bestaudio/best",
        "format_sort": ["abr", "asr"],
        "geo_bypass": True,
        "nocheckcertificate": True,
        "extractor_args": {
            "youtube": {
                # android provides format 18; mweb provides its config download.
                # Do NOT skip configs — mweb needs its config to expose format 18.
                "player_client": ["android", "mweb"],
            }
        },
    }
    cookies = _cookies_file()
    if cookies:
        opts["cookiefile"] = cookies
    return opts


ytdl = yt_dlp.YoutubeDL(_base_opts())


def download(url: str, my_hook) -> str:
    ydl_optssx = {
        **_base_opts(),
        'quiet': True,
        'no_warnings': True,
    }
    info = ytdl.extract_info(url, False)
    try:
        x = yt_dlp.YoutubeDL(ydl_optssx)
        x.add_progress_hook(my_hook)
        dloader = x.download([url])
    except Exception as y_e:
        return print(y_e)
    else:
        dloader
    xyz = path.join("downloads", f"{info['id']}.{info['ext']}")
    return xyz
