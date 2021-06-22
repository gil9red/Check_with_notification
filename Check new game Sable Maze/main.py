#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых игр серии Sable Maze.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / 'third_party' / 'bigfishgames_com__hidden_object'))

from format import FORMAT_GAME
from root_common import run_notification_job
from third_party.bigfishgames_com__hidden_object.find__Sable_Maze__CE import get_games


run_notification_job(
    'Sable Maze',
    DIR,
    get_games,
    format=FORMAT_GAME,
)
