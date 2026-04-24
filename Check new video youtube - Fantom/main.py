#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Fantom.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    SavedModeEnum,
    get_yt_video_list,
    run_notification_job,
)


run_notification_job(
    "Fantom",
    DIR,
    lambda _: get_yt_video_list(
        "https://www.youtube.com/@YaFanTom/videos",
        maximum_items=100,
    ),
    save_mode=SavedModeEnum.DATA_ITEM,
    formats=FORMATS_VIDEO.replace(
        prefix="👻",
    ),
)
