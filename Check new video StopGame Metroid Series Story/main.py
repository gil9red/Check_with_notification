#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео истории серии Metroid.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job, search_youtube_with_filter


URL = 'https://www.youtube.com/playlist?list=PLZfhqd1-Hl3Di2yxyrrvH53vdREDrHU3c'


run_notification_job(
    'История серии Metroid [StopGame]',
    DIR,
    lambda job: search_youtube_with_filter(URL),
    formats=FORMATS_VIDEO,
    url=URL,
)
