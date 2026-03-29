#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о новых главах https://mangalib.me.

"""


import sys
import time
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / "third_party" / "grouple_co"))

from formats import FORMATS_CHAPTER
from root_common import (
    NotificationJob,
    DataItem,
    SavedModeEnum,
    run_notification_job,
    read_data_items,
)
from third_party.mangalib_me.get_chapters import Chapter, get_chapters

PATH_ITEMS: Path = DIR / "items.json"


ITEMS: list[DataItem] = read_data_items(
    file_name=PATH_ITEMS,
    save_mode=SavedModeEnum.DATA_ITEM,
)


def get_items(job: NotificationJob) -> list[DataItem]:
    items: list[DataItem] = []

    for item in ITEMS:
        manga_title: str = item.value
        manga_url: str = item.url

        job.log.info(f"Загрузка глав {manga_title!r} из {manga_url}")

        chapters: list[Chapter] = get_chapters(manga_url)

        # Последние 10 добавленных глав
        latest_chapters: list[Chapter] = sorted(
            chapters,
            key=lambda c: c.branches[0].created_at,
            reverse=True,
        )[:10]

        items.extend(
            DataItem(
                value=f"{manga_title}\n{chapter.title}",
                url=chapter.url,
            )
            for chapter in latest_chapters
        )

        time.sleep(1)

    return items


run_notification_job(
    "Новые главы манги [mangalib.me]",
    DIR,
    get_items,
    formats=FORMATS_CHAPTER,
)
