#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о выходе игр из раннего доступа steam.

"""


import sys

from dataclasses import dataclass
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_GAME
from root_common import NotificationJob, DataItem, run_notification_job
from third_party.store_steampowered_com__check_early_access import is_early_access


@dataclass
class Game:
    title: str
    url: str


GAMES: list[Game] = [
    Game(
        title="Ultrakill",
        url="https://store.steampowered.com/app/1229490/ULTRAKILL/",
    ),
    Game(
        title="Turbo Overkill",
        url="https://store.steampowered.com/app/1328350/Turbo_Overkill/",
    ),
    Game(
        title="Wizordum",
        url="https://store.steampowered.com/app/1715590/Wizordum/",
    ),
    Game(
        title="Soulstone Survivors",
        url="https://store.steampowered.com/app/2066020/Soulstone_Survivors/",
    ),
    Game(
        title="Hades II",
        url="https://store.steampowered.com/app/1145350/Hades_II/",
    ),
    Game(
        title="Death Must Die",
        url="https://store.steampowered.com/app/2334730/Death_Must_Die/",
    ),
    Game(
        title="Deep Rock Galactic: Survivor",
        url="https://store.steampowered.com/app/2321470/Deep_Rock_Galactic_Survivor/",
    ),
]


def get_items(_: NotificationJob) -> list[DataItem]:
    return [
        DataItem(
            value=game.title + (" в раннем доступе" if is_early_access(game.url) else " готова!"),
            url=game.url,
        )
        for game in GAMES
    ]


run_notification_job(
    "Выход из раннего доступа steam",
    DIR,
    get_items,
    formats=FORMATS_GAME,
    send_new_items_separately=True,
)
