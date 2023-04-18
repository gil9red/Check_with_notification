#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

import feedparser

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_CHAPTER
from root_common import run_notification_job, TimeoutWait


URL_USER_RSS = "https://grouple.co/user/rss/315828?filter="


def get_feeds_by_manga_chapters() -> list[str]:
    feed = feedparser.parse(
        URL_USER_RSS,
        agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    )

    feeds = []
    for entry in feed.entries:
        title: str = entry.title
        title = (
            title.replace("&quot;", '"')
            .replace("Манга", "")
            .replace("Взрослая манга", "")
            .strip()
        )

        feeds.append(title)

    return feeds


run_notification_job(
    "Новые главы манги",
    DIR,
    lambda job: get_feeds_by_manga_chapters(),
    timeout=TimeoutWait(hours=1),
    formats=FORMATS_CHAPTER,
    need_to_store_items=500,  # Будем помнить последние 500 глав
)
