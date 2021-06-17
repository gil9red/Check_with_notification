#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео Разбора полётов.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job
from third_party.youtube_com__get_video_list import get_video_list


def get_yt_video_list():
    url = 'https://www.youtube.com/playlist?list=PLZfhqd1-Hl3BKhWwCgmqtENSlearqLlAV'
    return get_video_list(url)


run_notification_job(
    'Разбор полётов [StopGame]',
    'video',
    get_yt_video_list,
    notified_by_sms=True,
    timeout={'days': 1},
    format_current_items='Текущий список видео (%s): %s',
    format_get_items='Запрос видео',
    format_items='Список видео (%s): %s',
    format_new_item='Новое видео "%s"',
    format_no_new_items='Изменений нет',
)
