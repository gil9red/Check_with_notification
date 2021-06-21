#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых сезонов аниме "Дорохедоро".

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job, FORMAT_SEASON
from third_party.get_seasons_anime_Dorohedoro import get_seasons


run_notification_job(
    'Дорохедоро',
    DIR,
    get_seasons,
    format=FORMAT_SEASON,
)
