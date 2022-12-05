#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых взломанных играх.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_GAME
from root_common import run_notification_job
from third_party.gamestatus_info__lastcrackedgames import get_games


run_notification_job(
    'Новые взломанные игры',
    DIR,
    lambda job: get_games(),
    formats=FORMATS_GAME,
)
