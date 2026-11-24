#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "Страшно, вырубай!" от Василия Гальперова.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import get_yt_playlist_video_list, run_notification_job_youtube

run_notification_job_youtube(
    "Страшно, вырубай! [Василий Гальперов]",
    DIR,
    lambda job: get_yt_playlist_video_list("PLL-xlboKIBBU"),
)
