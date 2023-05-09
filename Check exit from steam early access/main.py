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


def get_games() -> list[Game]:
    return [
        Game(
            title="Ultrakill",
            url="https://store.steampowered.com/app/1229490/ULTRAKILL/",
        ),
        Game(
            title="Turbo Overkill",
            url="https://store.steampowered.com/app/1328350/Turbo_Overkill/",
        ),
    ]


def get_items(_: NotificationJob) -> list[DataItem]:
    return [
        DataItem(
            value=game.title + (" в раннем доступе" if is_early_access(game.url) else " готова!"),
            url=game.url,
        )
        for game in get_games()
    ]


run_notification_job(
    "Выход из раннего доступа steam",
    DIR,
    get_items,
    formats=FORMATS_GAME,
    send_new_items_separately=True,
)
