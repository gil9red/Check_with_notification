#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых игр серии Spirits of Mystery.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / 'third_party' / 'bigfishgames_com__hidden_object'))

from root_common import run_notification_job
from third_party.bigfishgames_com__hidden_object.find__Spirits_of_Mystery__CE import get_games


run_notification_job(
    'Spirits of Mystery',
    DIR,
    get_games,
    notified_by_sms=True,
    format_current_items='Текущий список игр (%s): %s',
    format_get_items='Запрос списка игр',
    format_items='Список игр (%s): %s',
    format_new_item='Появилась новая игра "%s"',
    format_no_new_items='Новых игр нет',
)
