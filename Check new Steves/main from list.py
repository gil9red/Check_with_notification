#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о изменении списка Стивов.

"""


import sys
import time

from typing import List

from common import DIR, has_lock
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import Formats
from root_common import run_notification_job, get_logger, NotificationJob
from third_party.ncse_ngo__list_steves import get_Steves


FORMATS_STEVES = Formats(
    current_items='Текущий список Стивов (%s): %s',
    get_items='Запрос списка Стивов',
    items='Список Стивов (%s): %s',
    new_item='Изменение списка Стивов: %s',
    new_items='Появились новые Стивы (%s):\n%s',
    no_new_items='Изменений нет',
)


def get_items(job: NotificationJob) -> List[str]:
    # Даем фору скрипту "main from description.py", ждем пока он выполнится
    # Тогда, при изменении количества Стивов будет логичнее получить уведомление раньше, чем
    # новые Стивы из списка
    time.sleep(5)
    while has_lock():
        time.sleep(1)

    return [x.get_text() for x in get_Steves()]


run_notification_job(
    get_logger('Проверка новых Стивов (из списка)', DIR / 'log from list.txt'),
    DIR,
    get_items,
    file_name_saved='saved from list.json',
    file_name_saved_backup='saved from list backup.json',
    log_new_items_separately=True,
    formats=FORMATS_STEVES,
)
