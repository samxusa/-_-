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
import asyncio
import config
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChannelInvalid,
    ChatAdminRequired,
    InviteRequestSent,
    PeerIdInvalid,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from SHUKLAMUSIC import YouTube, app
from SHUKLAMUSIC.misc import SUDOERS
from SHUKLAMUSIC.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_maintenance,
)
from SHUKLAMUSIC.utils.inline import botplaylist_markup
from SHUKLAMUSIC.utils.media import is_video_document
from config import PLAYLIST_IMG_URL, SUPPORT_CHAT, adminlist
from strings import get_string

links = {}


def PlayWrapper(command):
    async def wrapper(client, message):
        language, maintenance = await asyncio.gather(
            get_lang(message.chat.id),
            is_maintenance(),
        )
        _ = get_string(language)
        if message.sender_chat:
            from pyrogram.enums import ButtonStyle as _BS
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔧 ʜᴏᴡ ᴛᴏ ғɪx ?",
                            callback_data="SHUKLAmousAdmin",
                            style=_BS.DANGER,
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="💬 sᴜᴘᴘᴏʀᴛ",
                            url=config.SUPPORT_CHAT,
                            style=_BS.PRIMARY,
                        ),
                    ],
                ]
            )
            return await message.reply_text(_["general_3"], reply_markup=upl)

        if maintenance is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a> ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                    disable_web_page_preview=True,
                )

        # Acknowledge immediately. URL/search/download work can take seconds;
        # users should never mistake that work for a dead bot.
        status = await message.reply_text(_["play_1"])

        try:
            await message.delete()
        except Exception:
            pass

        audio_telegram = (
            (message.reply_to_message.audio or message.reply_to_message.voice)
            if message.reply_to_message
            else None
        )
        reply = message.reply_to_message
        video_telegram = None
        if reply:
            video_telegram = reply.video or (
                reply.document if is_video_document(reply.document) else None
            )
        url = await YouTube.url(message)
        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                try:
                    await status.delete()
                except Exception:
                    pass
                if "stream" in message.command:
                    return await message.reply_text(_["str_1"])
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["play_18"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

        async def _status_reply(text, **kwargs):
            try:
                return await status.edit_text(text, **kwargs)
            except Exception:
                return await message.reply_text(text, **kwargs)

        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await _status_reply(_["setting_7"])
            try:
                chat = await app.get_chat(chat_id)
            except:
                return await _status_reply(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None
        playmode, playty = await asyncio.gather(
            get_playmode(message.chat.id),
            get_playtype(message.chat.id),
        )
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await _status_reply(_["admin_13"])
                else:
                    if message.from_user.id not in admins:
                        return await _status_reply(_["play_4"])
        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None
        active_chat = await is_active_chat(chat_id)
        if message.command[0][-1] == "e":
            if not active_chat:
                return await _status_reply(_["play_16"])
            fplay = True
        else:
            fplay = None

        if not active_chat:
            try:
                userbot = await get_assistant(chat_id)
            except Exception as exc:
                return await _status_reply(
                    _["call_3"].format(app.mention, type(exc).__name__)
                )
            try:
                try:
                    # Ask the assistant client about its own membership. The
                    # bot client may not have this user in its peer cache,
                    # which causes PeerIdInvalid even when the assistant is
                    # already in the group.
                    get = await userbot.get_chat_member(chat_id, userbot.id)
                except ChatAdminRequired:
                    return await _status_reply(_["call_1"])
                if (
                    get.status == ChatMemberStatus.BANNED
                    or get.status == ChatMemberStatus.RESTRICTED
                ):
                    return await _status_reply(
                        _["call_2"].format(
                            app.mention, userbot.id, userbot.name, userbot.username
                        ), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text= "๏ 𝗨ɴʙᴀɴ 𝗔ssɪsᴛᴀɴᴛ ๏", callback_data=f"unban_assistant")]])
                    )
            except (UserNotParticipant, PeerIdInvalid, ChannelInvalid):
                myu = await message.reply_text(_["call_4"].format(app.mention))
                joined = False

                # Prefer a direct add for every chat. This avoids relying on
                # an old exported invite link and works when the bot has the
                # required permission to invite members.
                try:
                    await app.add_chat_members(chat_id, userbot.id)
                    joined = True
                except UserAlreadyParticipant:
                    joined = True
                except Exception:
                    pass   # fall through to invite-link method

                # ── For groups (or channel fallback): join via invite link ──
                if not joined:
                    if chat_id in links:
                        invitelink = links[chat_id]
                    else:
                        if message.chat.username and message.command[0][0] != "c":
                            invitelink = message.chat.username
                            try:
                                await userbot.resolve_peer(invitelink)
                            except:
                                pass
                        else:
                            try:
                                invitelink = await app.export_chat_invite_link(chat_id)
                            except ChatAdminRequired:
                                await myu.delete()
                                return await _status_reply(_["call_1"])
                            except Exception as e:
                                await myu.delete()
                                return await _status_reply(
                                    _["call_3"].format(app.mention, type(e).__name__)
                                )

                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace(
                            "https://t.me/+", "https://t.me/joinchat/"
                        )
                    try:
                        await userbot.join_chat(invitelink)
                        joined = True
                    except InviteRequestSent:
                        try:
                            await app.approve_chat_join_request(chat_id, userbot.id)
                        except Exception as e:
                            await myu.delete()
                            return await _status_reply(
                                _["call_3"].format(app.mention, type(e).__name__)
                            )
                        await asyncio.sleep(1)
                        await myu.edit(_["call_5"].format(app.mention))
                        joined = True
                    except UserAlreadyParticipant:
                        joined = True
                    except Exception as e:
                        # Invite links can expire while they remain cached in
                        # memory. Drop the stale value, export a fresh link,
                        # and retry once instead of making /play unusable.
                        if type(e).__name__ not in {
                            "InviteHashExpired",
                            "InviteHashInvalid",
                            "InviteHashEmpty",
                        }:
                            await myu.delete()
                            return await _status_reply(
                                _["call_3"].format(app.mention, type(e).__name__)
                            )
                        links.pop(chat_id, None)
                        try:
                            if message.chat.username and message.command[0][0] != "c":
                                fresh_link = message.chat.username
                            else:
                                fresh_link = await app.export_chat_invite_link(chat_id)
                            if fresh_link.startswith("https://t.me/+"):
                                fresh_link = fresh_link.replace(
                                    "https://t.me/+", "https://t.me/joinchat/"
                                )
                            await userbot.join_chat(fresh_link)
                            invitelink = fresh_link
                            joined = True
                        except InviteRequestSent:
                            try:
                                await app.approve_chat_join_request(chat_id, userbot.id)
                            except Exception as retry_exc:
                                await myu.delete()
                                return await _status_reply(
                                    _["call_3"].format(app.mention, type(retry_exc).__name__)
                                )
                            await asyncio.sleep(1)
                            joined = True
                        except UserAlreadyParticipant:
                            joined = True
                        except Exception as retry_exc:
                            await myu.delete()
                            return await _status_reply(
                                _["call_3"].format(app.mention, type(retry_exc).__name__)
                            )

                    links[chat_id] = invitelink

                try:
                    await userbot.resolve_peer(chat_id)
                except:
                    pass

                try:
                    await myu.delete()
                except:
                    pass

        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
            status_message=status,
        )

    return wrapper