#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Южный парк в Rutube.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    SavedModeEnum,
    NotificationJob,
    run_notification_job,
    get_items_from_rutube,
)


URL = "https://rutube.ru/channel/36379221/videos/"


def on_first_start_detected(job: NotificationJob):
    job.log.debug("На первый запуск выполняется сохранение всех видео")

    items = get_items_from_rutube(job, URL)
    job.save_items(items)


run_notification_job(
    "Южный парк [Rutube]",
    DIR,
    lambda job: get_items_from_rutube(job, URL, max_items=100),
    formats=FORMATS_VIDEO,
    save_mode=SavedModeEnum.DATA_ITEM,
    callbacks=NotificationJob.Callbacks(
        on_first_start_detected=on_first_start_detected,
    ),
    need_to_store_items=9999,
)
