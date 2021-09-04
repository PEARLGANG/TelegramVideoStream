import os
import asyncio
import subprocess 
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME, STREAM_URL
import schedule 
import time 
VIDEO_CALL = {}

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()
process = None

def raw_converter(source, output):
    return subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-i",
            source,
            "-f",
            "s16le",
            "-ac",
            "2",
            "-ar",
            "48000",
            "-acodec",
            "pcm_s16le",
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
            stream_url = STREAM_URL
            file = f"stream(m.chat.id).raw"
            #process = raw_converter(stream_url, file)
            #await asyncio.sleep(5) 
            await group_call.start(m.chat.id)
            group_call.start_video(stream_url)
            #await group_call.set_video_capture(stream_url)
            await msg.edit("**Streaming!**")
        except Exception as e:
            await msg.edit(f"**🚫 Error** - `{e}`")

@Client.on_message(filters.command("stop"))
async def stopvideo(client, m: Message):
    global process
    try:
        process.terminate()
        await group_call.stop()
        await m.reply("**K Stopped!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")

