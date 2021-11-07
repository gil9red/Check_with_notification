#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о изменении количества Стивов из описания.

"""


import sys
from typing import List

from common import DIR, set_lock
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import Formats
from root_common import run_notification_job, get_logger
from third_party.ncse_ngo__list_steves import get_number_from_description


# Адаптация текста под одно значение, вместо списка
FORMATS_STEVES = Formats(
    current_items='Текущее количество Стивов (%s): %s',
    get_items='Запрос количества Стивов',
    items='Список количества Стивов (%s): %s',
    new_item='Изменение количества Стивов: %s',
    no_new_items='Изменений нет',
)


def get_items() -> List[str]:
    try:
        set_lock(True)
        return [str(get_number_from_description())]  # Список из одного элемента
    finally:
        set_lock(False)


run_notification_job(
    get_logger('Check new Steves (from description)', DIR / 'log from description.txt'),
    DIR,
    get_items,
    file_name_saved='saved from description.json',
    formats=FORMATS_STEVES,
)
