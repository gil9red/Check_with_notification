#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "Страшно, вырубай!" от Василия Гальперова.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import (
    DataItem,
    NotificationJob,
    SavedModeEnum,
    get_yt_video_list,
    run_notification_job,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    # Нет плейлиста
    url = "https://www.youtube.com/@frank129002/videos"
    return [
        item
        for item in get_yt_video_list(url)
        if "[Страшно, вырубай!]".upper() in item.title.upper()
    ]


run_notification_job(
    "Страшно, вырубай! [Василий Гальперов]",
    DIR,
    get_items,
    save_mode=SavedModeEnum.DATA_ITEM,
)
