#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых главах Berserk.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_CHAPTER
from root_common import DataItem, run_notification_job, NotificationJob
from third_party.readberserk_com__get_chapters import get_chapters


def get_items(_: NotificationJob) -> list[DataItem]:
    return [
        DataItem(
            value=chapter.title,
            url=chapter.url,
        )
        for chapter in get_chapters()
    ]


run_notification_job(
    "Манга Berserk",
    DIR,
    get_items,
    formats=FORMATS_CHAPTER.replace(
        new_item="Новая глава %s",
    ),
)
