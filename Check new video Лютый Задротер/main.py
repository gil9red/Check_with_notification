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
    run_notification_job,
    SavedModeEnum,
    get_video_list_from_playlists,
)


PLAYLISTS = [
    (f"TES и Fallout", "PLI3zbIkPvOTdBlH4bV7WKxvon4IFMXYsX"),
    (f"Ревью", "PLI3zbIkPvOTcmCFoBwNj2T_WOG_wZYugZ"),
    (f"Видеоигры", "PLI3zbIkPvOTfxqYX6HkklZgFc6XH2oxrm"),
]


run_notification_job(
    "Лютый Задротер",
    DIR,
    lambda job: get_video_list_from_playlists(job, PLAYLISTS),
    save_mode=SavedModeEnum.DATA_ITEM,
    # Чтобы не было "каши", т.к. видео собирается из нескольких плейлистов
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
