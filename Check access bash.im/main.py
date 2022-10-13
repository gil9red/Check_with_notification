#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о изменении доступности https://bash.im.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import Formats
from root_common import run_notification_job, DataItem, NotificationJob, session


URL = 'https://bash.im'


def get_items(_: NotificationJob) -> list[DataItem]:
    try:
        rs = session.get(URL)
        rs.raise_for_status()
        result = 'Ожил!'
    except Exception:
        result = 'Умер!'

    return [
        DataItem(value=result)
    ]


run_notification_job(
    'Доступность bash.im',
    DIR,
    get_items,
    formats=Formats(
        current_items='Текущий список значений (%s): %s',
        get_items='Запрос сайта',
        items='Список значений (%s): %s',
        new_item='%s',
        no_new_items='Изменений нет',
    ),
    url=URL,
)
