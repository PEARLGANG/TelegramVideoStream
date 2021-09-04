import os
import asyncio
import subprocess 
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME, STREAM_URL
import schedule 
import time 
from youtube_dl import YoutubeDL

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()


ydl_opts = {
    "geo-bypass": True,
    "nocheckcertificate": True
    }
ydl = YoutubeDL(ydl_opts)
links=[]

@Client.on_message(filters.command("stream"))
async def stream(client, m: Message):
        msg = await m.reply("`Firing The Stream!`")
        try:
            if " " in m.text:
                text = m.text.split(" ", 1)  
                meta = ydl.extract_info(text, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                    links.append(f['url'])
                    finalurl=links[-1]
                print(finalurl)
            await group_call.join(m.chat.id)
            await group_call.start_video(finalurl)
            await msg.edit("**Streaming!**")
        except Exception as e:
            await msg.edit(f"**🚫 Error** - `{e}`")

@Client.on_message(filters.command("stop"))
async def stopvideo(client, m: Message):
    try:
        await group_call.stop()
        await m.reply("**K Stopped!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")

