#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о завершенных мангах.

"""


import sys
from pathlib import Path
from typing import List

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / 'third_party' / 'grouple_co'))

from formats import FORMATS_MANGA
from root_common import NotificationJob, run_notification_job
from third_party.grouple_co.print_pretty_title_all_bookmarks import get_all_pretty_title_of_bookmarks as get_all_items


def on_first_start_detected(job: NotificationJob):
    job.log.debug('На первый запуск выполняется сохранение всех манг')

    items = get_all_items()
    job.save_items(items)


def get_only_finished_items(job: NotificationJob) -> List[str]:
    return [title for title in get_all_items() if 'переведено' in title]


# На первый раз выполняется загрузка всех манг (через событие on_first_start_detected)
# На последующие разы загружаются только переведенные (законченные и переведенные) манги
run_notification_job(
    'Завершенная манга',
    DIR,
    get_only_finished_items,
    formats=FORMATS_MANGA,
    callbacks=NotificationJob.Callbacks(
        on_first_start_detected=on_first_start_detected,
    ),
)
