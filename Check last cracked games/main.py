#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых взломанных играх.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_GAME
from root_common import (
    NotificationJob,
    DataItem,
    run_notification_job,
    SavedModeEnum,
    TimeoutWait,
)
from third_party.gamestatus_info__lastcrackedgames import get_games


def get_items(_: NotificationJob) -> list[DataItem]:
    return [
        DataItem(
            value=game.url,
            title=(
                f"{game.title}\n(релиз {game.release_date:%d/%m/%Y}, "
                f"взлом {game.crack_date:%d/%m/%Y}, защита {game.protection})"
            ),
            url=game.url,
        )
        for game in get_games()
    ]


run_notification_job(
    "Новые взломанные игры",
    DIR,
    get_items,
    save_mode=SavedModeEnum.DATA_ITEM,
    timeout=TimeoutWait(days=1),
    formats=FORMATS_GAME,
)
