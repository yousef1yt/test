from pyrogram import Client, filters, raw, utils
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message
from config import logger as log, logger_mode as logm, OWNER
from GeNeRaL.info import (get_served_chats, get_served_users, del_served_chat, del_served_user, activecall, add_active_chat, add_served_call, add_active_video_chat)
from GeNeRaL.Data import Bots
from GeNeRaL.play import (logs, join_call)
from GeNeRaL.Data import (get_userbot, get_dev, get_call, get_group, get_channel)
import aiohttp
import asyncio
from datetime import datetime
from pyrogram.errors import FloodWait
from pyrogram import enums
from typing import Union, List, Iterable

BASE = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def base(text):
    resp = await post(f"{BASE}api/v2/paste", data=text)
    if not resp["success"]:
        return
    link = BASE + resp["message"]
    return link



@Client.on_message(filters.command(["الاحصائيات", "❲ الاحصائيات ❳"], ""))
async def analysis(client: Client, message: Message):
 bot_username = client.me.username
 dev = await get_dev(bot_username)
 if message.chat.id == dev or message.chat.username in OWNER:
   chats = len(await get_served_chats(client))
   user = len(await get_served_users(client))
   return await message.reply_text(f"****≭︰احصائيات البوت كامله ↯.**\n**≭︰ المجموعات ↫ ❲ {chats} ❳ **\n**≭︰ المستخدمين ↫ ❲ {user} ❳ **")

@Client.on_message(filters.command(["❲ الكروبات ❳"], ""))
async def chats_func(client: Client, message: Message):
 bot_username = client.me.username
 dev = await get_dev(bot_username)
 if message.chat.id == dev or message.chat.username in OWNER:
    m = await message.reply_text("≭︰انتظر قليلا ...")
    served_chats = []
    text = ""
    chats = await get_served_chats(client)
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    count = 0
    co = 0
    msg = ""
    for served_chat in served_chats:
        if f"{served_chat}" in text:
          await del_served_chat(client, served_chat)
        else:
         try:
            chat = await client.get_chat(served_chat)
            title = chat.title
            username = chat.username
            count += 1
            txt = f"{count}- ︰المجموعه ↫ ❲ [{title}](https://t.me/{username}) ❳ ︰ايديها ↫ ❲ `{served_chat}` ❳\n" if username else f"{count}- ︰المجموعه ↫ ❲ {title} ❳ ︰ايديها ↫ ❲ `{served_chat}` ❳\n"
            text += txt
         except Exception:
            title = "Not Found" 
            count += 1
            text += f"{count}:- {title} {served_chat}\n"
    if count == 0:
      return await m.edit("≭︰لا يوجد كروبات")
    else:
      try:
        await message.reply_text(text, disable_web_page_preview=True)
      except: 
         link = await base(text)
         await message.reply_text(link)
      return await m.delete()



@Client.on_message(filters.command(["❲ المشتركين ❳"], ""))
async def users_func(client: Client, message: Message):
 bot_username = client.me.username
 dev = await get_dev(bot_username)
 if message.chat.id == dev or message.chat.username in OWNER:
    m = await message.reply_text("≭︰انتظر قليلا ....")
    served_chats = []
    text = ""
    chats = await get_served_users(client)
    for chat in chats:
        served_chats.append(int(chat["user_id"]))
    count = 0
    co = 0
    msg = ""
    for served_chat in served_chats:
        if f"{served_chat}" in text:
           await del_served_user(client, served_chat)
        else:
         try:
            chat = await client.get_chat(served_chat)
            title = chat.first_name
            username = chat.username
            count += 1
            txt = f"{count}- ︰العضو ↫ ❲ [{title}](https://t.me/{username}) ❳ ︰ايديه ↫ ❲ `{served_chat}` ❳\n" if username else f"{count}- ︰العضو ↫ ❲ {title} ❳ ︰ايديه ↫ ❲ `{served_chat}` ❳\n"
            text += txt
         except Exception:
            title = "Not Found" 
            count += 1
            text += f"{count}-  {title} {served_chat}\n"
    if count == 0:
      return await m.edit("≭︰لا يوجد مشتركين")
    else:
      try:
        await message.reply_text(text, disable_web_page_preview=True)
      except: 
         link = await base(text)
         await message.reply_text(link)
      return await m.delete()

@Client.on_message(filters.command("❲ المكالمات النشطه ❳", ""))
async def geetmeactive(client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username in OWNER:
   m = await message.reply_text("**≭︰انتظر قليلا ..**")
   count = 0
   text = ""
   for i in activecall[client.me.username]:
       try:
          chat = await client.get_chat(i)
          count += 1
          text += f"{count}- ❲ [{chat.title}](https://t.me/{chat.username}) ❳\n" if chat.username else f"❲ {chat.title} ❳\n"
       except Exception:
            title = "Not Found" 
            count += 1
            text += f"{count}:- {title} {chat.id}\n"
   if count == 0:
      return await m.edit("≭︰لا يوجد مكالمات قيد التشغيل")
   else:
      try:
        await message.reply_text(text, disable_web_page_preview=True)
      except: 
         link = await base(text)
         await message.reply_text(link)
      return await m.delete()



@Client.on_message(filters.command(["❲ اوامر الاذاعه ❳", "❲ للخلف ❳"], ""))
async def cast(client: Client, message):
   bot_username = client.me.username
   dev = await get_dev(bot_username)
   if message.chat.id == dev or message.chat.username in OWNER:
    kep = ReplyKeyboardMarkup([["❲ اذاعه عام ❳"], ["❲ اذاعه للمجموعات ❳", "❲ اذاعه للمستخدمين ❳"], ["❲ توجيه عام ❳"], ["❲ توجيه للمجموعات ❳", "❲ توجيه للمستخدمين ❳"], ["❲ القائمه الرئيسيه ❳"]], resize_keyboard=True)
    await message.reply_text("**≭︰مرحبا بك عزيزي المطور **\n**≭︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)


@Client.on_message(filters.command(["❲ اذاعه عام ❳", "❲ اذاعه للمجموعات ❳", "❲ اذاعه للمستخدمين ❳", "❲ توجيه عام ❳", "❲ توجيه للمستخدمين ❳", "❲ توجيه للمجموعات ❳"], ""))
async def cast1(client: Client, message):
   command = message.command[0]
   bot_username = client.me.username
   dev = await get_dev(bot_username)
   if message.chat.id == dev or message.chat.username in OWNER:
    if command == "❲ اذاعه عام ❳":
     kep = ReplyKeyboardMarkup([["❲ اذاعه عام بالبوت ❳"], ["❲ اذاعه عام بالمساعد ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≭︰مرحبا بك عزيزي المطور **\n**≭︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)
    elif command == "❲ اذاعه للمجموعات ❳":
     kep = ReplyKeyboardMarkup([["❲ اذاعه للمجموعات بالبوت ❳"], ["❲ اذاعه للمجموعات بالمساعد ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≭︰مرحبا بك عزيزي المطور **\n**≭︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)
    elif command == "❲ اذاعه للمستخدمين ❳":
     kep = ReplyKeyboardMarkup([["❲ اذاعه للمستخدمين بالبوت ❳"], ["❲ اذاعه للمستخدمين بالمساعد ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≭︰مرحبا بك عزيزي المطور **\n**≭︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)
    elif command == "❲ توجيه عام ❳":
     kep = ReplyKeyboardMarkup([["❲ توجيه عام بالبوت ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≭︰مرحبا بك عزيزي المطور **\n**≭︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)
    elif command == "❲ توجيه للمستخدمين ❳":
     kep = ReplyKeyboardMarkup([["❲ توجيه للمستخدمين بالبوت ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≭︰مرحبا بك عزيزي المطور **\n**≭︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)
    else:
     kep = ReplyKeyboardMarkup([["❲ توجيه للمجموعات بالبوت ❳"], ["❲ للخلف ❳"]], resize_keyboard=True)
     await message.reply_text("**≭︰مرحبا بك عزيزي المطور **\n**≭︰اليك كيبورد اوامر الاذاعات**", reply_markup=kep)


@Client.on_message(filters.command(["❲ اذاعه عام بالبوت ❳", "❲ اذاعه عام بالمساعد ❳", "❲ اذاعه للمجموعات بالبوت ❳", "❲ اذاعه للمجموعات بالمساعد ❳", "❲ اذاعه للمستخدمين بالبوت ❳", "❲ اذاعه للمستخدمين بالمساعد ❳", "❲ توجيه عام بالبوت ❳", "❲ توجيه عام بالمساعد ❳", "❲ توجيه للمجموعات بالبوت ❳", "❲ توجيه للمجموعات بالمساعد ❳", "❲ توجيه للمستخدمين بالبوت ❳", "❲ توجيه للمستخدمين بالمساعد ❳"], ""))
async def cast5(client: Client, message):
  command = message.command[0]
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username in OWNER:
   kep = ReplyKeyboardMarkup([["❲ الغاء ❳"], ["❲ للخلف ❳"], ["❲ القائمه الرئيسيه ❳"]], resize_keyboard=True)
   ask = await client.ask(message.chat.id, "≭︰ارسل الرساله المراد اذاعتها", reply_markup=kep)
   x = ask.id
   y = message.chat.id
   if ask.text == "❲ الغاء ❳":
     return await ask.reply_text("**≭︰تم الغاء الامر**")
   pn = await client.ask(message.chat.id, "≭︰هل تريد تثبيت الرساله ؟\n≭︰ارسل ❲ نعم ❳ او ❲ لا ❳")
   await message.reply_text("**≭︰جاري نشر الرساله قد يستغرق بعض الوقت**")
   text = ask.text
   dn = 0
   fd = 0
   if command == "❲ اذاعه عام بالبوت ❳":
     chats = await get_served_chats(client)
     users = await get_served_users(client)
     chat = []
     for user in users:
         chat.append(int(user["user_id"]))
     for c in chats:
         chat.append(int(c["chat_id"]))
     for i in chat:
         try:
           m = await client.send_message(chat_id=i, text=text)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
         except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
         except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ اذاعه عام بالمساعد ❳":
     user = await get_userbot(bot_username)
     async for i in user.get_dialogs():
         try:
           m = await user.send_message(chat_id=i.chat.id, text=text)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
         except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
         except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ اذاعه للمجموعات بالبوت ❳":
     chats = await get_served_chats(client)
     chat = []
     for c in chats:
         chat.append(int(c["chat_id"]))
     for i in chat:
         try:
           m = await client.send_message(chat_id=i, text=text)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
         except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
         except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ اذاعه للمجموعات بالمساعد ❳":
     user = await get_userbot(bot_username)
     async for i in user.get_dialogs():
         if not i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await user.send_message(chat_id=i.chat.id, text=text)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
          except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
          except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ اذاعه للمستخدمين بالبوت ❳":
     chats = await get_served_users(client)
     chat = []
     for c in chats:
         chat.append(int(c["user_id"]))
     for i in chat:
         try:
           i = i
           m = await client.send_message(chat_id=i, text=text)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
         except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
         except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ اذاعه للمستخدمين بالمساعد ❳":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         if i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await client.send_message(chat_id=i.chat.id, text=text)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
          except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
          except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه عام بالبوت ❳":
     chats = await get_served_chats(client)
     users = await get_served_users(client)
     chat = []
     for user in users:
         chat.append(int(user["user_id"]))
     for c in chats:
         chat.append(int(c["chat_id"]))
     for i in chat:
         try:
           m = await client.forward_messages(i, y, x)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
         except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
         except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه عام بالمساعد ❳":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         try:
           m = await client.forward_messages(
               chat_id=i.chat.id,
               from_chat_id=message.chat.username,
               message_ids=int(x),
               )
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
         except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
         except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه للمجموعات بالبوت ❳":
     chats = await get_served_chats(client)
     chat = []
     for user in chats:
         chat.append(int(user["chat_id"]))
     for i in chat:
         try:
           m = await client.forward_messages(i, y, x)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
         except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
         except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه للمجموعات بالمساعد ❳":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         if not i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await client.forward_messages(i.chat.id, y, x)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
          except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
          except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه للمستخدمين بالبوت ❳":
     chats = await get_served_users(client)
     chat = []
     for c in chats:
         chat.append(int(c["user_id"]))
     for i in chat:
         try:
           m = await client.forward_messages(i, y, x)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
         except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
         except Exception as e:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")
   elif command == "❲ توجيه للمستخدمين بالمساعد ❳":
     client = await get_userbot(bot_username)
     async for i in client.get_dialogs():
         if i.chat.type == enums.ChatType.PRIVATE:
          try:
           m = await client.forward_messages(i.chat.id, y, x)
           dn += 1
           if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
          except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
          except:
                    fd += 1
                    continue
     return await message.reply_text(f"**≭︰تم اذاعه الرساله**\n\n**≭︰الارسال الناجح ↫ ❲ {dn} ❳**\n**≭︰الارسال الفاشل ↫ ❲ {fd} ❳**")

# قسم التحكم ف المساعد


@Client.on_message(filters.command("❲ اعدادات الحساب المساعد ❳", ""))
async def helpercn(client, message):
   bot_username = client.me.username
   dev = await get_dev(bot_username) 
   userbot = await get_userbot(bot_username)
   me = userbot.me 
   i = f"≭︰المعرف ↫ ❲ @{me.username} ❳\n≭︰الايدي ↫ ❲ {me.id} ❳" if me.username else me.id
   b = await client.get_chat(me.id)
   b = b.bio if b.bio else "لا يوجد بايو"
   if message.chat.id == dev or message.chat.username in OWNER:
    kep = ReplyKeyboardMarkup([["❲ احصائيات المساعد ❳"], ["❲ تغيير الاسم الثاني ❳", "❲ تغيير الاسم الاول ❳"], ["❲ تغيير المعرف ❳"], ["❲ تغيير النبذه ❳"], ["❲ مسح الصوره ❳", "❲ تعيين الصوره ❳"], ["❲ انضمام المساعد لمجموعه ❳"], ["❲ القائمه الرئيسيه ❳"]], resize_keyboard=True)
    await message.reply_text(f"**≭︰مرحبا بك عزيزي المطور \n≭︰اليك كيبورد اوامر المساعد\n\n≭︰الاسم ↫❲ {me.mention} ❳\n{i}\n≭︰النبذه ↫ ❲ {b} ❳**", reply_markup=kep)
   


@Client.on_message(filters.command("❲ احصائيات المساعد ❳", ""))
async def userrrrr(client: Client, message):
   bot_username = client.me.username
   dev = await get_dev(bot_username)
   if message.chat.id == dev or message.chat.username in OWNER:
    client = await get_userbot(bot_username)
    mm = await message.reply_text("Collecting stats")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh = client.me
    usere = Meh.mention
    async for dialog in client.get_dialogs():
        type = dialog.chat.type
        if enums.ChatType.PRIVATE == type:
            u += 1
        elif enums.ChatType.BOT == type:
            b += 1
        elif enums.ChatType.GROUP == type:
            g += 1
        elif enums.ChatType.SUPERGROUP == type:
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status == enums.ChatMemberStatus.ADMINISTRATOR or user_s.status == enums.ChatMemberStatus.OWNER:
                a_chat += 1
        elif enums.ChatType.CHANNEL == type:
            c += 1
        else:
          print(type)

    end = datetime.now()
    ms = (end - start).seconds
    await mm.edit_text(
        """**≭︰اليك احصائيات المساعد مفصله ↯.**

≭︰**تم الرد في ↫ ❲ {} ❳ ثانيه**
≭︰**عدد محادثات الخاص ↫ ❲ {} ❳ **
≭︰**عدد الكروبات العاديه ↫ ❲ {} ❳**
≭︰**عدد الكروبات السوبر↫ ❲ {} ❳**
≭︰**عدد القنوات فالحساب↫ ❲ {} ❳**
≭︰**عدد المجموعات الادمن فيها↫ ❲ {} ❳**
≭︰**عدد البوتات فالحساب ↫ ❲ {} ❳**
≭︰**هذه احصائيات↫ ❲ {} ❳**""".format(
            ms, u, g, sg, c, a_chat, b, usere
        )
    )

@Client.on_message(filters.command("❲ تغيير الاسم الاول ❳", ""))
async def changefisrt(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username in OWNER:
   try:
    name = await client.ask(message.chat.id, "≭︰ارسل الاسم الجديد")
    name = name.text
    client = await get_userbot(bot_username)
    await client.update_profile(first_name=name)
    await message.reply_text("**≭︰تم تغيير اسم المساعد**")
   except Exception as es:
     await message.reply_text(f"≭︰حدثت مشكله في تغيير الاسم \n {es}")


@Client.on_message(filters.command("❲ تغيير الاسم الثاني ❳", ""))
async def changelast(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username in OWNER:
   try:
    name = await client.ask(message.chat.id, "≭︰ارسل الاسم الجديد")
    name = name.text
    client = await get_userbot(bot_username)
    await client.update_profile(last_name=name)
    await message.reply_text("**≭︰تم تغيير اسم المساعد**")
   except Exception as es:
     await message.reply_text(f"≭︰حدثت مشكله في تغيير الاسم \n {es}")


@Client.on_message(filters.command("❲ تغيير النبذه ❳", ""))
async def changebio(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username in OWNER:
   try:
    name = await client.ask(message.chat.id, "≭︰ارسل النبذه الجديده")
    name = name.text
    client = await get_userbot(bot_username)
    await client.update_profile(bio=name)
    await message.reply_text("**≭︰تم تغيير نبذه المساعد**")
   except Exception as es:
     await message.reply_text(f"≭︰حدثت مشكله في تغيير النبذه \n {es}")


@Client.on_message(filters.command("❲ تغيير المعرف ❳", ""))
async def changeusername(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username in OWNER:
   try:
    name = await client.ask(message.chat.id, "≭︰ارسل المعرف الجديد")
    name = name.text
    client = await get_userbot(bot_username)
    await client.set_username(name)
    await message.reply_text("**≭︰تم تغيير معرف المساعد**")
   except Exception as es:
     await message.reply_text(f"≭︰حدثت مشكله في تغيير المعرف \n {es}")


@Client.on_message(filters.command(["❲ تعيين الصوره ❳"], ""))
async def changephoto(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username in OWNER:
   try:
    m = await client.ask(message.chat.id, "≭︰ارسل الصوره الجديده")
    photo = await m.download()
    client = await get_userbot(bot_username)
    await client.set_profile_photo(photo=photo)
    await message.reply_text("**≭︰تم تغيير صوره المساعد**") 
   except Exception as es:
     await message.reply_text(f"≭︰حدثت مشكله في تغيير الصوره \n {es}")

@Client.on_message(filters.command(["❲ مسح الصوره ❳"], ""))
async def changephotos(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username in OWNER:
       try:
        client = await get_userbot(bot_username)
        photos = await client.get_profile_photos("me")
        await client.delete_profile_photos([p.file_id for p in photos[1:]])
        await message.reply_text("**≭︰تم مسح صوره المساعد**")
       except Exception as es:
         await message.reply_text(f"≭︰حدثت مشكله في مسح الصوره \n {es}")


@Client.on_message(filters.command("❲ انضمام المساعد لمجموعه ❳", ""))
async def joined(client: Client, message):
  bot_username = client.me.username
  dev = await get_dev(bot_username)
  if message.chat.id == dev or message.chat.username in OWNER:
   try:
    name = await client.ask(message.chat.id, "≭︰ارسل رابط الكروب للانضمام")
    name = name.text
    if "https" in name: 
     if not "+" in name: 
       name = name.replace("https://t.me/", "")
    client = await get_userbot(bot_username)
    await client.join_chat(name)
    await message.reply_text("**≭︰تم انضمام المساعد للكروب**")
   except Exception as es:
     await message.reply_text(f"≭︰حدثت مشكله في انضمام المساعد \n {es}")



@Client.on_message(filters.command(["❲ تغيير مكان الاشعارات ❳", "❲ تفعيل الاشعارات ❳", "❲ تعطيل الاشعارات ❳"], ""))
async def set_history(client: Client, message):
 bot_username = client.me.username
 dev = await get_dev(bot_username)
 if message.chat.id == dev or message.chat.username in OWNER:
  if message.command[0] == "❲ تغيير مكان الاشعارات ❳":
   ask = await client.ask(message.chat.id, "**≭︰ارسل ايدي الكروب او القناة**", timeout=30)
   logger = ask.text
   if "@" in logger:
     logger = logger.replace("@", "")
  Botts = Bots.find({})
  for i in Botts:
      bot = client.me
      if i["bot_username"] == bot.username:
        dev = i["dev"]
        token = i["token"]
        session = i["session"]
        bot_username = i["bot_username"]
        loogger = i["logger"]
        logger_mode = i["logger_mode"]
        if message.command[0] == "❲ تغيير مكان الاشعارات ❳":
         if i["logger"] == logger:
           return await ask.reply_text("**≭︰تم تعيين هذا المكان فعلا**")
         else:
          try:
           user = await get_userbot(bot_username)
           await client.send_message(logger, "**≭︰انتظر قليلا**")
           await user.send_message(logger, "**≭︰جاري تغيير مكان اشعارات التشغيل**")
           d = {"bot_username": bot_username}
           Bots.delete_one(d)
           asyncio.sleep(2)
           aha = {"bot_username": bot_username, "token": token, "session": session, "dev": dev, "logger": logger, "logger_mode": logger_mode}
           Bots.insert_one(aha)
           log[bot_username] = logger
           await ask.reply_text("**≭︰تم تعيين مكان اشعارات التشغيل الجديد**")
          except Exception:
            await ask.reply_text("**تاكد ان البوت والحساب المساعد مشرفين**")
        else:
         mode = "ON" if message.command[0] == "❲ تفعيل الاشعارات ❳" else "OFF"
         if i["logger_mode"] == mode:
           m = "مفعله" if message.command[0] == "❲تفعيل الاشعارات ❳" else "معطله"
           return await message.reply_text(f"**≭︰الاشعارات {m} فعلا**")
         else:
          try:
           hh = {"bot_username": bot_username}
           Bots.delete_one(hh)
           h = {"bot_username": bot_username, "token": token, "session": session, "dev": dev, "logger": loogger, "logger_mode": mode}
           Bots.insert_one(h)
           logm[bot_username] = mode
           m = "تفعيل" if message.command == "❲ تفعيل الاشعارات ❳" else "تعطيل"
           await message.reply_text(f"**≭︰تم {m} الاشعارات**")
          except Exception as es:
            await message.reply_text("**≭︰حدثت مشكله راسل المبرمج**")
