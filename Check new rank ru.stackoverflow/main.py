#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о изменении ранга на ru.stackoverflow.

"""


import sys
import time

from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

import root_common
from root_common import IS_SINGLE, get_logger, send_telegram_notification, wait
from third_party.stackoverflow_site__parsing.user_rank_and_reputation import get_user_rank_and_reputation

import requests


log = get_logger("Изменение ранга в ru.stackoverflow")


FILE_NAME_LAST_RANK = "last_rank"


def update_file_data(value: str):
    with open(FILE_NAME_LAST_RANK, mode="w", encoding="utf-8") as f:
        f.write(value)


if __name__ == "__main__":
    # Чтобы получить в телеграм уведомления о непойманных исключениях
    root_common.IS_CAN_SEND_ERROR_NOTIFICATIONS = True

    need_notification = True

    try:
        last_rank = open(FILE_NAME_LAST_RANK, encoding="utf-8").read()
    except:
        last_rank = ""

    attempts = 0
    max_attempts_for_is_single = 5

    while True:
        try:
            log.debug("get rank and reputation")
            log.debug("last_rank: %s", last_rank if last_rank else "<null>")

            rank, reputation = get_user_rank_and_reputation()

            log.debug("current rank: %s, reputation: %s", rank, reputation)

            # Если предыдущий ранг не был известен, например при первом запуске скрипта
            if not last_rank:
                log.debug("Обнаружен первый запуск")

                last_rank = rank
                update_file_data(last_rank)

            else:
                if last_rank != rank:
                    text = f"Изменился ранг: {last_rank} -> {rank} ({reputation})"
                    log.debug(text)

                    # Обновление последнего ранга
                    last_rank = rank
                    update_file_data(last_rank)

                    if need_notification:
                        send_telegram_notification(log.name, text)

                else:
                    log.debug("Ранг не изменился")

            if IS_SINGLE:
                break

            attempts = 0
            wait(weeks=1)

        except Exception as e:
            attempts += 1

            if isinstance(e, requests.exceptions.RequestException):
                log.warning("Ошибка подключения к сети: %s", e)
            else:
                log.exception("Непредвиденная ошибка:")

            # Слишком много подряд неудачных попыток в режиме is_single
            if IS_SINGLE and attempts >= max_attempts_for_is_single:
                raise e

            log.debug("Через 5 минут попробую снова...")
            time.sleep(5 * 60)
