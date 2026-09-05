# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# -----------------------------------------------
import asyncio

from pyrogram import Client
from pyrogram.errors import FloodWait

import config
from ..logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(name="SHUKLAAss1", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING1))
        self.two = Client(name="SHUKLAAss2", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING2))
        self.three = Client(name="SHUKLAAss3", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING3))
        self.four = Client(name="SHUKLAAss4", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING4))
        self.five = Client(name="SHUKLAAss5", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING5))
        self.six = Client(name="SHUKLAAss6", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING6))
        self.seven = Client(name="SHUKLAAss7", api_id=config.API_ID, api_hash=config.API_HASH, session_string=str(config.STRING7))

    def _assistant_specs(self):
        return (
            (1, self.one, config.STRING1, "One"),
            (2, self.two, config.STRING2, "Two"),
            (3, self.three, config.STRING3, "Three"),
            (4, self.four, config.STRING4, "Four"),
            (5, self.five, config.STRING5, "Five"),
            (6, self.six, config.STRING6, "Six"),
            (7, self.seven, config.STRING7, "Seven"),
        )

    async def _start_assistant(self, number, client, label):
        try:
            await client.start()
        except FloodWait as exc:
            wait = getattr(exc, "value", getattr(exc, "x", "unknown"))
            LOGGER(__name__).error(
                f"Assistant {label} hit Telegram FloodWait ({wait}s); skipping this assistant."
            )
            return False
        except Exception as exc:
            LOGGER(__name__).error(
                f"Assistant {label} failed to start; continuing without it: "
                f"{type(exc).__name__}: {exc}"
            )
            return False

        assistants.append(number)
        client.id = client.me.id
        client.name = client.me.mention
        client.username = client.me.username
        assistantids.append(client.id)

        # Do not join promotional chats or send startup messages automatically.
        # Those repeated writes were causing FloodWaits with multiple assistants.
        if config.SEND_ASSISTANT_STARTUP_MESSAGES:
            try:
                await client.send_message(config.LOGGER_ID, "Assistant Started")
            except FloodWait as exc:
                wait = getattr(exc, "value", getattr(exc, "x", "unknown"))
                LOGGER(__name__).warning(
                    f"Assistant {label} startup message rate-limited ({wait}s); continuing."
                )
            except Exception as exc:
                LOGGER(__name__).warning(
                    f"Assistant {label} cannot access LOGGER_ID: {type(exc).__name__}: {exc}"
                )

        if not hasattr(self, "id"):
            self.id = client.id
            self.name = client.name
            self.username = client.username
        LOGGER(__name__).info(f"Assistant {label} Started as {client.name}")
        return True

    async def start(self):
        LOGGER(__name__).info("Starting Assistants without automatic chat joins...")
        assistants.clear()
        assistantids.clear()
        for number, client, session, label in self._assistant_specs():
            if not session:
                continue
            await self._start_assistant(number, client, label)
            # Keep Telegram auth/start requests spaced out across sessions.
            await asyncio.sleep(1)

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        for _, client, session, label in self._assistant_specs():
            if not session:
                continue
            try:
                await client.stop()
            except Exception as exc:
                LOGGER(__name__).warning(
                    f"Assistant {label} stop failed: {type(exc).__name__}: {exc}"
                )
