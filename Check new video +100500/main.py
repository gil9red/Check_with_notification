#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео "+100500".

"""


import sys
from pathlib import Path
from typing import List

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job, get_playlist_video_list, NotificationJob


def get_items(job: NotificationJob) -> List[str]:
    items = get_playlist_video_list('PLC6A0625DCA9AAE2D')

    # Проверка работы скрипта для извлечения видео из youtube
    assert len(items) > 100, f"Количество видео меньше или равно 100: {len(items)}"

    return items


run_notification_job(
    '+100500',
    DIR,
    get_items,
    formats=FORMATS_VIDEO,
)
