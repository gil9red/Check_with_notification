#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео из плейлиста "Все фильмы" из Фильмач в Rutube.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    NotificationJob,
    SavedModeEnum,
    run_notification_job,
    get_items_from_rutube,
)


URL = "https://rutube.ru/plst/328068/"


def on_first_start_detected(job: NotificationJob):
    job.log.debug("На первый запуск выполняется сохранение всех видео")

    items = get_items_from_rutube(job, URL)
    job.save_items(items)


run_notification_job(
    "Все фильмы Фильмач [Rutube]",
    DIR,
    lambda job: get_items_from_rutube(job, URL, max_items=100),
    send_new_items_as_group=True,
    formats=FORMATS_VIDEO,
    save_mode=SavedModeEnum.DATA_ITEM,
    callbacks=NotificationJob.Callbacks(
        on_first_start_detected=on_first_start_detected,
    ),
    need_to_store_items=9999,
)
