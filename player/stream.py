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
group_call = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_file_group_call()
process = None
#video = None
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
def mp4_converter(source, output):
    return subprocess.Popen(
        [
            "ffmpeg",
            source,
            "-c",
            "copy",
            output,
        ],
        stdin=None,
        stdout=None,
        stderr=None,
        cwd=None,
    )
@Client.on_message(filters.command("livestream"))
async def stream(client, m: Message):
        global process
        global video
        msg = await m.reply("`Firing The Stream!`")
        try:
            stream_url = STREAM_URL
            try:
                stream_url = m.text.split(' ', 1)[1]
            except IndexError:
                ...
            file = f"stream(m.chat.id).raw"
            mp4 = f"output.mp4"
            process = raw_converter(stream_url, file)
            #video = mp4_converter(stream_url, mp4)
            await asyncio.sleep(5)
            await group_call.start(m.chat.id)
            group_call.input_filename = file
            await group_call.set_video_capture(stream_url)
            VIDEO_CALL[m.chat.id] = group_call
            await msg.edit("**Streaming!**")
        except Exception as e:
            await msg.edit(f"**🚫 Error** - `{e}`")

@Client.on_message(filters.command("stoplive"))
async def stopvideo(client, m: Message):
    global process
    #global video
    try:
        process.terminate()
        #video.terminate()
        await VIDEO_CALL[m.chat.d].stop()
        await m.reply("**K Stopped!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")






Client.on_message(filters.command("vstream"))
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        await m.reply("**Give me a video to stream*")
    elif replied.video or replied.document:
        msg = await m.reply("📥 **Downloading**")
        chat_id = m.chat.id
        try:
            video = await client.download_media(m.reply_to_message)
            os.system(f'ffmpeg -i "{video}" -vn -f s16le -ac 2 -ar 48000 -acodec pcm_s16le -filter:a "atempo=0.81" vid-{chat_id}.raw -y')
        except Exception as e:
            await msg.edit(f"**🚫 Error** - `{e}`")
        await asyncio.sleep(5)
        try:
            group_call = group_call_factory.get_file_group_call(f'vid-{chat_id}.raw')
            await group_call.start(chat_id)
            await group_call.set_video_capture(video, repeat=False)
            VIDEO_CALL[chat_id] = group_call
            await msg.edit("💡 **video streaming started!**\n\n» **join to video chat to watch the video.**")
        except Exception as e:
            await msg.edit(f"**Error** -- `{e}`")
    else:
        await m.reply("**¶lay wot my ass?**")

@Client.on_message(filters.command("vstop"))
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply(" **Ended Vstream!")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")
