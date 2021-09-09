import os
from pyrogram import Client
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from pyrogram.utils import MAX_CHANNEL_ID
from config import instances, queues, to_delete







class Player:
    def __init__(self, chat_id):
        self._current_chat = chat_id
        if instances.get(chat_id):
            self.group_call = instances[chat_id].get('instance')
        else:
            _client = GroupCallFactory(UB, mtproto_backend=GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
            self.group_call = _client.get_file_group_call()
            instances[chat_id] = {'instance': self.group_call}

    async def startCall(self):
        if not self.group_call.is_connected:
            try:
                self.group_call.on_network_status_changed(self.on_network_changed)
                self.group_call.on_playout_ended(self.playout_ended_handler)
                await self.group_call.start(self._current_chat)
            except Exception as e:
                return False, e
        return True, None

    async def on_network_changed(self, group_call, is_connected):
        chat_id = MAX_CHANNEL_ID - group_call.full_chat.id
        if is_connected:
            instances[self._current_chat]['is_active'] = True
            await Client.send_message(chat_id, 'Successfully joined!')
        else:
            instances[self._current_chat]['is_active'] = True
            try:
                os.remove(group_call._GroupCallFile__input_filename)
            except BaseException:
                pass
            await Client.send_message(chat_id, 'Disconnected from voice chat..')

    async def playout_ended_handler(self, call, __):
        try:
            for i in to_delete:
                print(f"Deleting {i}")
                to_delete.remove(i)
                os.remove(i)
            os.remove(call._GroupCallFile__input_filename)
        except BaseException:
            pass
        info = queues.get(self._current_chat)
        if info:
            file, is_path, req_user = info
            await self.play_file(file, is_path)
            await Client.send_message(
                self._current_chat,
                "🎧 **Now playing:**  {}\n👤 **Requested by:** {}".format(
                    file.video.file_name if is_path else file,  req_user.mention(style='md')
                ),
            )
        else:
            await self.leave_vc()

    async def play_file(self, file, is_path=False):
        global to_delete
        group_call = self.group_call
        width = None
        height = None
   
        try:
            os.mkfifo(audio)
        except FileExistsError:
            ... # will not happen btw
 
        if not audio:
            return False, "Couldn't fetch audio from file!"
        await group_call.start_video(file, width=width, height=height)
        return True, None

    async def play_or_queue(self, vid, m: Message, is_path=False):
        anything = queues.get(self._current_chat, False)
        if not anything and not self.group_call.is_connected:
            suc, err = await self.play_file(vid, is_path)
            if not suc:
                await Client.send_message(self._current_chat, str(err))
            return True     
        else:
            data = [vid, is_path, m.from_user]
            pos = queues.add(self._current_chat, data)
            await m.reply(f"Added to queue #{pos}")
            return False
            
    async def leave_vc(self):
        global to_delete
        await self.group_call.stop()
        del instances[self._current_chat]
        try:
            for i in to_delete:
                print(f"Deleting {i}")
                to_delete.remove(i)
                os.remove(i)
        except BaseException:
            pass

    async def join_vc(self):
        success, err = await self.startCall()
        if success:
            return True
        await Client.send_message(
            self._current_chat, f"An error occured\n`{err}`"
        )
        return False

