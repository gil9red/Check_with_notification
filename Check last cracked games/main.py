#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых взломанных играх.

"""


import html
import sys

from inspect import cleandoc
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
from third_party.gamestatus_info__lastcrackedgames import Game, get_games


DATE_FORMAT: str = "%d.%m.%Y"


def get_game_title(game: Game) -> str:
    title: str = html.escape(game.title)
    protection: str = html.escape(game.protection)
    hacked: str = html.escape(game.hacked_groups)
    release_date: str = (
        game.release_date.strftime(DATE_FORMAT) if game.release_date else "Ожидается"
    )
    crack_date: str = (
        game.crack_date.strftime(DATE_FORMAT) if game.crack_date else "Не взломана"
    )

    return cleandoc(
        f"""
        <b>{title}</b>
        
        📅 <b>Дата релиза:</b> <code>{release_date}</code>
        🔓 <b>Дата взлома:</b> <code>{crack_date}</code>
        🛡 <b>Защита:</b> <code>{protection}</code>
        🏴‍☠️ <b>Взломана:</b>
        <blockquote>{hacked}</blockquote>
        """
    ).strip()


def get_items(_: NotificationJob) -> list[DataItem]:
    return [
        DataItem(
            value=game.url,
            title=get_game_title(game),
            url=game.url,
            need_html_escape_content=False,
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
