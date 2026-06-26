#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео TVG (Time Video Game).

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job_vkvideo

run_notification_job_vkvideo(
    "TVG",
    DIR,
    "https://vkvideo.ru/@timevideogame/all",
)
