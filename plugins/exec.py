from asyncio import create_subprocess_exec, create_subprocess_shell, run_coroutine_threadsafe
from asyncio.subprocess import PIPE
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import InputMediaPhoto
from pyrogram.errors import ReplyMarkupInvalid, FloodWait, PeerIdInvalid, ChannelInvalid, RPCError, UserNotParticipant, MessageNotModified, MessageEmpty, PhotoInvalidDimensions, WebpageCurlFailed, MediaEmpty
from plugins.dl import *
from plugins.jio import *
from plugins.dash import *
##from plugins.handler.playback import *
#from plugins.handler.mhandler import* 
#from plugins.ytdl import *
#from asyncio import sleep

from random import choice as rchoice
from time import time
from re import match as re_match


async def sendFile(message, file, caption=None, buttons=None):
    try:
        return await message.reply_document(document=file, quote=True, caption=caption, disable_notification=True, reply_markup=buttons)

    except Exception as e:
       # LOGGER.error(str(e))
        return str(e)

async def sendMessage(message, text, buttons=None, photo=None, **kwargs):
    try:
        return await message.reply(text=text, quote=True, disable_web_page_preview=True, disable_notification=True,
                                    reply_markup=buttons, reply_to_message_id=rply.id if (rply := message.reply_to_message) and not rply.text and not rply.caption else None,
                                    **kwargs)

    except Exception as e:
     #   LOGGER.error(format_exc())
        return str(e)

async def cmd_exec(cmd, shell=False):
    
    if shell:
        proc = await create_subprocess_shell(cmd, stdout=PIPE, stderr=PIPE)
    else:
        proc = await create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate()
    stdout = stdout.decode().strip()
    stderr = stderr.decode().strip()
    return stdout, stderr, proc.returncode
