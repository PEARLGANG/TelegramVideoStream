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

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()
DATA = {}

@Client.on_message(filters.command("stream"))
async def stream(client, m: Message):
    try:
        msg = await m.reply("`Firing The Stream!`")
        media = m.reply_to_message
        gc = DATA.get(m.chat.id)
        if gc is None:
            DATA[m.chat.id] = group_call
        
        if not media and not ' ' in m.text:
            await msg.edit("Neither YT Link Nor Media? Kek=fuck.off()!")

        elif ' ' in m.text:
            text = m.text.split(' ', 1)
            url = text[1]
            results = YoutubeSearch(url, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            video = pafy.new(link)
            video_source = video.getbest().url
            await asyncio.sleep(5) 
            await group_call.join(m.chat.id)
            await group_call.start_video(video_source, enable_experimental_lip_sync=True)
            await msg.edit("**Streaming!**")  
        
        elif media.video or media.document:
            msg = await m.reply_text("`Trying to Stream the File...`")    
            video = await client.download_media(media)
            await group_call.start(m.chat.id)
            await group_call.start_video(video, enable_experimental_lip_sync=True)
            await msg.edit("**Streaming!**")  

    except Exception as e:
        await msg.edit(f"**🚫 Error** - `{e}`")

@Client.on_message(filters.command("live"))
async def live(client, m: Message):
        gc = DATA.get(m.chat.id)
        if gc is None:
            DATA[m.chat.id] = group_call
        msg = await m.reply("`Firing The Stream!`")
        try:
            await group_call.join(m.chat.id)
            await group_call.start_video(STREAM_URL, enable_experimental_lip_sync=True)
            await msg.edit("**Stream Is Live!**")         
        except Exception as e:
            await msg.edit(f"**🚫 Error** - `{e}`")           
            
            
@Client.on_message(filters.command("stop"))
async def stopvideo(client, m: Message):
    try:
        gc = DATA.get(m.chat.id)
        if gc:
            await group_call.stop()
            caching.clear_cache()
            await m.reply("**K Stopped!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")

@Client.on_message(filters.command("lstop"))
async def stoplive(client, m: Message):
    try:
        gc = DATA.get(m.chat.id)
        if gc:
            await group_call.stop()
            caching.clear_cache()
            await m.reply("**K Live Stopped!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")
