#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Кино Огонь - Полезность персонажей

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    run_notification_job,
    SavedModeEnum,
    get_yt_video_list,
    DataItem,
    NotificationJob,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    url = "https://www.youtube.com/@kinoogon/search?query=полезность полезный"
    return [item for item in get_yt_video_list(url) if "полезн" in item.title.lower()]


run_notification_job(
    "Кино Огонь",
    DIR,
    get_items,
    save_mode=SavedModeEnum.DATA_ITEM,
    formats=FORMATS_VIDEO,
)
