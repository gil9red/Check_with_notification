#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Шизоидус.

"""


import sys

from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job_youtube

run_notification_job_youtube(
    "Шизоидус",
    DIR,
    "https://www.youtube.com/@shizoidus/videos",
    formats=FORMATS_VIDEO.replace(
        prefix="🍄",
    ),
)
