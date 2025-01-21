import time
import random 
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from JioSavaan import app
from JioSavaan.misc import _boot_
from JioSavaan.plugins.sudo.sudoers import sudoers_list
from JioSavaan.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from JioSavaan.utils.decorators.language import LanguageStart
from JioSavaan.utils.formatters import get_readable_time
from JioSavaan.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

IMAGE = [
"https://te.legra.ph/file/7757731c3e8b784b6a550.png", 
"https://te.legra.ph/file/58c34981e21180989887c.png", 
"https://te.legra.ph/file/a3a874be5095d9af685ac.png", 
"https://te.legra.ph/file/ac461a1889255424420ff.png", 
"https://te.legra.ph/file/74a8ba5270d0e27ac045c.png", 
"https://te.legra.ph/file/c0d0ee1452cbbbce116f4.png", 
"https://te.legra.ph/file/d373ae93502a5ae7fd403.png", 
"https://te.legra.ph/file/ab243bcad20965f637b5c.png", 
"https://te.legra.ph/file/fd9cc86239dd76d564d01.png", 
"https://te.legra.ph/file/c12a0b77178e2d2e27a50.png", 
"https://te.legra.ph/file/35177bbb5d5f07ad8e394.png", 
"https://te.legra.ph/file/700af8c3ee786a20aff35.png", 
"https://te.legra.ph/file/cbecd8af0446a422a95ca.png", 
"https://te.legra.ph/file/c3a0fde4abde25dd25e26.png", 
"https://te.legra.ph/file/7be8c2f9e093f695c4c6e.png", 
"https://te.legra.ph/file/ee10888e828bae3a6a0fc.png", 
"https://te.legra.ph/file/1b55fe681163188149fa4.png", 
"https://te.legra.ph/file/30ee4e96f64cd9abb69b6.png", 
"https://te.legra.ph/file/30b121ce5fa87360692ba.png", 
"https://te.legra.ph/file/f0617cc52008bd78f1a9d.png", 
"https://te.legra.ph/file/1cd1adc3eb9ac0a101610.png",
"https://te.legra.ph/file/860c3dd149f91eb450d5a.png", 
"https://te.legra.ph/file/2e9df77f8100e0327ba52.png",
"https://te.legra.ph/file/639efe98c133d71c418db.png",
"https://te.legra.ph/file/8a834586b677739b86bff.png",
"https://te.legra.ph/file/13f79674ce777f43871fb.png", 
"https://te.legra.ph/file/147157eca055a1e2c8756.png",
"https://te.legra.ph/file/b774a8da74dc954afebc6.png",
"https://te.legra.ph/file/7ae4a6a6a6c28f9f08ceb.png",
"https://te.legra.ph/file/12d5ea64ed00416a38ec8.png"   

]



@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    await message.react("❤️")
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            await message.reply_sticker("CAACAgIAAxkBAAEBAjVnjyrcOqBOoPgtfLpcN3vlL7h4eAAC5SsAAmMK-UnNyZDgYsxtfjYE")
            return await message.reply_photo(
                random.choice(IMAGE),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"❀ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>● ᴜsᴇʀ ɪᴅ ➥</b> <code>{message.from_user.id}</code>\n<b>● ᴜsᴇʀɴᴀᴍᴇ ➥</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"❀ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>● ᴜsᴇʀ ɪᴅ ➥</b> <code>{message.from_user.id}</code>\n<b>● ᴜsᴇʀɴᴀᴍᴇ ➥</b> @{message.from_user.username}",
                )
    else:
        out = private_panel(_)
        await message.reply_sticker("CAACAgIAAxkBAAEBAjVnjyrcOqBOoPgtfLpcN3vlL7h4eAAC5SsAAmMK-UnNyZDgYsxtfjYE")
        await message.reply_photo(
            random.choice(IMAGE),
            caption=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"❀ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>● ᴜsᴇʀ ɪᴅ ➥</b> <code>{message.from_user.id}</code>\n<b>● ᴜsᴇʀɴᴀᴍᴇ ➥</b> @{message.from_user.username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        random.choice(IMAGE),
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    random.choice(IMAGE),
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
            
