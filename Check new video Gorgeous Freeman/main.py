#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео Gorgeous Freeman.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job

from third_party.youtube_com__get_video_list import get_video_list


def get_yt_video_list():
    text = 'Gorgeous Freeman -'
    url = 'https://www.youtube.com/user/antoine35DeLak/search?query=' + text

    return get_video_list(url, filter_func=lambda name: text in name)


run_notification_job(
    'Gorgeous Freeman',
    DIR,
    get_yt_video_list,
    notified_by_sms=True,
    format_current_items='Текущий список видео (%s): %s',
    format_get_items='Запрос видео',
    format_items='Список видео (%s): %s',
    format_new_item='Новое видео "%s"',
    format_no_new_items='Изменений нет',
)
