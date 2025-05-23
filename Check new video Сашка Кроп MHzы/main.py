#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Сашка Кроп MHz'ы.

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
    "Сашка Кроп MHz'ы",
    DIR,
    lambda _: get_yt_playlist_video_list("PL24NJvgUw-cyZ6Mz25pAhMSa1l8uYLzo9"),
    save_mode=SavedModeEnum.DATA_ITEM,
    formats=FORMATS_VIDEO,
)
