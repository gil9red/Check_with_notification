#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео John Kalligan - Умеет ли петь.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    DataItem,
    SavedModeEnum,
    NotificationJob,
    get_yt_video_list,
    get_yt_playlist_video_list,
    run_notification_job,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    # Не всегда вовремя в плейлист кладет, поэтому для актуальности брать со страницы
    items: list[DataItem] = [
        item
        for item in get_yt_video_list(
            "https://www.youtube.com/@JohnKalligan/videos",
            maximum_items=100,
        )
        if "умеет" in item.title.lower() and "петь" in item.title.lower()
    ]

    # Некоторые видео в плейлисте не имеют шаблона по названию
    for video in get_yt_playlist_video_list("PLhNsPPGFrZoquxBDlDTl50XrajwG8Bo5j"):
        if video not in items:
            items.append(video)

    return items


run_notification_job(
    "Умеет ли петь [John Kalligan] [Youtube]",
    DIR,
    get_items,
    save_mode=SavedModeEnum.DATA_ITEM,
    formats=FORMATS_VIDEO.replace(
        prefix="🎵",
    ),
)
