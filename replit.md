# ROSE X MUSIC Bot (SHUKLAMUSIC)

A Telegram voice-chat music bot that streams YouTube, Spotify, Apple Music, and SoundCloud audio into Telegram group voice chats. Includes an AI chatbot (Groq/LLaMA 3.3), autoplay, queue management, and a built-in keep-alive web server.

## Tech Stack

- **Python 3.12**
- **Pyrogram** — Telegram MTProto client (bot)
- **PyTgCalls** — Telegram voice-chat streaming
- **yt-dlp** — YouTube/audio downloading
- **Motor / MongoDB** — async database
- **Groq (LLaMA 3.3 70B)** — AI chatbot
- **aiohttp** — keep-alive web server (port 8080)

## How to Run

The bot starts automatically via the **"Start application"** workflow:

```
python3 -m SHUKLAMUSIC
```

The keep-alive HTTP server listens on the platform-provided `PORT` (8080 locally by default) and responds to `/`, `/ping`, and `/health` with the current startup state. The bot is designed for an always-on VM deployment; an uptime monitor is not required to keep the process alive.

## Required Secrets

All secrets are stored as Replit Secrets (never hardcoded):

| Secret | Description |
|---|---|
| `API_ID` | Telegram API ID from https://my.telegram.org |
| `API_HASH` | Telegram API Hash from https://my.telegram.org |
| `BOT_TOKEN` | Bot token from @BotFather |
| `MONGO_DB_URI` | MongoDB Atlas connection string |
| `STRING_SESSION` | Pyrogram userbot session string |
| `LOGGER_ID` | Numeric ID of Telegram log group/channel |
| `OWNER_ID` | Bot owner's Telegram numeric user ID |
| `GIT_TOKEN` | GitHub personal access token (optional; never commit this) |
| `YOUTUBE_API_KEY` | YouTube Data API v3 key (optional) |
| `GROQ_API_KEY` | Groq API key for AI chatbot (optional) |

## Reliability

- The bot starts the health server before Telegram clients so deployment health checks can observe slow authentication.
- Telegram and voice startup are supervised; transient failures back off and retry instead of exiting immediately.
- Invalid or missing `LOGGER_ID` disables optional startup logging without blocking the music bot.
- Keep all credentials in Replit Secrets or the deployment provider's secret store. Do not put them in `.replit`, `sample.env`, or committed source files.
