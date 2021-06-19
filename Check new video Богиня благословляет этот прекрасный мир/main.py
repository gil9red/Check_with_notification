#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых серий аниме Богиня благословляет этот прекрасный мир.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from root_common import run_notification_job
from third_party.online_anidub_com.get_video_list import search_video_list


run_notification_job(
    'Богиня благословляет этот прекрасный мир',
    DIR,
    lambda: search_video_list('Богиня благословляет этот прекрасный мир'),
    notified_by_sms=True,
    notify_when_empty=False,  # На сайте пока отсутствуют серии, поэтому не считаем их отсутствие проблемой
    timeout={'weeks': 2},
    format_current_items='Текущий список видео (%s): %s',
    format_get_items='Запрос видео',
    format_items='Список видео (%s): %s',
    format_new_item='Новая серия "%s"',
    format_no_new_items='Изменений нет',
)
