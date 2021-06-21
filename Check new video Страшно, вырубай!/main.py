#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео "Страшно, вырубай!".

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job, get_playlist_video_list, FORMAT_VIDEO


run_notification_job(
    'Страшно, вырубай! [StopGame]',
    DIR,
    lambda: get_playlist_video_list('PLZfhqd1-Hl3CdAaP_DVgU2tpBSVLBNICD'),
    format=FORMAT_VIDEO,
)
