#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео Sally Face.

"""


import sys
from pathlib import Path
from typing import List

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from format import FORMAT_VIDEO
from root_common import run_notification_job
from third_party.youtube_com__get_video_list import get_video_list


def get_yt_video_list() -> List[str]:
    text = 'Sally Face'
    url = 'https://www.youtube.com/user/HellYeahPlay/search?query=' + text

    return get_video_list(url, filter_func=lambda name: text in name and 'эпизод' in name.lower())


run_notification_job(
    'Sally Face',
    DIR,
    get_yt_video_list,
    format=FORMAT_VIDEO,
)
