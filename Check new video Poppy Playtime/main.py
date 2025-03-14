#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Poppy Playtime.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    SavedModeEnum,
    get_yt_playlist_video_list,
    run_notification_job,
)


run_notification_job(
    "Poppy Playtime",
    DIR,
    lambda _: get_yt_playlist_video_list("PLejGw9J2xE9XXoMpS8xOPmkuzriJxyINS"),
    save_mode=SavedModeEnum.DATA_ITEM,
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
