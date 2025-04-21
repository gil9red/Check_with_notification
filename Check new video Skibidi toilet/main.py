#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Skibidi toilet.

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
    # Не всегда вовремя в плейлист кладет, поэтому для актуальности брать со страницы
    url = "https://www.youtube.com/@DaFuqBoom/videos"
    return [
        item
        for item in get_yt_video_list(url, maximum_items=100)
        if "skibidi toilet" in item.title.lower()
    ]


run_notification_job(
    "Skibidi toilet",
    DIR,
    get_items,
    save_mode=SavedModeEnum.DATA_ITEM,
    formats=FORMATS_VIDEO.replace(
        prefix="🚽",
    ),
)
