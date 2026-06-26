#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Poppy Playtime.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job_youtube

run_notification_job_youtube(
    "Poppy Playtime",
    DIR,
    "PLejGw9J2xE9XXoMpS8xOPmkuzriJxyINS",
)
