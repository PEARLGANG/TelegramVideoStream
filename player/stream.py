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
process = None
app = Client(SESSION_NAME, API_ID, API_HASH)
group_call = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()
video = []

ydl_opts = {
    "geo-bypass": True,
    "nocheckcertificate": True
    }
ydl = YoutubeDL(ydl_opts)
links=[]
def mp4_converter(source, output):
    return subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            source,
            "-c",
            "copy",
            "-bsf:a",
            "aac_adtstoasc",
            output,
        ],
        stdin=None,
        stdout=None,
        stderr=None,
        cwd=None,
    )

@Client.on_message(filters.command("stream"))
async def stream(client, m: Message):
        global process
        msg = await m.reply("`Firing The Stream!`")
        try:
            #meta = ydl.extract_info(STREAM_URL, download=False)
            #formats = meta.get('formats', [meta])
           # for f in formats:
                #links.append(f['url'])
                #finalurl=links[-1]
            #print(finalurl)
           # file = f"dr.mkv"
            #process = mp4_converter(finalurl, file)
            #await asyncio.sleep(5) 
            await group_call.join(m.chat.id)
            await group_call.start_video(STREAM_URL)
            await msg.edit("**Streaming!**")         
        except Exception as e:
            await msg.edit(f"**🚫 Error** - `{e}`")

@Client.on_message(filters.command("stop"))
async def stopvideo(client, m: Message):
    global process
    try:
        #process.terminate()
        await group_call.stop()
        await m.reply("**K Stopped!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")

