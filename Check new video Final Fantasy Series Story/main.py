#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео истории серии Final Fantasy.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job, get_playlist_video_list


run_notification_job(
    'История серии Final Fantasy [StopGame]',
    DIR,
    lambda: get_playlist_video_list('PLZfhqd1-Hl3DnNDG-x6SgDqlBJee-50E1'),
    formats=FORMATS_VIDEO,
)
