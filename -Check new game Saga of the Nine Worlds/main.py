#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых игр серии Saga of the Nine Worlds.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / 'third_party' / 'bigfishgames_com__hidden_object'))

from formats import FORMATS_GAME
from root_common import run_notification_job
from third_party.bigfishgames_com__hidden_object.find__Saga_of_the_Nine_Worlds__CE import get_games


run_notification_job(
    'Saga of the Nine Worlds',
    DIR,
    lambda job: get_games(),
    formats=FORMATS_GAME,
)
