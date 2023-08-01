#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о изменении лайков в репозитории.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_DEFAULT
from root_common import DataItem, run_notification_job, NotificationJob
from third_party.get_stargazers import get_stargazers


OWNER = "gil9red"
REPOSITORY = "SimplePyScripts"


def get_items(job: NotificationJob) -> list[DataItem]:
    current_items = job.read_items()

    new_items = []
    for user in get_stargazers(OWNER, REPOSITORY):
        user_login = f'<a href="{user.url}">{user.login}</a>'
        new_items.append(
            DataItem(
                value=user_login,
                title=f'{user_login} поставил лайк в {REPOSITORY}',
            )
        )

    for item in current_items:
        if not item.value.startswith("-") and item not in new_items:
            new_items.append(
                DataItem(
                    value=f"-{item.value}",
                    title=f'{item.value} убрал свой лайк в {REPOSITORY}',
                )
            )

    return new_items


run_notification_job(
    "Лайки в гитхабе",
    DIR,
    get_items,
    formats=FORMATS_DEFAULT,
)
