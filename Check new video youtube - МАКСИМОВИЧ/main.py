#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео МАКСИМОВИЧ.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job_youtube

run_notification_job_youtube(
    "МАКСИМОВИЧ",
    DIR,
    "https://www.youtube.com/@Maksimovich94/videos",
)
