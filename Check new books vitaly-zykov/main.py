#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых книг Зыкова.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job
from third_party.vitaly_zykov_ru_knigi__get_books import get_books


run_notification_job(
    'Новые книги Виталия Зыкова',
    DIR / 'books',
    get_books,
    notified_by_sms=True,
    format_current_items='Текущий список книг (%s): %s',
    format_get_items='Запрос списка книг',
    format_items='Список книг (%s): %s',
    format_new_item='Появилась новая книга Зыкова: "%s"',
    format_no_new_items='Новых книг нет',
)
