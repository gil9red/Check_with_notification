#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео SMILE FACE.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    DataItem,
    NotificationJob,
    get_yt_video_list,
    run_notification_job_youtube,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    items: list[DataItem] = []
    for url in [
        "https://www.youtube.com/@SMILEFACEru/videos",
        "https://www.youtube.com/@SFArchive/videos",
    ]:
        items += get_yt_video_list(url)
    return items


run_notification_job_youtube(
    "SMILE FACE",
    DIR,
    get_items,
    formats=FORMATS_VIDEO.replace(
        prefix="🎭",
    ),
)
