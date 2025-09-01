#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о изменении подписчиков пользователя в github.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent
sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import FORMATS_DEFAULT
from root_common import DataItem, run_notification_job, NotificationJob

sys.path.append(str(ROOT_DIR / "third_party" / "github_api__examples"))
from third_party.github_api__examples.get_followers import get_followers


OWNER = "gil9red"


def get_items(job: NotificationJob) -> list[DataItem]:
    current_items = job.read_items()

    new_items = []

    users = get_followers(OWNER)
    total_stars = len(users)

    for user in users:
        user_login = f'<a href="{user.url}">{user.login}</a>'
        new_items.append(
            DataItem(
                value=user_login,
                title=f"{user_login} подписался (всего подписчиков {total_stars})",
                need_html_escape_content=False,
            )
        )

    for item in current_items:
        if not item.value.startswith("-") and item not in new_items:
            new_items.append(
                DataItem(
                    value=f"-{item.value}",
                    title=f"{item.value} отписался (всего подписчиков {total_stars})",
                    need_html_escape_content=False,
                    prefix="💔",
                )
            )

    return new_items


run_notification_job(
    "Подписчики в гитхабе",
    DIR,
    get_items,
    formats=FORMATS_DEFAULT.replace(
        new_item="%s",
        prefix="❤️",
    ),
    need_to_store_items=None,
)
