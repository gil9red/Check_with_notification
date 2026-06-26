#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Разбора полётов и Истории серий на канале StopGame.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    DataItem,
    NotificationJob,
    run_notification_job_youtube,
    get_yt_video_list,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    url = "https://www.youtube.com/@StopGameRu/videos"
    return [
        item
        for item in get_yt_video_list(url)
        if "Разбор полётов" in item.title or "История серии" in item.title
    ]


run_notification_job_youtube(
    "StopGame",
    DIR,
    get_items,
)
