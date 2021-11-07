#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых главах Легендарного лунного скульптора.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_CHAPTER
from root_common import run_notification_job
from third_party.ranobehub_org_api_ranobe_92_contents__The_Legendary_Moonlight_Sculptor import get_chapters


run_notification_job(
    'Легендарный лунный скульптор',
    DIR,
    get_chapters,
    formats=FORMATS_CHAPTER,
)
