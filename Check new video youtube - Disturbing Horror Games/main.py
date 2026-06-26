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

from root_common import (
    DataItem,
    NotificationJob,
    get_yt_video_list,
    run_notification_job_youtube,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    # Не всегда вовремя в плейлист кладет, поэтому для актуальности брать со страницы
    url = "https://www.youtube.com/@DisturbingHorrorGames/videos"
    return [item for item in get_yt_video_list(url) if "DHG #" in item.title]


run_notification_job_youtube(
    "Disturbing Horror Games",
    DIR,
    get_items,
)
