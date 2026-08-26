# Railway credentials setup

This project is a Telegram voice-chat music bot. Add the following variables
in **Railway → Service → Variables**. Do not put real values in GitHub,
`sample.env`, or chat messages.

## Required for startup and `/play` / `/vplay`

| Variable | Where to get it | Notes |
| --- | --- | --- |
| `API_ID` | my.telegram.org → API development tools | Numeric Telegram app ID |
| `API_HASH` | Same Telegram app page | Keep private |
| `BOT_TOKEN` | @BotFather | Create a bot token |
| `OWNER_ID` | Telegram ID lookup | Numeric owner user ID |
| `LOGGER_ID` | Telegram group/channel ID | The bot must be able to access it |
| `MONGO_DB_URI` | MongoDB Atlas or another MongoDB provider | Allow Railway network access |
| `STRING_SESSION` | Generate with a trusted Pyrogram session generator | Keep private; this is a user account session |

The bot must be added to `LOGGER_ID` and promoted as an administrator. The
assistant account represented by `STRING_SESSION` must also be able to join
voice chats and must be an administrator in the target group.

## Optional integrations

| Variable | Enables |
| --- | --- |
| `YOUTUBE_API_KEY` | Faster YouTube search and metadata |
| `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` | Spotify search and playlists |
| `TMDB_API_KEY` | Movie search |
| `GROQ_API_KEY` | AI chatbot features |
| `API_KEY` / `API_URL` | Optional external media API fallback |
| `YOUTUBE_COOKIES_FILE` | Optional private cookie file for age-restricted YouTube content |

YouTube playback still uses `yt-dlp` when `YOUTUBE_API_KEY` is empty. The
optional YouTube API key is not the same thing as `BOT_TOKEN`.

## Railway deployment

1. Deploy the repository as a Railway service.
2. Add the variables above in the Variables tab.
3. Use the default Dockerfile build, or set the start command to
   `python3 -m SHUKLAMUSIC`.
4. Railway supplies `PORT` automatically. The bot exposes `/` and `/ping` on
   that port and returns a JSON health response.
5. Deploy and check the service logs for `Bot fully started!`.

Do not use a worker-only process for this service: Railway health checks need
the web process to bind the assigned `PORT`.