#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Disturbing Horror Games.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    run_notification_job,
    SavedModeEnum,
    get_playlist_video_list,
    DataItem,
    NotificationJob,
)


# NOTE: Нужна фильтрация, чтобы оставить только нужные видео
#       Т.к. в плейлисте иногда попадают видео типа "Klasky Csupo in Pixitracker Major 9312"
def get_items(_: NotificationJob) -> list[DataItem]:
    return [
        item
        for item in get_playlist_video_list("PLVOZT4ssBLx7d4TSZuYU_lkRwAUaON3FI")
        if "DHG #" in item.title
    ]


run_notification_job(
    "Disturbing Horror Games",
    DIR,
    get_items,
    save_mode=SavedModeEnum.DATA_ITEM,
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
