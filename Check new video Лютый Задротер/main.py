#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Лютый Задротер.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    DataItem,
    run_notification_job,
    search_youtube,
    NotificationJob,
    SavedModeEnum,
)


PLAYLISTS = [
    (f"TES и Fallout", "PLI3zbIkPvOTdBlH4bV7WKxvon4IFMXYsX"),
    (f"Ревью", "PLI3zbIkPvOTcmCFoBwNj2T_WOG_wZYugZ"),
    (f"Видеоигры", "PLI3zbIkPvOTfxqYX6HkklZgFc6XH2oxrm"),
]


# TODO:
def get_playlist_video_list(playlist_id: str) -> list[DataItem]:
    url = "https://www.youtube.com/playlist?list=" + playlist_id
    return [
        DataItem(value=video.id, title=video.title, url=video.url)
        for video in search_youtube(url)
    ]


def get_video_list_from_playlists(
    job: NotificationJob,
    playlists: list[tuple[str, str]],
) -> list[DataItem]:
    name = job.log.name

    items = []
    for playlist_title, playlist_id in playlists:
        video_list = get_playlist_video_list(playlist_id)
        job.log.info(f"Из плейлиста '{playlist_title}' загружено {len(video_list)} видео")

        for item in video_list:
            item.notification_title = f"{playlist_title} [{name}]"
            items.append(item)

    return items


run_notification_job(
    "Лютый Задротер",
    DIR,
    lambda job: get_video_list_from_playlists(job, PLAYLISTS),
    save_mode=SavedModeEnum.DATA_ITEM,
    # Чтобы не было "каши", т.к. видео собирается из нескольких плейлистов
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
