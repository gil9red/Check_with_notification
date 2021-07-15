#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import logging
import sys
import time
import traceback

from logging.handlers import RotatingFileHandler
from typing import Callable, List, Union, NamedTuple, Dict
from pathlib import Path

import requests

from format import Format, FORMAT_DEFAULT
from root_config import API_ID, TO, DIR, FILE_NAME_SAVED, DEBUG_LOGGING_CURRENT_ITEMS, DEBUG_LOGGING_GET_NEW_ITEMS

# Добавление точки поиска для модулей в third_party
sys.path.append(str(DIR / 'third_party'))

from third_party.wait import wait
from third_party.add_notify_telegram import add_notify
from third_party.youtube_com__get_video_list import get_video_list


class TimeoutWait(NamedTuple):
    days: int = 0
    seconds: int = 0
    microseconds: int = 0
    milliseconds: int = 0
    minutes: int = 0
    hours: int = 0
    weeks: int = 0

    def as_dict(self) -> Dict[str, int]:
        return dict(self._asdict())


def get_logger(name, file='log.txt', encoding='utf-8', log_stdout=True, log_file=True) -> 'logging.Logger':
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

    if log_file:
        fh = RotatingFileHandler(file, maxBytes=10000000, backupCount=5, encoding=encoding)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


def get_playlist_video_list(playlist_id: str):
    url = 'https://www.youtube.com/playlist?list=' + playlist_id
    return get_video_list(url)


def get_short_repr_list(items: List) -> str:
    if len(items) <= 4:
        return str(items)

    first, last = list(map(repr, items[:3])), repr(items[-1])
    return '[' + ', '.join(first) + ', ..., ' + last + ']'


def send_sms(api_id: str, to: str, text: str, log):
    api_id = api_id.strip()
    to = to.strip()

    if not api_id or not to:
        log.warning('Параметры api_id или to не указаны, отправка СМС невозможна!')
        return

    log.info(f'Отправка sms: {text!r}')

    if len(text) > 70:
        text = text[:70-3] + '...'
        log.info(f'Текст sms будет сокращен, т.к. слишком длинное (больше 70 символов): {text!r}')

    # Отправляю смс на номер
    url = 'https://sms.ru/sms/send?api_id={api_id}&to={to}&text={text}'.format(
        api_id=api_id,
        to=to,
        text=text
    )
    log.debug(repr(url))

    while True:
        try:
            rs = requests.get(url)
            log.debug(repr(rs.text))
            break

        except:
            log.exception("При отправке sms произошла ошибка:")
            log.debug('Через 5 минут попробую снова...')

            # Wait 5 minutes before next attempt
            time.sleep(5 * 60)


def simple_send_sms(text: str, log=None):
    # Если логгер не определен, тогда создаем свой, который логирует в консоль
    if not log:
        log = get_logger('all_common', log_file=False)

    return send_sms(API_ID, TO, text, log)


def send_telegram_notification(name: str, message: str, type='INFO'):
    try:
        add_notify(name=name, message=message, type=type)
    except Exception as e:
        log = get_logger('error_send_telegram', file=str(DIR / 'errors.txt'))
        log.exception('')

        simple_send_sms(f'[Error] {e}', log)

        # Пробрасываем ошибку, чтобы она не прошла незаметно для скриптов
        raise e


def send_telegram_notification_error(name: str, message: str):
    send_telegram_notification(name, message, 'ERROR')


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f'{ex_cls.__name__}: {ex}:\n'
    text += ''.join(traceback.format_tb(tb))

    print(text)
    send_telegram_notification_error('root_common.py', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


def read_items(file_name_items: Path) -> List[str]:
    try:
        with open(file_name_items, encoding='utf-8') as f:
            obj = json.load(f)

            # Должен быть список, но если в файле будет что-то другое -- это будет неправильно
            if not isinstance(obj, list):
                return []

            return obj

    except:
        return []


def save_items(file_name_items: Path, items: List[str]):
    with open(file_name_items, mode='w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=4)


def run_notification_job(
    log__or__log_name: Union['logging.Logger', str],
    script_dir: Union[Path, str],
    get_new_items: Callable[[], List[str]],
    need_notification=True,
    notify_when_empty=True,
    log_new_items_separately=False,
    timeout=TimeoutWait(days=1),
    timeout_exception_seconds=5 * 60,
    format: Format = FORMAT_DEFAULT,
):
    log = log__or__log_name
    if isinstance(log, str):
        log = get_logger(log, script_dir / 'log.txt')

    log.debug(format.on_start)

    file_name_items = script_dir / FILE_NAME_SAVED

    # Если не существует или пустой
    if not file_name_items.exists() or not file_name_items.stat().st_size:
        log.debug(format.first_start_detected)

    file_name_skip = script_dir / 'skip'

    while True:
        try:
            log.debug(format.on_start_check)

            if file_name_skip.exists():
                log.info(format.file_skip_exists, file_name_skip.name)
                wait(**timeout.as_dict())
                continue

            # Загрузка текущего списка из файла
            current_items = read_items(file_name_items)

            text_current_items = current_items if DEBUG_LOGGING_CURRENT_ITEMS else get_short_repr_list(current_items)
            log.debug(format.current_items, len(current_items), text_current_items)

            log.debug(format.get_items)

            items = get_new_items()
            if not items and notify_when_empty:
                send_telegram_notification_error(log.name, format.when_empty_items)

            text_items = items if DEBUG_LOGGING_GET_NEW_ITEMS else get_short_repr_list(items)
            log.debug(format.items, len(items), text_items)

            # Если текущих список пустой
            if not current_items:
                save_items(file_name_items, items)

            else:
                new_items = set(items) - set(current_items)
                if new_items:
                    # Если один элемент или стоит флаг, разрешающий каждый элемент логировать отдельно
                    if len(new_items) == 1 or log_new_items_separately:
                        for item in new_items:
                            text = format.new_item % item
                            log.debug(text)
                            if need_notification:
                                send_telegram_notification(log.name, text)
                    else:
                        # Новые элементы логируем все разом
                        text = format.new_items % (len(new_items), '\n'.join(new_items))
                        log.debug(text)
                        if need_notification:
                            send_telegram_notification(log.name, text)

                    # Сохраняем после отправки уведомлений
                    save_items(file_name_items, items)

                else:
                    log.debug(format.no_new_items)

            log.debug(format.on_finish_check)

            wait(**timeout.as_dict())

        except:
            log.exception(format.on_exception)
            log.debug(format.on_exception_next_attempt)

            # Wait <timeout_exception_seconds> before next attempt
            time.sleep(timeout_exception_seconds)


if __name__ == '__main__':
    try:
        items = get_short_repr_list([])
        assert items == '[]'

        items = get_short_repr_list([1, 2, 3])
        assert items == '[1, 2, 3]'

        items = get_short_repr_list([1, 2, 3, 4])
        assert items == '[1, 2, 3, 4]'

        items = get_short_repr_list([1, 2, 3, 4, 5])
        assert items == '[1, 2, 3, ..., 5]'

    except:
        print(traceback.format_exc())
