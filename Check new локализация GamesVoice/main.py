#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о новых локализациях GamesVoice.

"""


from pathlib import Path

from formats import FORMATS_GAME
from root_common import NotificationJob, DataItem, SavedModeEnum, run_notification_job
from third_party.gamesvoice_ru__get_finished import get_games

DIR = Path(__file__).resolve().parent


def get_items(_: NotificationJob) -> list[DataItem]:
    return [
        DataItem(
            value=game.title_eng,
            url=game.url,
        )
        for game in get_games()
    ]


run_notification_job(
    "Локализация GamesVoice",
    DIR,
    get_items,
    formats=FORMATS_GAME.replace(
        prefix="📣",
    ),
    save_mode=SavedModeEnum.DATA_ITEM,
)
