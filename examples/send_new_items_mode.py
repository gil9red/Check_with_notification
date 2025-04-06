#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для примера отправки группы уведомлений.

"""


import sys
import uuid

from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import SendNewItemsModeEnum, NotificationJob, run_notification_job


def get_items(_: NotificationJob) -> list[str]:
    return [f"#{i + 1}. {uuid.uuid4()}" for i in range(5)]


run_notification_job(
    "Тест [single message]",
    DIR,
    get_items,
    is_single=True,
    send_new_items_mode=SendNewItemsModeEnum.SINGLE_MESSAGE,
)

run_notification_job(
    "Тест [separately]",
    DIR,
    get_items,
    is_single=True,
    send_new_items_mode=SendNewItemsModeEnum.SEPARATELY,
)

run_notification_job(
    "Тест [group]",
    DIR,
    get_items,
    is_single=True,
    send_new_items_mode=SendNewItemsModeEnum.GROUP,
)
