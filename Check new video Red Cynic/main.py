#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Red Cynic.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    SavedModeEnum,
    get_playlist_video_list,
    run_notification_job,
)


run_notification_job(
    "Обзоры Red Cynic",
    DIR,
    lambda _: get_playlist_video_list("PLBoSqopCxgMm6fRnlgL_BTYT9Jy8iciG9"),
    save_mode=SavedModeEnum.DATA_ITEM,
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
