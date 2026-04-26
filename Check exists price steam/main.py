#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении цены игр в Steam.

"""


import sys
import time

from pathlib import Path

from bs4 import BeautifulSoup, Tag

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import Formats
from root_common import (
    DataItem,
    SavedModeEnum,
    read_data_items,
    run_notification_job,
    NotificationJob,
    session,
)

PATH_ITEMS: Path = DIR / "items.json"


GAMES: list[DataItem] = read_data_items(
    file_name=PATH_ITEMS,
    save_mode=SavedModeEnum.DATA_ITEM,
)


def get_price(url: str) -> int | None:
    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    meta_price: Tag | None = soup.select_one("meta[itemprop=price]")
    if meta_price is None:
        return

    value: str | None = meta_price.get("content")
    if value is None:
        return

    return int(value)


def get_items(job: NotificationJob) -> list[DataItem]:
    current_items: list[DataItem] = job.read_items()

    new_items: list[DataItem] = []
    for game in GAMES:
        title_is_ready: str = f"Игра {game.title!r} доступна для покупки"

        # Если игра уже была в списке как готовая, то пропуск проверки в стиме
        if any(item for item in current_items if item.value == title_is_ready):
            continue

        title: str = (
            title_is_ready
            if get_price(game.url)
            else f"Игра {game.title!r} не доступна для покупки"
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
    "Появлении цены у игры в Steam",
    DIR,
    get_items,
    formats=Formats(
        get_items="Проверка игры",
        new_item="%s",  # Название статуса будет использовано для описания уведомления
        no_new_items="Изменений нет",
        prefix="🎮",
    ),
)
