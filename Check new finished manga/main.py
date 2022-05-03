#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о завершенных мангах.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / 'third_party' / 'grouple_co'))

from formats import FORMATS_MANGA
from root_common import DataItem, NotificationJob, run_notification_job
from third_party.grouple_co.common import get_all_bookmarks


def get_all_items() -> list[DataItem]:
    items = []
    for bookmarks in get_all_bookmarks().values():
        for x in bookmarks:
            title = x.get_title_with_tags()
            items.append(
                DataItem(value=title, url=x.url)
            )

    return items


def on_first_start_detected(job: NotificationJob):
    job.log.debug('На первый запуск выполняется сохранение всех манг')

    items = get_all_items()
    job.save_items(items)


def get_only_finished_items(job: NotificationJob) -> list[DataItem]:
    return [item for item in get_all_items() if 'переведено' in item.title or 'завершён' in item.title]


# На первый раз выполняется загрузка всех манг (через событие on_first_start_detected)
# На последующие разы загружаются только переведенные (законченные и переведенные) манги
run_notification_job(
    'Завершенная манга',
    DIR,
    get_only_finished_items,
    formats=FORMATS_MANGA,
    log_new_items_separately=True,
    callbacks=NotificationJob.Callbacks(
        on_first_start_detected=on_first_start_detected,
    ),
    need_to_store_items=500,  # Будем помнить последние 500 манг
)
