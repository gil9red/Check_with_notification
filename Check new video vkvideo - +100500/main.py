#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "+100500".

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job_vkvideo

run_notification_job_vkvideo(
    "+100500",
    DIR,
    "https://vkvideo.ru/playlist/-1719791_48513772",
)
