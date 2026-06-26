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

from root_common import run_notification_job_youtube

run_notification_job_youtube(
    "Сашка Кроп MHz'ы",
    DIR,
    "PL24NJvgUw-cyZ6Mz25pAhMSa1l8uYLzo9",
)
