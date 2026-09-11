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
from pyrogram.types import Message
from SHUKLAMUSIC import YouTube, app
from pyrogram import filters

@app.on_message(filters.command("search"))
async def ytsearch(_, message: Message):
    m = None
    try:
        if len(message.command) < 2:
            await message.reply_text("/search needs an argument!")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("🔎 Searching YouTube…")
        results = await YouTube.search(query, max_results=5)
        if not results:
            return await m.edit("No YouTube results found. Try a shorter title.")
        text = "\n\n".join(
            f"{index}. <b>{item['title']}</b>\n"
            f"Duration: {item['duration_min']}\n"
            f"{item['link']}"
            for index, item in enumerate(results, 1)
        )
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        if m:
            await m.edit(f"Search failed: {type(e).__name__}")
        else:
            await message.reply_text(f"Search failed: {type(e).__name__}")
