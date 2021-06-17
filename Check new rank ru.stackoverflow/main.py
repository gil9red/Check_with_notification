#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о изменении ранга на ru.stackoverflow.

"""


# TODO: попробовать реализовать через run_notification_job

import sys
import time

from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import get_logger, simple_send_sms, wait
from third_party.stackoverflow_site__parsing.user_rank_and_reputation import get_user_rank_and_reputation

import requests


log = get_logger('Изменение ранга в ru.stackoverflow')


FILE_NAME_LAST_RANK = 'last_rank'


def update_file_data(value: str):
    open(FILE_NAME_LAST_RANK, mode='w', encoding='utf-8').write(value)


if __name__ == '__main__':
    notified_by_sms = True

    try:
        last_rank = open(FILE_NAME_LAST_RANK, encoding='utf-8').read()
    except:
        last_rank = ''

    while True:
        try:
            log.debug('get rank and reputation')
            log.debug('last_rank: %s', last_rank if last_rank else '<null>')

            rank, reputation = get_user_rank_and_reputation()

            log.debug('current rank: %s, reputation: %s', rank, reputation)

            # Если предыдущий ранг не был известен, например при первом запуске скрипта
            if not last_rank:
                log.debug('Обнаружен первый запуск')

                last_rank = rank
                update_file_data(last_rank)

            else:
                if last_rank != rank:
                    text = 'Изменился ранг: {} -> {} ({})'.format(last_rank, rank, reputation)
                    log.debug(text)

                    # Обновление последнего ранга
                    last_rank = rank
                    update_file_data(last_rank)

                    if notified_by_sms:
                        simple_send_sms(text, log)

                else:
                    log.debug('Ранг не изменился')

            wait(weeks=1)

        except requests.exceptions.ConnectionError as e:
            log.warning('Ошибка подключения к сети: %s', e)
            log.debug('Через минуту попробую снова...')

            time.sleep(60)

        except:
            log.exception('Непредвиденная ошибка:')
            log.debug('Через 5 минут попробую снова...')

            time.sleep(5 * 60)
