#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from format import FORMAT_GAME
from root_common import get_logger, wait, send_telegram_notification, send_telegram_notification_error
from third_party.kanobu_ru__games__collections__igry_s_podderzhkoi_rtx import get_games
from db import db_create_backup, Game


log = get_logger("Игры с RTX")


while True:
    log.debug('Запуск')

    is_empty = not Game.select().count()
    if is_empty:
        log.debug('Обнаружен первый запуск')
    else:
        db_create_backup()

    try:
        has_new_game = False

        games = get_games()
        log.debug(f'Обработка {len(games)} игр')

        if not games:
            send_telegram_notification_error(log.name, FORMAT_GAME.when_empty_items)

        for game in games:
            game_db, created = Game.get_or_create(
                name=game.name,
                url=game.url
            )
            if game_db.img_base64 != game.img_base64:
                game_db.img_base64 = game.img_base64
                game_db.save()

            if not created:
                continue

            has_new_game = True
            log.debug(f'Добавление новой игры с RTX: {game.name!r}')

            # При первом запуске не нужно информировать по СМС
            if not is_empty:
                text = f'RTX: {game.name}'
                send_telegram_notification(log.name, text)

        if not has_new_game and games:
            log.debug(f'Новых игр нет')

        wait(weeks=1)

    except Exception as e:
        log.exception('Ошибка:')

        wait(minutes=15)

    print()
