#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о новых сленговых словах.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / "third_party"))

from formats import FORMATS_DEFAULT
from root_common import run_notification_job, DataItem, NotificationJob, TimeoutWait, SavedModeEnum
from third_party.memepedia_ru import get_memes_words


def get_all_items(_: NotificationJob) -> list[DataItem]:
    items = []
    for meme in get_memes_words():
        items.append(
            DataItem(
                value=meme.title,
                title=f"<b>{meme.title}</b>\n\n{meme.url_img}",
                url=meme.url,
                need_html_escape_content=False,
            )
        )

    return items


run_notification_job(
    "Новый сленг",
    DIR,
    get_all_items,
    timeout=TimeoutWait(hours=4),
    formats=FORMATS_DEFAULT.replace(
        new_item="%s",
        prefix="🗿",
    ),
    save_mode=SavedModeEnum.DATA_ITEM,
)
