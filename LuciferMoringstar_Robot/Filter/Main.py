# (c) PR0FESS0R-99
from Config import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, TUTORIAL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from LuciferMoringstar_Robot import get_filter_results, get_file_details, is_subscribed, get_poster
from LuciferMoringstar_Robot import RATING, GENRES, HELP, ABOUT
import random
BUTTONS = {}
BOT = {}

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📢 𝗝𝗼𝗶𝗻 𝗨𝗽𝗱𝗮𝘁𝗲𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 📢", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        mo_tech_yt = f"**🗂️ Title:** {search}\n**⭐ Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**📤 Uploaded by {message.chat.title}\n**➡️ Press The Down Buttons To Access The File**"
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                btn.append(
                 [
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}",callback_data=f"pr0fess0r_99#{file_id}"),
                    InlineKeyboardButton(text=f"{file.file_name}",callback_data=f"pr0fess0r_99#{file_id}") 
                 ]
            )
             
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAADBQADMwIAAtbcmFelnLaGAZhgBwI')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📑 Pages 1/1 📝",callback_data="pages")]
            )
            poster=None 
            buttons = [[InlineKeyboardButton("✪ 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 ✪", url="https://t.me/joinchat/XwtyyrY9RH41YmE1")]]  + buttons
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="☛ 𝗚𝗢 𝗧𝗢 𝗡𝗘𝗫𝗧 𝗣𝗔𝗚𝗘 📇",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🔖 𝗣𝗮𝗴𝗲 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        buttons = [[InlineKeyboardButton("✪ 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 ✪", url="https://t.me/joinchat/XwtyyrY9RH41YmE1")]]  + buttons
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        mo_tech_yt = f"**🗂️ Title:** {search}\n**⭐ Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**📤 Uploaded by {message.chat.title}**"
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=pr0fess0r_99_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📑 Pages 1/1 📝",callback_data="pages")]
            )
            poster=None
            buttons = [[InlineKeyboardButton("✪ 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 ✪", url="https://t.me/joinchat/XwtyyrY9RH41YmE1")]]  + buttons
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="☛ 𝗚𝗢 𝗧𝗢 𝗡𝗘𝗫𝗧 𝗣𝗔𝗚𝗘 📇",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🔖 𝗣𝗮𝗴𝗲 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        buttons = [[InlineKeyboardButton("✪ 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 ✪", url="https://t.me/joinchat/XwtyyrY9RH41YmE1")]]  + buttons
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("☚ 𝘽𝙖𝙘𝙠", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"(๑′°︿°๑)  🔖 𝗣𝗮𝗴𝗲 {int(index)+2}/{data['total']}  (๑′°︿°๑)", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("☚𝘽𝙖𝙘𝙠", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("𝙉𝙚𝙭𝙩 ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"(๑′°︿°๑)  🔖 𝗣𝗮𝗴𝗲 {int(index)+2}/{data['total']}  (๑′°︿°๑)", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("𝗚𝗢 𝗧𝗢 𝗡𝗘𝗫𝗧 𝗣𝗔𝗚𝗘 📇", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"(๑′°︿°๑)  🔖 𝗣𝗮𝗴𝗲 {int(index)}/{data['total']}  (๑′°︿°๑)", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("☚⏪ 𝘽𝙖𝙘𝙠", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("𝙉𝙚𝙭𝙩 ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"(๑′°︿°๑)  🔖 𝗣𝗮𝗴𝗲 {int(index)}/{data['total']}  (๑′°︿°๑)", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "help":
            buttons = [
                [
                    InlineKeyboardButton('Premium Webseries 🔰', url='https://t.me/joinchat/_BnPI1aIpz5lZDE1'),
                    InlineKeyboardButton('Premium Movies 🎬', url='https://t.me/joinchat/XwtyyrY9RH41YmE1')
                ]
                ]
            await query.message.edit(text=f"{HELP}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('Premium Webseries 🔰', url='https://t.me/joinchat/XwtyyrY9RH41YmE1'),
                    InlineKeyboardButton('Premium Movies 🎬', url='https://t.me/joinchat/XwtyyrY9RH41YmE1')
                ]
                ]
            await query.message.edit(text=f"{ABOUT}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


        elif query.data.startswith("pr0fess0r_99"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('Movies Club 🎬', url='https://t.me/MoviesClub_OP')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("𝐀𝐅𝐓𝐄𝐑 𝐉𝐎𝐈𝐍𝐈𝐍𝐆 𝐌𝐀𝐈𝐍 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐂𝐋𝐈𝐂𝐊 𝐌𝐄 ,𝐀𝐍𝐃 𝐘𝐎𝐔 𝐖𝐈𝐋𝐋 𝐆𝐄𝐓 𝐓𝐇𝐄 𝐅𝐈𝐋𝐄☺️",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('🎬Movies Group', url='https://t.me/MoviesClub_OP'),
                        InlineKeyboardButton('Private Database📊', url='https://t.me/joinchat/XwtyyrY9RH41YmE1')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("Why Bro Why 👀",show_alert=True)
