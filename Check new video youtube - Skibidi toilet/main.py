#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Skibidi toilet.

"""


import sys
import re

from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    DataItem,
    NotificationJob,
    get_yt_video_list,
    run_notification_job_youtube,
)

# NOTE: Варианты "Skibidi Toilet", "скибиди туалет", "туалет skibidi"
PATTERN: re.Pattern = re.compile(
    pattern="(?=.*(skibidi|скибиди))(?=.*(toilet|туалет))",
    flags=re.IGNORECASE,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    # Не всегда вовремя в плейлист кладет, поэтому для актуальности брать со страницы
    url: str = "https://www.youtube.com/channel/UCsSsgPaZ2GSmO6il8Cb5iGA/videos"
    return [item for item in get_yt_video_list(url) if PATTERN.search(item.title)]


run_notification_job_youtube(
    "Skibidi toilet",
    DIR,
    get_items,
    formats=FORMATS_VIDEO.replace(
        prefix="🚽",
    ),
)
