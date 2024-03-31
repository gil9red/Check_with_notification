#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении цены игр в Steam.

"""


import sys
from dataclasses import dataclass
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import Formats
from root_common import DataItem, run_notification_job, NotificationJob
from third_party.price_of_games.app_parser.utils import get_price


@dataclass
class Game:
    title: str
    url: str


GAMES: list[Game] = [
    Game(
        title="I Am Jesus Christ",
        url="https://store.steampowered.com/app/1198970/I_Am_Jesus_Christ/",
    ),
    Game(
        title="Cat Quest III",
        url="https://store.steampowered.com/app/2305840/Cat_Quest_III/",
    ),
    Game(
        title="Titan Quest II",
        url="https://store.steampowered.com/app/1154030/Titan_Quest_II/",
    ),
]


def get_items(job: NotificationJob) -> list[DataItem]:
    items: list[DataItem] = []
    for game in GAMES:
        price = get_price(game.title, job.log)
        title = (
            f"Игра {game.title!r} доступна для покупки"
            if price
            else f"Игра {game.title!r} не доступна для покупки"
        )

        items.append(
            DataItem(
                value=title,
                url=game.url,
            )
        )

    return items


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
