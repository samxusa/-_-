---
name: Pyrogram event loop
description: Event-loop compatibility guidance for Pyrogram and PyTgCalls startup/reconnects.
---

Pyrogram clients must be started on the same asyncio event loop they bind to during import-time construction; reusing the configured process loop avoids cross-loop futures during reconnects.

**Why:** Replacing the process loop with `asyncio.run()` caused Telegram startup retries to fail with “Future attached to a different loop” even though credentials and network access were valid.

**How to apply:** Keep the entrypoint on the existing configured loop when client objects are constructed at module import. If changing initialization order, retest bot reconnects and assistant startup.