#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "Пацаны".

"""


import sys

from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import DataItem, run_notification_job

from third_party.theboys_fun import get_all_series


def get_all_items() -> list[DataItem]:
    return [
        DataItem(
            value=video.title,
            url=video.url,
        )
        for video in get_all_series()
    ]


run_notification_job(
    "Пацаны",
    DIR,
    lambda job: get_all_items(),
    formats=FORMATS_VIDEO,
)
