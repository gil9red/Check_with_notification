#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о завершенных ранобе.

"""


import sys
import time

from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / "third_party" / "ranobehub_org"))

from formats import FORMATS_BOOK
from root_common import DataItem, NotificationJob, run_notification_job
from third_party.ranobehub_org.get_bookmarks import get_bookmarks
from third_party.ranobehub_org.get_ranobe_info import get_ranobe_info


USER_ID = 19803


def get_all_items(_: NotificationJob) -> list[DataItem]:
    items = []
    for bookmark in get_bookmarks(USER_ID):
        if bookmark.status != "Прочитано":
            # Небольшая задержка перед загрузкой страницы ранобе
            time.sleep(0.5)

            status = get_ranobe_info(bookmark.url).status
            if status == "Завершено":
                items.append(
                    DataItem(value=bookmark.title, url=bookmark.url)
                )

    return items


run_notification_job(
    "Завершенные ранобе",
    DIR,
    get_all_items,
    formats=FORMATS_BOOK,
    send_new_items_separately=True,
)
