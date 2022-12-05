#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении I Am Jesus Christ в Steam.

"""


import sys
from pathlib import Path
from typing import List

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import Formats
from root_common import run_notification_job, NotificationJob
from third_party.price_of_games.app_parser.utils import get_price


def get_is_exists_title(job: NotificationJob) -> List[str]:
    price = get_price('I Am Jesus Christ', job.log)
    return [
        "Игра доступна для покупки" if price else "Игра не доступна для покупки"
    ]


run_notification_job(
    'Проверка I Am Jesus Christ',
    DIR,
    get_is_exists_title,
    formats=Formats(
        get_items='Проверка игры',
        new_item='%s',  # Название статуса будет использовано для описания уведомления
        no_new_items='Изменений нет',
        postfix='🎮',
    ),
)
