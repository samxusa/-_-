# -----------------------------------------------
# SHUKLAMUSIC / DHRUV X RADHA Music Bot
# -----------------------------------------------
import asyncio
import importlib
import os
from aiohttp import web
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
import config
from SHUKLAMUSIC import LOGGER, app, userbot
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.misc import sudo
from SHUKLAMUSIC.plugins import ALL_MODULES
from SHUKLAMUSIC.utils.database import get_banned_users, get_gbanned
from SHUKLAMUSIC.plugins.tools.vclogger import initialize_vc_logger
from SHUKLAMUSIC.core.commands import register_bot_commands


# ── Keep-alive web server ─────────────────────────────────────────────────────
_runtime_state = {
    "status": "starting",
    "stage": "booting",
    "bot": "ARES X GOD",
    "failed_plugins": [],
}


async def _ping(request):
    return web.json_response(_runtime_state)

async def start_keepalive():
    """Start a lightweight HTTP server so the repl stays alive via pings."""
    _app = web.Application()
    _app.router.add_get("/", _ping)
    _app.router.add_get("/ping", _ping)
    runner = web.AppRunner(_app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    try:
        await site.start()
    except OSError as ex:
        await runner.cleanup()
        if getattr(ex, "errno", None) == 98:
            LOGGER("SHUKLAMUSIC").warning(
                f"Keep-alive port {port} is already in use; "
                "continuing without starting a second HTTP listener."
            )
            return
        raise
    LOGGER("SHUKLAMUSIC").info(f"Keep-alive server started on port {port}")


async def init():
    # Bind Railway's assigned PORT before Telegram initialization. Telegram
    # login/session startup can take time, and Railway health checks should
    # still see a live HTTP service during that phase.
    await start_keepalive()
    _runtime_state["stage"] = "session_check"
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
        and not config.STRING6
        and not config.STRING7
    ):
        LOGGER(__name__).error("String Session Not Filled, Please Fill A Pyrogram Session")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            pass
        users = await get_banned_users()
        for user_id in users:
            pass
    except:
        pass
    _runtime_state["stage"] = "telegram_authorizing"
    await app.start()
    _runtime_state.update({"stage": "telegram_connected", "bot": getattr(app, "username", "unknown")})
    failed_plugins = []
    for all_module in ALL_MODULES:
        try:
            importlib.import_module("SHUKLAMUSIC.plugins" + all_module)
        except Exception as exc:
            failed_plugins.append(all_module)
            LOGGER("SHUKLAMUSIC.plugins").error(
                f"Plugin load failed for {all_module}: {type(exc).__name__}: {exc}"
            )
    _runtime_state["failed_plugins"] = failed_plugins
    LOGGER("SHUKLAMUSIC.plugins").info(
        f"Features loaded: {len(ALL_MODULES) - len(failed_plugins)}/{len(ALL_MODULES)}"
    )
    try:
        await register_bot_commands()
    except Exception as exc:
        LOGGER("SHUKLAMUSIC.core.commands").warning(
            f"Command menu registration failed; message handlers remain active: {type(exc).__name__}: {exc}"
        )
    await userbot.start()
    await SHUKLA.start()
    try:
        await SHUKLA.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("SHUKLAMUSIC").error(
            "No active voice chat in LOGGER_ID; continuing without startup audio."
        )
    except:
        pass
    await SHUKLA.decorators()
    await initialize_vc_logger()
    # Restore any dynamic sessions added via /addsession
    try:
        from SHUKLAMUSIC.plugins.sudo.addsession import restore_dynamic_sessions
        await restore_dynamic_sessions()
    except Exception:
        pass
    _runtime_state.update({"status": "ready", "stage": "ready", "bot": getattr(app, "username", "unknown")})
    LOGGER("SHUKLAMUSIC").info("Bot fully started!")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("SHUKLAMUSIC").info("Bot stopped.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
