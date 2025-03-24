#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении цены игр в Steam.

"""


import sys
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup, Tag

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import Formats
from root_common import DataItem, run_notification_job, NotificationJob, session


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
        title="Little Nightmares III",
        url="https://store.steampowered.com/app/1392860/Little_Nightmares_III/",
    ),
    Game(
        title="Titan Quest II",
        url="https://store.steampowered.com/app/1154030/Titan_Quest_II/",
    ),
    Game(
        title="MOUSE: P.I. For Hire",
        url="https://store.steampowered.com/app/2416450/MOUSE_PI_For_Hire/",
    ),
    Game(
        title="Heroes of Might & Magic: Olden Era",
        url="https://store.steampowered.com/app/3105440/Heroes_of_Might__Magic_Olden_Era/",
    ),
]


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


def get_items(_: NotificationJob) -> list[DataItem]:
    items: list[DataItem] = []
    for game in GAMES:
        price = get_price(game.url)
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
