#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Александр N и YouHollywood.

"""


import sys
import re

from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    run_notification_job,
    SavedModeEnum,
    get_yt_video_list,
    DataItem,
    NotificationJob,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    # Не все видео интересны, убраны те, что связаны с курсами YouHollywood
    url = "https://www.youtube.com/@YouHollywood/videos"
    return [
        item
        for item in get_yt_video_list(url)
        if (
            # Слова в черном списке
            not re.search(
                "Проект Про|курс|школ",
                item.title,
                flags=re.IGNORECASE,
            )
            and "Александр N".lower() in item.title.lower()
        )
    ]


run_notification_job(
    "Александр N и YouHollywood",
    DIR,
    get_items,
    save_mode=SavedModeEnum.DATA_ITEM,
    formats=FORMATS_VIDEO,
)
