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

from root_common import (
    DataItem,
    NotificationJob,
    get_vkvideo_video_list,
    run_notification_job_vkvideo,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    url = "https://vkvideo.ru/@stopgameru/all"
    return [
        item
        for item in get_vkvideo_video_list(url)
        if "Разбор полётов" in item.title or "История серии" in item.title
    ]


run_notification_job_vkvideo(
    "StopGame",
    DIR,
    get_items,
)
