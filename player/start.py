from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup 

@Client.on_message(filters.command("start"))
async def start(client, m: Message):
   if m.chat.type == 'private':
       await m.reply(f"**Hey, I'm VideoChat Streamer developed by** @Inches_8 \n\n**To use it:-** __ \n1) Add this Bot to your Group and Make it Admin \n2) Add__ Assistant __to your Group__ \n3) **Commands** : \n`/stream` \n`/stop`",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                     InlineKeyboardButton(
                                            "TestStream", url="t.me/joinchat/CwwOb62gbX8yYzcx")
                                    ]]
                            ))
   else:
      await m.reply("**live! ✨**")
