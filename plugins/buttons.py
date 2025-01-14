import json
import re
import requests
import utils
import yt_dlp
from plugins.jiodl import *
from plugins.gdrive import *
import subprocess
from pyrogram import Client, filters, idle
from urllib import parse
import logging
import os
from plugins.handler.playback import *
from plugins.ytdl import *
from plugins.handler.mhandler import *
from plugins.dl import *
from plugins.exec import *
from plugins.jio import *
from plugins.dash import *

from base64 import b64decode, b64encode
from yt_dlp.postprocessor import PostProcessor
from utils import scriptsDir, joinPath, realPath
from asyncio import create_subprocess_exec, create_subprocess_shell, run_coroutine_threadsafe, sleep
#from button import ButtonMaker
LOG_FILE = "log.txt"
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %I:%M:%S %p",
    level=logging.INFO,
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
def atos(func, *args, wait=True, **kwargs):
    future = run_coroutine_threadsafe(func(*args, **kwargs), bot_loop)
    return future.result() if wait else future
import os
#from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
configPath = joinPath(scriptsDir, 'config.json')
if not utils.isExist(configPath):
    utils.copyFile(joinPath(scriptsDir, 'config.def'), configPath)

# Some important variables
default_res = ""
default_strm = ''
config = utils.JSO(configPath, 4)
sudo_users = [7126874550, -1002273935741, 6209057258, 1596559467, 7361945688, 1195351595]

class ButtonMaker:
    def __init__(self):
        self.__button = []
        self.__header_button = []
        self.__first_body_button = []
        self.__last_body_button = []
        self.__footer_button = []

    def ubutton(self, key, link, position=None):
        if not position:
            self.__button.append(InlineKeyboardButton(text=key, url=link))
        elif position == 'header':
            self.__header_button.append(InlineKeyboardButton(text=key, url=link))
        elif position == 'f_body':
            self.__first_body_button.append(InlineKeyboardButton(text=key, url=link))
        elif position == 'l_body':
            self.__last_body_button.append(InlineKeyboardButton(text=key, url=link))
        elif position == 'footer':
            self.__footer_button.append(InlineKeyboardButton(text=key, url=link))

    def ibutton(self, key, data, position=None):
        if not position:
            self.__button.append(InlineKeyboardButton(text=key, callback_data=data))
        elif position == 'header':
            self.__header_button.append(InlineKeyboardButton(text=key, callback_data=data))
        elif position == 'f_body':
            self.__first_body_button.append(InlineKeyboardButton(text=key, callback_data=data))
        elif position == 'l_body':
            self.__last_body_button.append(InlineKeyboardButton(text=key, callback_data=data))
        elif position == 'footer':
            self.__footer_button.append(InlineKeyboardButton(text=key, callback_data=data))

    def build_menu(self, b_cols=1, h_cols=8, fb_cols=2, lb_cols=2, f_cols=8):
        menu = [self.__button[i:i+b_cols]
                for i in range(0, len(self.__button), b_cols)]
        if self.__header_button:
            if len(self.__header_button) > h_cols:
                header_buttons = [self.__header_button[i:i+h_cols]
                                  for i in range(0, len(self.__header_button), h_cols)]
                menu = header_buttons + menu
            else:
                menu.insert(0, self.__header_button)
        if self.__first_body_button:
            if len(self.__first_body_button) > fb_cols:
                [menu.append(self.__first_body_button[i:i+fb_cols])
                 for i in range(0, len(self.__first_body_button), fb_cols)]
            else:
                menu.append(self.__first_body_button)
        if self.__last_body_button:
            if len(self.__last_body_button) > lb_cols:
                [menu.append(self.__last_body_button[i:i+lb_cols])
                 for i in range(0, len(self.__last_body_button), lb_cols)]
            else:
                menu.append(self.__last_body_button)
        if self.__footer_button:
            if len(self.__footer_button) > f_cols:
                [menu.append(self.__footer_button[i:i+f_cols])
                 for i in range(0, len(self.__footer_button), f_cols)]
            else:
                menu.append(self.__footer_button)
        return InlineKeyboardMarkup(menu)
