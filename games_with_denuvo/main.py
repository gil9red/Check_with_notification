#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для периодического сбора игр с защитой Denuvo и занесения их в базу.

"""


import time
import sys

from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from common import init_db, log, append_list_games_which_denuvo_is_removed, append_list_games, db_create_backup
from format import FORMAT_GAME
from games_with_denuvo import get_games_with_denuvo, get_games_which_denuvo_is_removed
from root_common import wait, send_telegram_notification_error


# connect = create_connect()
# connect.execute("DROP TABLE IF EXISTS Game")
# connect.commit()

init_db()

# NOTE: С этим флагом нужно быть осторожным при первом запуске, когда база пуста,
# ведь на каждую добавленную взломанную игру отправится уведомление по смс
need_notification = True

while True:
    try:
        log.debug('get_games_with_denuvo')

        games = get_games_with_denuvo()
        log.debug('games (%s): %s', len(games), games)

        if need_notification and not games:
            send_telegram_notification_error(log.name, FORMAT_GAME.when_empty_items)

        games_without_denuvo = get_games_which_denuvo_is_removed()
        log.debug('games_without_denuvo (%s): %s', len(games_without_denuvo), games_without_denuvo)

        changed_1 = append_list_games_which_denuvo_is_removed(games_without_denuvo, need_notification)
        changed_2 = append_list_games(games, need_notification)

        if changed_1 or changed_2:
            db_create_backup()

        wait(days=3)

    except Exception:
        log.exception('Ошибка:')
        log.debug('Через 5 минут попробую снова...')

        # Wait 5 minutes before next attempt
        time.sleep(5 * 60)
