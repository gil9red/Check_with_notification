#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео BadComedian.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    DataItem,
    run_notification_job,
    SavedModeEnum,
    get_yt_playlist_video_list,
    NotificationJob,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    items = get_yt_playlist_video_list("PL471DC4C544B5A1B9")

    # Проверка работы скрипта для извлечения видео из youtube
    assert len(items) > 100, f"Количество видео меньше или равно 100: {len(items)}"

    return items


run_notification_job(
    "BadComedian",
    DIR,
    get_items,
    save_mode=SavedModeEnum.DATA_ITEM,
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
