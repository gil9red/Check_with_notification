#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import time

from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import get_logger, send_telegram_notification, wait
from third_party.check__haveibeenpwned_com import do_check

import requests


# TODO: попробовать реализовать через run_notification_job

log = get_logger('Проверка через pwned')


FILE_NAME_LAST_VALUE = 'last_value'
DIR_SAVE_PWNED_SCREENSHOTS = 'pwned_screenshots'
CHECK_EMAIL = 'ilya.petrash@inbox.ru'


def update_file_data(value: str):
    open(FILE_NAME_LAST_VALUE, mode='w', encoding='utf-8').write(value)


if __name__ == '__main__':
    need_notification = True

    try:
        last_value = open(FILE_NAME_LAST_VALUE, encoding='utf-8').read()
    except:
        last_value = ''

    while True:
        try:
            log.debug('Check pwned')
            log.debug("Last value: %s", repr(last_value) if last_value else '<empty>')

            value = do_check(CHECK_EMAIL, DIR_SAVE_PWNED_SCREENSHOTS)
            log.debug(f'Current value: {value!r}')

            if not last_value:
                log.debug('Обнаружен первый запуск')

                last_value = value
                update_file_data(last_value)

            else:
                if last_value != value:
                    text = 'PWNED'
                    log.debug(text)

                    last_value = value
                    update_file_data(last_value)

                    if need_notification:
                        send_telegram_notification(log.name, text)

                else:
                    log.debug('Ничего не поменялось...')

            wait(weeks=1)

        except requests.exceptions.ConnectionError as e:
            log.warning('Ошибка подключения к сети: %s', e)
            log.debug('Через минуту попробую снова...')

            time.sleep(60)

        except:
            log.exception('Непредвиденная ошибка:')
            log.debug('Через 5 минут попробую снова...')

            time.sleep(5 * 60)
