#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "+100500".

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


def get_items(_: NotificationJob) -> list[DataItem]:
    items = get_playlist_video_list("PLC6A0625DCA9AAE2D")

    # Проверка работы скрипта для извлечения видео из youtube
    assert len(items) > 100, f"Количество видео меньше или равно 100: {len(items)}"

    return items


run_notification_job(
    "+100500",
    DIR,
    get_items,
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
