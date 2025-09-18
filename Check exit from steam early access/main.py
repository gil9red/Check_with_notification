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
    Game(
        title="Witchfire",
        url="https://store.steampowered.com/app/3156770/Witchfire/",
    ),
    Game(
        title="Selaco",
        url="https://store.steampowered.com/app/1592280/Selaco/",
    ),
    Game(
        title="BRUTAL JOHN 2",
        url="https://store.steampowered.com/app/1859620/BRUTAL_JOHN_2/",
    ),
    Game(
        title="Project Silverfish",
        url="https://store.steampowered.com/app/2941710/Project_Silverfish/",
    ),
    Game(
        title="VOID/BREAKER",
        url="https://store.steampowered.com/app/2615540/VOIDBREAKER/",
    ),
    Game(
        title="Conquest Dark",
        url="https://store.steampowered.com/app/3238670/Conquest_Dark/",
    ),
    Game(
        title="Ketz: Galactic Overlords",
        url="https://store.steampowered.com/app/2542140/Ketz_Galactic_Overlords/",
    ),
    Game(
        title="Godslayer Arena",
        url="https://store.steampowered.com/app/2870430/Godslayer_Arena/",
    ),
    Game(
        title="The Spell Brigade",
        url="https://store.steampowered.com/app/2904000/The_Spell_Brigade/",
    ),
    Game(
        title="Demon Hunt",
        url="https://store.steampowered.com/app/3039910/Demon_Hunt/",
    ),
    Game(
        title="Asgard's Fall — Viking Survivors",
        url="https://store.steampowered.com/app/2780710/Asgards_Fall__Viking_Survivors/",
    ),
    Game(
        title="Noobs Are Coming",
        url="https://store.steampowered.com/app/2225960/Noobs_Are_Coming/",
    ),
    Game(
        title="NIMRODS",
        url="https://store.steampowered.com/app/2086430/NIMRODS/",
    ),
    Game(
        title="Funguys Swarm",
        url="https://store.steampowered.com/app/3371770/Funguys_Swarm/",
    ),
    Game(
        title="Be My Horde",
        url="https://store.steampowered.com/app/2499520/Be_My_Horde/",
    ),
    Game(
        title="Temtem: Swarm",
        url="https://store.steampowered.com/app/2510960/Temtem_Swarm/",
    ),
    Game(
        title="Yokai Survivor",
        url="https://store.steampowered.com/app/3514690/Yokai_Survivor/",
    ),
    Game(
        title="KOTARO Survivor",
        url="https://store.steampowered.com/app/3243710/KOTARO_Survivor/",
    ),
    Game(
        title="Survivor Mercs",
        url="https://store.steampowered.com/app/2141520/Survivor_Mercs/",
    ),
    Game(
        title="Driveloop: Survivors",
        url="https://store.steampowered.com/app/3183730/Driveloop_Survivors/",
    ),
    Game(
        title="Letter Lancers",
        url="https://store.steampowered.com/app/2522160/Letter_Lancers/",
    ),
    Game(
        title="Slingbot Survivors",
        url="https://store.steampowered.com/app/3432800/Slingbot_Survivors/",
    ),
    Game(
        title="Survivors of Mayhem",
        url="https://store.steampowered.com/app/2559500/Survivors_of_Mayhem/",
    ),
    Game(
        title="BRUTUS MAXIMUS",
        url="https://store.steampowered.com/app/2928450/BRUTUS_MAXIMUS/",
    ),
    Game(
        title="Letifer",
        url="https://store.steampowered.com/app/2294640/Letifer/",
    ),
    Game(
        title="Pizza Delivery Survivors",
        url="https://store.steampowered.com/app/2840910/Pizza_Delivery_Survivors/",
    ),
    Game(
        title="Tiny Chaos",
        url="https://store.steampowered.com/app/2500680/Tiny_Chaos/",
    ),
    Game(
        title="Mad World Survivors",
        url="https://store.steampowered.com/app/2117370/Mad_World_Survivors/",
    ),
]


def get_items(job: NotificationJob) -> list[DataItem]:
    current_items: list[DataItem] = job.read_items()

    new_items: list[DataItem] = []
    for game in GAMES:
        title_is_ready: str = f"{game.title!r} готова!"

        # Если игра уже была в списке как готовая, то пропуск проверки в стиме
        if any(item for item in current_items if item.value == title_is_ready):
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
