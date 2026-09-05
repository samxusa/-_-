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
import config
from ..logging import LOGGER


def git():
    # Git sync is optional in Railway/container deployments. Import GitPython
    # lazily so a broken or unavailable Git client cannot stop bot startup.
    try:
        from git import Repo
        from git.exc import GitCommandError, InvalidGitRepositoryError
    except Exception as exc:
        LOGGER(__name__).warning(
            f"Git client unavailable; skipping upstream sync: {type(exc).__name__}: {exc}"
        )
        return

    REPO_LINK = config.UPSTREAM_REPO
    if config.GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
    else:
        UPSTREAM_REPO = config.UPSTREAM_REPO
    try:
        repo = Repo()
        LOGGER(__name__).info(f"Git Client Found [VPS DEPLOYER]")
    except GitCommandError:
        LOGGER(__name__).info(f"Invalid Git Command")
    except InvalidGitRepositoryError:
        # A deployed source bundle may not contain .git metadata. Do not try
        # to clone or install dependencies during import; startup must remain
        # independent of the Git CLI and package manager.
        LOGGER(__name__).warning(
            "Git metadata not found; skipping upstream sync."
        )

    except Exception as exc:
        LOGGER(__name__).warning(
            f"Git sync unavailable; continuing startup: {type(exc).__name__}: {exc}"
        )
