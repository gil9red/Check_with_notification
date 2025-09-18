#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о выходе игр из раннего доступа steam.

"""


import sys
import time

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
    Game(
        title="Древние Русы",
        url="https://store.steampowered.com/app/2669860/_/",
    ),
    Game(
        title="Jotunnslayer: Hordes of Hel",
        url="https://store.steampowered.com/app/2820820/Jotunnslayer_Hordes_of_Hel/",
    ),
    Game(
        title="Gloomwood",
        url="https://store.steampowered.com/app/1150760/Gloomwood/?curator_clanid=34055240",
    ),
    Game(
        title="Titan Quest II",
        url="https://store.steampowered.com/app/1154030/Titan_Quest_II/",
    ),
]


def get_items(job: NotificationJob) -> list[DataItem]:
    current_items: list[DataItem] = job.read_items()

    new_items: list[DataItem] = []
    for game in GAMES:
        title_is_ready: str = f"{game.title} готова!"

        # Если игра уже была в списке как готовая, то пропуск проверки в стиме
        if any(item for item in current_items if item.value == title_is_ready):
            continue

        title: str = (
            f"{game.title} в раннем доступе"
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
