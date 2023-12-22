#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления об устаревших скриптах.

"""


import sys
from datetime import datetime
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_DEFAULT
from root_common import DataItem, NotificationJob, run_notification_job


IGNORED = [".deprecated", "examples", str(DIR.name)]
DAYS_DIVIDER = 180


def get_scripts() -> list[tuple[str, int]]:
    items = []

    for file in DIR.parent.glob("Check*/saved.json"):
        if any(f in str(file) for f in IGNORED):
            continue

        script_name = file.parent.name
        modified_datetime = datetime.fromtimestamp(file.stat().st_mtime)
        delta = datetime.now() - modified_datetime
        delta_in_days = int(delta.total_seconds()) // (3600 * 24)
        items.append((script_name, delta_in_days))

    return items


def get_items(_: NotificationJob) -> list[DataItem]:
    new_items = []

    for script_name, delta_in_days in get_scripts():
        n = delta_in_days // DAYS_DIVIDER
        if n == 0:
            continue

        days = n * DAYS_DIVIDER

        new_items.append(
            DataItem(
                value=f"{script_name}/{days}",
                title=f'От скрипта "{script_name}" нет уведомлений уже {days} дней',
            )
        )

    return new_items


run_notification_job(
    "Устаревшие скрипты",
    DIR,
    get_items,
    formats=FORMATS_DEFAULT.replace(
        new_item="%s",
        prefix="🚮",
    ),
    notify_when_empty=False,
    send_new_items_separately=True,
)
