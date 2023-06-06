#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Лютый Задротер.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    DataItem,
    run_notification_job,
    get_playlist_video_list,
    NotificationJob,
)

NAME = "Лютый Задротер"


def get_video_list(_: NotificationJob) -> list[DataItem]:
    items = []
    for playlist_title, playlist_id in [
        (f"TES и Fallout", "PLI3zbIkPvOTdBlH4bV7WKxvon4IFMXYsX"),
        (f"Ревью", "PLI3zbIkPvOTcmCFoBwNj2T_WOG_wZYugZ"),
        (f"Видеоигры", "PLI3zbIkPvOTfxqYX6HkklZgFc6XH2oxrm"),
    ]:
        for item in get_playlist_video_list(playlist_id):
            item.notification_title = f'{playlist_title} [{NAME}]'
            items.append(item)

    return items


run_notification_job(
    NAME,
    DIR,
    get_video_list,
    # Чтобы не было "каши", т.к. видео собирается из нескольких плейлистов
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
