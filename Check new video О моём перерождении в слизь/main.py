#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых серий аниме "О моём перерождении в слизь".

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job, DataItem, NotificationJob

from third_party.jut_su.anime_get_video_list import get_video_list


URL = "https://jut.su/slime-datta-ken/"


def get_items(_: NotificationJob) -> list[DataItem]:
    items = []
    for season, video_list in get_video_list(URL).items():
        for video in video_list:
            title = video.title
            if season:
                title = f"{season}. {title}"

            items.append(
                DataItem(value=title, url=video.url)
            )

    return items


run_notification_job(
    "О моём перерождении в слизь",
    DIR,
    get_items,
    formats=FORMATS_VIDEO,
)
