#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о новых релизных версиях python.

"""


import sys

from datetime import date
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import FORMATS_DEFAULT
from root_common import TimeoutWait, NotificationJob, DataItem, run_notification_job
from third_party.python_org.get_release_versions import get_release_versions


def get_items(_: NotificationJob) -> list[DataItem]:
    return [
        DataItem(value=v.version, url=v.url_whatsnew)
        for v in get_release_versions()
        if v.release_start < date.today()
    ]


run_notification_job(
    "Новый релиз python",
    DIR,
    get_items,
    timeout=TimeoutWait(weeks=1),
    formats=FORMATS_DEFAULT.replace(
        new_item="%s",
        prefix="🐍",
    ),
)
