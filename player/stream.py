import os
import asyncio
import subprocess 
import schedule 
import time
import pafy
from youtube_search import YoutubeSearch
from pytgcalls import GroupCallFactory
from pyrogram.utils import MAX_CHANNEL_ID
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME, STREAM_URL
from streamlit import caching
from player.queue import Queue
from player.acc import Player
app = Client(SESSION_NAME, API_ID, API_HASH)
group_call = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_group_call()

DATA = {}





@Client.on_message(filters.command("stream"))
async def stream(client, m: Message):
    try:
        player = Player(chat_id)
        msg = await m.reply("`Firing The Stream!`")
        media = m.reply_to_message
        is_file = False
        
        if not media and not ' ' in m.text:
            await msg.edit("Neither YT Link Nor Media? Kek=fuck.off()!")

        elif ' ' in m.text:
            text = m.text.split(' ', 1)
            url = text[1]
            results = YoutubeSearch(url, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            video = pafy.new(link)
            link = video.getbest().url
            is_file = False
            await asyncio.sleep(5) 
            await group_call.join(m.chat.id)
            p = await player.play_or_queue(link, m, is_file)
            await msg.edit("**Streaming!**" if p else "**Queued**")
        
        elif media.video or media.document:
            msg = await m.reply_text("`Trying to Stream the File...`")    
            link = await client.download_media(media)
            is_file = True
            await group_call.start(m.chat.id)
            p = await player.play_or_queue(link, m, is_file)
            await msg.edit("**Streaming!**" if p else "**Queued**")  

    except Exception as e:
        await msg.edit(f"**🚫 Error** - `{e}`")

@Client.on_message(filters.command("live"))
async def live(client, m: Message):
        player = Player(chat_id)
        is_file = False
        link = STREAM_URL
        msg = await m.reply("`Firing The Stream!`")
        try:
            await group_call.join(m.chat.id)
            await msg.edit("**Stream Is Live!**")    
            p = await player.play_or_queue(link, m, is_file)
            await msg.edit("**Streaming!**" if p else "**Queued**")  
     
        except Exception as e:
            await msg.edit(f"**🚫 Error** - `{e}`")           
            
            
@Client.on_message(filters.command("stop"))
async def stopvideo(client, m: Message):
    player = Player(chat_id)
    try:
        await player.leave_vc()
        await m.reply("**K Stopped!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")

