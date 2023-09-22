#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о новых релизных версиях python.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import FORMATS_DEFAULT
from root_common import run_notification_job, NotificationJob, DataItem
from third_party.python_org.get_release_versions import get_release_versions


def get_items(_: NotificationJob) -> list[DataItem]:
    return [
        DataItem(
            value=version,
            url=f"https://docs.python.org/{version[0]}/whatsnew/{version}.html",
        )
        for version in get_release_versions()
    ]


run_notification_job(
    "Новый релиз python",
    DIR,
    get_items,
    send_new_items_separately=True,
    formats=FORMATS_DEFAULT.replace(
        new_item="Новая версия %s",
        prefix="🐍",
    ),
    need_notification=False,
)
