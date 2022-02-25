#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео Лютый Задротер.

"""


import sys
from pathlib import Path
from typing import List

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job, get_playlist_video_list, NotificationJob


def get_video_list(job: NotificationJob) -> List[str]:
    items = []
    for playlist_title, playlist_id in [
        ('TES и Fallout', 'PLI3zbIkPvOTdBlH4bV7WKxvon4IFMXYsX'),
        ('Ревью', 'PLI3zbIkPvOTcmCFoBwNj2T_WOG_wZYugZ'),
        ('Видеоигры', 'PLI3zbIkPvOTfxqYX6HkklZgFc6XH2oxrm'),
    ]:
        items += [
            f'{video} [{playlist_title}]'
            for video in get_playlist_video_list(playlist_id)
        ]

    return items


run_notification_job(
    'Лютый Задротер',
    DIR,
    get_video_list,
    # Чтобы не было "каши", т.к. видео собирается из нескольких плейлистов
    log_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
