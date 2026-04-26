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
    get_vkvideo_video_list,
)

run_notification_job(
    "Сашка Кроп MHz'ы [vkvideo]",
    DIR,
    lambda _: get_vkvideo_video_list("https://vkvideo.ru/playlist/-60916056_2"),
    save_mode=SavedModeEnum.DATA_ITEM,
    formats=FORMATS_VIDEO,
)
