#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

import root_common
from formats import FORMATS_GAME
from root_config import DEBUG_LOGGING_GET_NEW_ITEMS
from root_common import (
    get_logger,
    wait,
    send_telegram_notification,
    send_telegram_notification_error,
    get_short_repr_list,
)
from third_party.kanobu_ru__games__collections__igry_s_podderzhkoi_rtx import get_games
from db import db_create_backup, Game


log = get_logger("Игры с RTX")

# Чтобы получить в телеграм уведомления о непойманных исключениях
root_common.IS_CAN_SEND_ERROR_NOTIFICATIONS = True

while True:
    log.debug("Запуск")

    is_empty = not Game.select().count()
    if is_empty:
        log.debug("Обнаружен первый запуск")
    else:
        db_create_backup()

    try:
        has_new_game = False

        games = get_games()
        logged_games = [x.name for x in games]
        text_games = logged_games if DEBUG_LOGGING_GET_NEW_ITEMS else get_short_repr_list(logged_games)
        log.debug("Обработка (%s) игр: %s", len(games), text_games)

        if not games:
            send_telegram_notification_error(log.name, FORMATS_GAME.when_empty_items)

        for game in games:
            game_db = Game.get_or_none(name=game.name)

            # Если игра уже в базе
            if game_db:
                # Если поменялась обложка
                if game_db.img_base64 != game.img_base64:
                    game_db.img_base64 = game.img_base64
                    game_db.save()

                continue

            # Создаем игру
            game_db = Game.create(
                name=game.name,
                url=game.url,
                img_base64=game.img_base64,
            )

            has_new_game = True
            log.debug(f"Добавление новой игры с RTX: {game.name!r}")

            # При первом запуске не нужно информировать по СМС
            if not is_empty:
                text = f"RTX: {game.name}"
                send_telegram_notification(log.name, text)

        if not has_new_game and games:
            log.debug(f"Новых игр нет")

        wait(weeks=1)

    except Exception as e:
        log.exception("Ошибка:")

        wait(minutes=15)

    print()
