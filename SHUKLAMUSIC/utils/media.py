"""Small helpers for identifying Telegram media safely."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any


VIDEO_EXTENSIONS = {
    ".3gp",
    ".avi",
    ".flv",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpeg",
    ".mpg",
    ".webm",
    ".wmv",
}


def is_video_document(document: Any) -> bool:
    """Return True only for documents that look like video files.

    Telegram users often upload videos as documents. Treating every document
    as video makes `/vplay` try to download PDFs, archives, and images as
    video streams, which then fails later inside ffmpeg.
    """

    if document is None:
        return False

    mime_type = (getattr(document, "mime_type", None) or "").lower()
    if mime_type.startswith("video/"):
        return True

    file_name = getattr(document, "file_name", None) or ""
    suffix = PurePosixPath(file_name).suffix.lower()
    return suffix in VIDEO_EXTENSIONS