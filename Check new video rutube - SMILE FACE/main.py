#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео SMILE FACE на Rutube.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    DataItem,
    NotificationJob,
    SavedModeEnum,
    get_rutube_video_list,
    run_notification_job,
)


def get_items(_: NotificationJob) -> list[DataItem]:
    items: list[DataItem] = []
    for url in [
        "https://rutube.ru/channel/23547494/videos/",
        "https://rutube.ru/channel/30714439/videos/",
    ]:
        items += get_rutube_video_list(url, maximum_items=50)
    return items


run_notification_job(
    "SMILE FACE [rutube]",
    DIR,
    get_items,
    save_mode=SavedModeEnum.DATA_ITEM,
    formats=FORMATS_VIDEO.replace(
        prefix="🎭",
    ),
)
