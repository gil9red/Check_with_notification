#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о изменении цены за интернет.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / 'third_party' / 'ttk_ru'))  # Путь к папке выше

from formats import Formats
from root_common import run_notification_job
from third_party.ttk_ru.main import get_price


run_notification_job(
    'Изменение цены за интернет',
    DIR,
    lambda job: [get_price()],
    formats=Formats(
        get_items='Проверка цены',
        new_item='Новая цена: %s',
        no_new_items='Изменений нет',
    ),
)