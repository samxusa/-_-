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
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from ..logging import LOGGER


class _NoopResult:
    acknowledged = False
    deleted_count = 0
    modified_count = 0
    matched_count = 0
    inserted_id = None


class _EmptyCursor:
    def __aiter__(self):
        return self

    async def __anext__(self):
        raise StopAsyncIteration

    def sort(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    async def to_list(self, length=None):
        return []


class _FallbackCollection:
    async def find_one(self, *args, **kwargs):
        return None

    def find(self, *args, **kwargs):
        return _EmptyCursor()

    async def update_one(self, *args, **kwargs):
        return _NoopResult()

    async def insert_one(self, *args, **kwargs):
        return _NoopResult()

    async def delete_one(self, *args, **kwargs):
        return _NoopResult()

    async def delete_many(self, *args, **kwargs):
        return _NoopResult()

    async def replace_one(self, *args, **kwargs):
        return _NoopResult()

    async def count_documents(self, *args, **kwargs):
        return 0


class _FallbackDatabase:
    def __getattr__(self, name):
        return _FallbackCollection()


if MONGO_DB_URI:
    LOGGER(__name__).info("Connecting to your Mongo Database...")
    try:
        _mongo_async_ = AsyncIOMotorClient(
            MONGO_DB_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=10000,
            waitQueueTimeoutMS=5000,
        )
        mongodb = _mongo_async_.Anon
        LOGGER(__name__).info("Mongo Database client initialized.")
    except Exception as exc:
        LOGGER(__name__).error(
            f"Mongo client initialization failed; using safe in-memory fallback: {type(exc).__name__}: {exc}"
        )
        mongodb = _FallbackDatabase()
else:
    LOGGER(__name__).warning(
        "MONGO_DB_URI is not configured; using safe in-memory fallback. "
        "Persistent features will be unavailable, but Telegram handlers can start."
    )
    mongodb = _FallbackDatabase()