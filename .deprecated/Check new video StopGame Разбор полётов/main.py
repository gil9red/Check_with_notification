#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Разбора полётов.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job, get_yt_playlist_video_list, SavedModeEnum


run_notification_job(
    "Разбор полётов [StopGame]",
    DIR,
    lambda _: get_yt_playlist_video_list("PLZfhqd1-Hl3BKhWwCgmqtENSlearqLlAV"),
    save_mode=SavedModeEnum.DATA_ITEM,
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
