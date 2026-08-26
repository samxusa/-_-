"""Compatibility entry point for Railway and local process managers."""

import runpy


if __name__ == "__main__":
    # SHUKLAMUSIC starts the single aiohttp health server on Railway's PORT.
    # Do not start a second fixed-port server here; that caused collisions when
    # a platform assigned PORT=8000.
    runpy.run_module("SHUKLAMUSIC", run_name="__main__", alter_sys=True)
