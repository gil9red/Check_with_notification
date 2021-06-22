#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых главах Berserk.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from format import FORMAT_CHAPTER
from root_common import run_notification_job
from third_party.risens_team__berserk import get_chapters


run_notification_job(
    'Манга Berserk',
    DIR,
    get_chapters,
    format=FORMAT_CHAPTER,
)
