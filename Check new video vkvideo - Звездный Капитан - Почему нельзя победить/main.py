#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Почему нельзя победить [Звездный Капитан].

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job_vkvideo

run_notification_job_vkvideo(
    "Почему нельзя победить [Звездный Капитан]",
    DIR,
    "https://vkvideo.ru/playlist/-119338402_3",
    formats=FORMATS_VIDEO.replace(
        prefix="💀",
    ),
)
