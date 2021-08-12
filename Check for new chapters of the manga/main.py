#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from pathlib import Path
from typing import List

import feedparser
import requests

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from format import FORMAT_CHAPTER
from root_common import run_notification_job


def get_feeds_by_manga_chapters(url_rss: str) -> List[str]:
    rss_text = requests.get(url_rss).text
    feed = feedparser.parse(rss_text)

    feeds = []

    for entry in feed.entries:
        title = entry.title

        if title.startswith('Манга '):
            title = title[len('Манга '):]

        elif title.startswith('Взрослая манга '):
            title = title[len('Взрослая манга '):]

        feeds.append(title)

    return feeds


URL_USER_RSS = 'https://grouple.co/user/rss/315828?filter='


run_notification_job(
    'Новые главы манги',
    DIR,
    lambda: get_feeds_by_manga_chapters(URL_USER_RSS),
    format=FORMAT_CHAPTER,
    need_to_store_items=500,  # Будем помнить последние 500 глав
)
