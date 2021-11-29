#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео Gorgeous Freeman.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job, NotificationJob
from third_party.youtube_com__results_search_query import search_youtube_with_filter


def get_yt_video_list(job: NotificationJob):
    text = 'Gorgeous Freeman -'
    url = 'https://www.youtube.com/user/antoine35DeLak/search?query=' + text

    return search_youtube_with_filter(url, filter_func=lambda name: text in name)


run_notification_job(
    'Gorgeous Freeman',
    DIR,
    get_yt_video_list,
    formats=FORMATS_VIDEO,
)
