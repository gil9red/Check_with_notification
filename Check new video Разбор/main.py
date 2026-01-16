#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "Разбор".

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    run_notification_job,
    SavedModeEnum,
    get_yt_playlist_video_list,
)

run_notification_job(
    "Разбор",
    DIR,
    lambda _: get_yt_playlist_video_list("PLL1mBUdBcoHqu83JI3TDDauDD4pi3-pF6"),
    save_mode=SavedModeEnum.DATA_ITEM,
    formats=FORMATS_VIDEO.replace(
        prefix="🪽",
    ),
)
