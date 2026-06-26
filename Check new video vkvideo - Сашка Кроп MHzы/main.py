#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Сашка Кроп MHz'ы.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job_vkvideo

run_notification_job_vkvideo(
    "Сашка Кроп MHz'ы",
    DIR,
    "https://vkvideo.ru/playlist/-60916056_2",
)
