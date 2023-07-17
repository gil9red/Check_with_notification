#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о новых главах манги в закладках пользователя.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / "third_party" / "grouple_co"))

from formats import FORMATS_CHAPTER
from root_common import run_notification_job, TimeoutWait
from third_party.grouple_co.get_updates_from_rss import get_feeds_by_manga_chapters


run_notification_job(
    "Новые главы манги",
    DIR,
    lambda job: get_feeds_by_manga_chapters(),
    timeout=TimeoutWait(hours=1),
    formats=FORMATS_CHAPTER,
    need_to_store_items=500,  # Будем помнить последние 500 глав
)
