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


USER_ID: int = 19803


def get_all_items(job: NotificationJob) -> list[DataItem]:
    items: list[DataItem] = []

    # Для кеширования
    current_items: list[str] = [item.value for item in job.read_items()]

    job.log.debug(f"Загрузка закладок USER_ID={USER_ID}")

    bookmarks = get_bookmarks(USER_ID)
    job.log.debug(f"Закладки: {len(bookmarks)}")

    bookmarks = [obj for obj in bookmarks if obj.status != "Прочитано"]
    job.log.debug(f"Закладки (не прочитано): {len(bookmarks)}")

    for i, bookmark in enumerate(bookmarks, 1):
        item = DataItem(value=bookmark.title, url=bookmark.url)

        if bookmark.title in current_items:
            job.log.debug(f"{i}. Закладка {bookmark.title!r} уже проверена. Пропуск")
            items.append(item)
            continue

        # Небольшая задержка перед загрузкой страницы ранобе
        time.sleep(1.5)

        job.log.debug(f"{i}. Загрузка {bookmark.url}")

        status = get_ranobe_info(bookmark.url).status
        job.log.debug(f"{i}. Статус: {status}")

        if status == "Завершено":
            items.append(item)

    return items


run_notification_job(
    "Завершенные ранобе",
    DIR,
    get_all_items,
    formats=FORMATS_BOOK,
)
