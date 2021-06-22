#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео "Бесполезное мнение".

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from format import FORMAT_VIDEO
from root_common import run_notification_job, get_playlist_video_list


run_notification_job(
    'Бесполезное мнение [Velind]',
    DIR,
    lambda: get_playlist_video_list('PLgqDz7CZ-6NbDjtcYuPFW2wb2LS7BQJMb'),
    format=FORMAT_VIDEO,
)
