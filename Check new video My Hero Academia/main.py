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

from format import FORMAT_VIDEO
from root_common import run_notification_job, TimeoutWait
from third_party.online_anidub_com.get_video_list import search_video_list


run_notification_job(
    'My Hero Academia',
    DIR,
    lambda: search_video_list('Моя геройская академия'),
    notify_when_empty=False,  # Парсер не всегда правильно работает из-за прокси, поэтому не уведомляем о проблемах
    notify_after_sequence_of_errors=False,
    timeout=TimeoutWait(days=3),
    format=FORMAT_VIDEO,
)
