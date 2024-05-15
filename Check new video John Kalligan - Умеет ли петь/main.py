#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео плейлиста John Kalligan - Умеет ли петь.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    SavedModeEnum,
    get_yt_playlist_video_list,
    run_notification_job,
)


run_notification_job(
    "Умеет ли петь [John Kalligan]",
    DIR,
    lambda _: get_yt_playlist_video_list("PLhNsPPGFrZoquxBDlDTl50XrajwG8Bo5j"),
    save_mode=SavedModeEnum.DATA_ITEM,
    send_new_items_separately=True,
    formats=FORMATS_VIDEO.replace(
        prefix="🎵",
    ),
)
