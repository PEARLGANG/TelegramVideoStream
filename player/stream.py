import os
import asyncio
import subprocess 
import schedule 
import time
import pafy
from youtube_search import YoutubeSearch
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME, STREAM_URL
from streamlit import caching
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
    #global process
    try:
        media = m.reply_to_message
        if not media and not ' ' in m.text:
            await m.reply("Neither YT Link Nor Media? Kek=fuck.off()!")

        elif ' ' in m.text:
            msg = await m.reply("`Firing The Stream!`")
            text = m.text.split(' ', 1)
            url = text[1]
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            video = pafy.new(link)
            video_source = video.getbest().url
            #file = f"dr.mkv"
            #process = mp4_converter(finalurl, file)
            await asyncio.sleep(5) 
            await group_call.join(m.chat.id)
            await group_call.start_video(videosource)
            await msg.edit("**Streaming!**")  
        
        elif media.video or media.document:
            msg = await m.reply_text("`Trying to Stream the File...`")    
            video = await client.download_media(media)
            await group_call.start(m.chat.id)
            await group_call.start_video(video, 1280, 720, 20)
            await msg.edit("**Streaming!**")  

    except Exception as e:
        await msg.edit(f"**🚫 Error** - `{e}`")

@Client.on_message(filters.command("live"))
async def live(client, m: Message):
        msg = await m.reply("`Firing The Stream!`")
        try:
            await group_call.join(m.chat.id)
            await group_call.start_video(STREAM_URL)
            await msg.edit("**Stream Is Live!**")         
        except Exception as e:
            await msg.edit(f"**🚫 Error** - `{e}`")           
            
            
@Client.on_message(filters.command("stop"))
async def stopvideo(client, m: Message):
    #global process
    try:
        #process.terminate()
        await group_call.stop()
        caching.clear_cache()
        await m.reply("**K Stopped!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")

@Client.on_message(filters.command("lstop"))
async def stoplive(client, m: Message):
    try:
        await group_call.stop()
        caching.clear_cache()
        await m.reply("**K Live Stopped!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")
