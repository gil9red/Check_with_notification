#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Crispy Crumb.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job_youtube

run_notification_job_youtube(
    "Crispy Crumb",
    DIR,
    "https://www.youtube.com/@Crispy_Crumb/videos",
    formats=FORMATS_VIDEO.replace(
        prefix="🍪",
    ),
)
