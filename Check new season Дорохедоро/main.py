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

from root_common import run_notification_job
from third_party.get_seasons_anime_Dorohedoro import get_seasons


run_notification_job(
    'Дорохедоро',
    DIR,
    get_seasons,
    notified_by_sms=True,
    format_current_items='Текущий список сезонов (%s): %s',
    format_get_items='Запрос сезонов',
    format_items='Список сезонов (%s): %s',
    format_new_item='Новый сезон "%s"',
    format_no_new_items='Изменений нет',
)
