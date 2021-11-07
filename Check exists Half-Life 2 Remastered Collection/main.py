#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении Half-Life 2: Remastered Collection в Steam.

"""


import sys
from pathlib import Path
from typing import List

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import Formats
from root_common import run_notification_job
from third_party.store_steampowered_com__check_exists_app import is_exists


def get_is_exists_title() -> List[str]:
    # Half-Life 2: Remastered Collection
    return [
        "Игра появилась в магазине Steam" if is_exists(600680) else "Игра убрана из магазина Steam"
    ]


run_notification_job(
    'Проверка Half-Life 2: Remastered Collection',
    DIR,
    get_is_exists_title,
    formats=Formats(
        get_items='Проверка игры',
        new_item='%s',  # Название статуса будет использовано для описания уведомления
        no_new_items='Изменений нет',
    ),
)
