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
_keepalive_runner = None


async def _ping(request):
    return web.json_response(_runtime_state)

async def start_keepalive():
    """Start one lightweight HTTP server for health checks.

    The supervisor can restart Telegram clients without starting duplicate
    listeners on the same PORT.
    """
    global _keepalive_runner
    if _keepalive_runner is not None:
        return
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
    _keepalive_runner = runner
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
        _runtime_state.update({
            "status": "error",
            "stage": "session_check_failed",
            "error": "No assistant session configured",
        })
        return
    try:
        await asyncio.wait_for(sudo(), timeout=10)
    except Exception as exc:
        LOGGER(__name__).warning(
            f"Sudo initialization skipped; bot startup will continue: {type(exc).__name__}: {exc}"
        )
    for loader in (get_gbanned, get_banned_users):
        try:
            await asyncio.wait_for(loader(), timeout=10)
        except Exception as exc:
            LOGGER(__name__).warning(
                f"Ban-list initialization skipped: {type(exc).__name__}: {exc}"
            )
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
    _runtime_state["stage"] = "assistants_starting"
    await userbot.start()
    _runtime_state["stage"] = "voice_starting"
    await SHUKLA.start()
    # Do not join/play a boot-time test stream. It adds latency and can fail
    # startup when LOGGER_ID is unavailable, even though the bot is healthy.
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


async def _safe_stop():
    """Stop partially-started clients after a failed run before retrying."""
    for resource, name in ((SHUKLA, "voice"), (userbot, "assistant"), (app, "bot")):
        stop = getattr(resource, "stop", None)
        if not callable(stop):
            continue
        try:
            await asyncio.wait_for(stop(), timeout=20)
        except Exception as exc:
            LOGGER("SHUKLAMUSIC").warning(
                f"Could not stop {name} cleanly: {type(exc).__name__}: {exc}"
            )


async def run_forever():
    """Keep the bot alive through transient Telegram/voice/network failures."""
    restart_delay = 5
    while True:
        _runtime_state.update({
            "status": "starting",
            "stage": "supervisor_starting",
            "failed_plugins": [],
        })
        try:
            await init()
            restart_delay = 5
            # init() returns after a normal idle shutdown. Avoid a tight loop.
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            await _safe_stop()
            raise
        except Exception as exc:
            _runtime_state.update({
                "status": "degraded",
                "stage": "restart_wait",
                "error": f"{type(exc).__name__}: {exc}",
            })
            LOGGER("SHUKLAMUSIC").exception(
                f"Main loop crashed; retrying in {restart_delay}s: {exc}"
            )
            await _safe_stop()
            await asyncio.sleep(restart_delay)
            restart_delay = min(restart_delay * 2, 60)


if __name__ == "__main__":
    asyncio.run(run_forever())
