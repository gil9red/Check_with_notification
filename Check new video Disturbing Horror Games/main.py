#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео Disturbing Horror Games.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job, get_playlist_video_list


run_notification_job(
    'Disturbing Horror Games',
    DIR,
    lambda job: get_playlist_video_list('PLVOZT4ssBLx7d4TSZuYU_lkRwAUaON3FI'),
    formats=FORMATS_VIDEO,
)
