#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео плейлиста DeadP47 - Худшие Стримеры.

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
    "Худшие Стримеры [DeadP47]",
    DIR,
    lambda _: get_yt_playlist_video_list("PLjdELgpd9M1uzBrb3yNsVM5-t2x7zBBLA"),
    save_mode=SavedModeEnum.DATA_ITEM,
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
