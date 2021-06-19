#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых серий аниме My Hero Academia.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job
from third_party.online_anidub_com.get_video_list import search_video_list


run_notification_job(
    'My Hero Academia',
    DIR,
    lambda: search_video_list('Моя геройская академия'),
    notified_by_sms=True,
    notify_when_empty=False,  # Парсер не всегда правильно работает из-за прокси, поэтому не уведомляем о проблемах
    timeout={'days': 3},
    format_current_items='Текущий список видео (%s): %s',
    format_get_items='Запрос видео',
    format_items='Список видео (%s): %s',
    format_new_item='Новая серия "%s"',
    format_no_new_items='Изменений нет',
)
