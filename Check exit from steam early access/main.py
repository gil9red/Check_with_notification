#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о выходе игр из раннего доступа steam.

"""


import sys
import time

from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_GAME
from root_common import (
    NotificationJob,
    DataItem,
    SavedModeEnum,
    read_data_items,
    run_notification_job,
)
from third_party.store_steampowered_com__check_early_access import is_early_access


PATH_ITEMS: Path = DIR / "items.json"


GAMES: list[DataItem] = read_data_items(
    file_name=PATH_ITEMS,
    save_mode=SavedModeEnum.DATA_ITEM,
)


def get_items(job: NotificationJob) -> list[DataItem]:
    current_items: list[DataItem] = job.read_items()

    new_items: list[DataItem] = []
    for game in GAMES:
        title_is_ready: str = f"{game.title!r} готова!"

        # Если игра уже была в списке как готовая, то пропуск проверки в стиме
        if any(item for item in current_items if item.value == title_is_ready):
            print(f"Пропуск {game.title!r}, так как уже готова")
            continue

        title: str = (
            f"{game.title!r} в раннем доступе"
            if is_early_access(game.url)
            else title_is_ready
        )

        new_items.append(
            DataItem(
                value=title,
                url=game.url,
            )
        )

        time.sleep(1)

    return new_items


run_notification_job(
    "Выход из раннего доступа steam",
    DIR,
    get_items,
    formats=FORMATS_GAME,
)
