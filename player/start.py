from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup 

@Client.on_message(filters.command("start"))
async def start(client, m: Message):
   if m.chat.type == 'private':
       await m.reply(f"**Just testing some drugs given by** @Inches_8 \n**To use it:-** __ \nYou Got this, no need of help\n**Commands** : \n`/stream` \n`/stop`",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                     InlineKeyboardButton(
                                            "TestStream", url="t.me/joinchat/CwwOb62gbX8yYzcx")
                                    ]]
                            ))
   else:
      await m.reply("**live! ✨**")
