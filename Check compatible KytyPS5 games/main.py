#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о совместимых играх KytyPS5.

"""


import html
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
from third_party.kytyps5__compatibility import Game, get_compatibility

TARGET_GAMES: list[str] = [
    "Demon's Souls",
    "Astro Bot",
    "Gran Turismo 7",
    "Ghost of Yōtei",
    "Marvel’s Wolverine",
]


def get_game_title(game: Game) -> str:
    title: str = html.escape(game.title)
    latest_tested: str = html.escape(game.latest_tested.isoformat())

    lines: list[str] = [
        f"<b>{title}</b>",
        "",
        "\n".join(
            f"<b>{html.escape(os.title())}</b>: <code>{stat}</code>"
            for os, stat in game.os.items()
        ),
        f"<b>Latest Tested:</b> <code>{latest_tested}</code>",
    ]
    return "\n".join(lines)


def get_items(_: NotificationJob) -> list[DataItem]:
    return [
        DataItem(
            value=f"{game.url}, latest_tested: {game.latest_tested}",
            title=get_game_title(game),
            url=game.url,
            need_html_escape_content=False,
        )
        for game in get_compatibility(filters=TARGET_GAMES)
    ]


run_notification_job(
    "Совместимые игры KytyPS5",
    DIR,
    get_items,
    save_mode=SavedModeEnum.DATA_ITEM,
    timeout=TimeoutWait(days=1),
    formats=FORMATS_GAME,
)
