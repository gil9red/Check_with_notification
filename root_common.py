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

from formats import Formats, FORMATS_DEFAULT
from root_config import (
    API_ID, TO, DIR, FILE_NAME_SAVED, FILE_NAME_SAVED_BACKUP, DEBUG_LOGGING_CURRENT_ITEMS, DEBUG_LOGGING_GET_NEW_ITEMS
)

# Добавление точки поиска для модулей в third_party
sys.path.append(str(DIR / 'third_party'))

from third_party.wait import wait
from third_party.add_notify_telegram import add_notify
from third_party.youtube_com__results_search_query import search_youtube_with_filter


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
    return search_youtube_with_filter(url)


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


STARTED_WITH_JOB = False


def log_uncaught_exceptions(ex_cls, ex, tb):
    # Если было запрошено прерывание
    if isinstance(ex, KeyboardInterrupt):
        sys.exit()

    text = f'{ex_cls.__name__}: {ex}:\n'
    text += ''.join(traceback.format_tb(tb))

    print(text)

    # Посылаем уведомление только при запуске через задачу
    if STARTED_WITH_JOB:
        send_telegram_notification_error('root_common.py', text)

    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class NotificationJob:
    class Callbacks(NamedTuple):
        on_start: Callable[['NotificationJob'], None] = lambda job: None
        on_first_start_detected: Callable[['NotificationJob'], None] = lambda job: None
        on_start_check: Callable[['NotificationJob'], None] = lambda job: None
        on_finish_check: Callable[['NotificationJob'], None] = lambda job: None
        on_finish: Callable[['NotificationJob'], None] = lambda job: None

    def __init__(
            self,
            log__or__log_name: Union['logging.Logger', str],
            script_dir: Union[Path, str],
            get_new_items: Callable[['NotificationJob'], List[str]],
            *,
            file_name_saved: str = FILE_NAME_SAVED,
            file_name_saved_backup: str = FILE_NAME_SAVED_BACKUP,
            need_notification=True,
            notify_when_empty=True,
            log_new_items_separately=False,
            log_new_item_diff=False,
            timeout=TimeoutWait(days=1),
            timeout_exception_seconds=5 * 60,
            formats: Formats = FORMATS_DEFAULT,
            callbacks: Callbacks = None,
            need_to_store_items: int = None,
            notify_after_sequence_of_errors=True,
            attempts_before_notification=5,
            debug_logging_current_items: bool = DEBUG_LOGGING_CURRENT_ITEMS,
            debug_logging_get_new_items: bool = DEBUG_LOGGING_GET_NEW_ITEMS,
    ):
        self.script_dir = script_dir
        self.get_new_items = get_new_items
        self.file_name_saved = file_name_saved
        self.file_name_saved_backup = file_name_saved_backup
        self.need_notification = need_notification
        self.notify_when_empty = notify_when_empty
        self.log_new_items_separately = log_new_items_separately
        self.log_new_item_diff = log_new_item_diff
        self.timeout = timeout
        self.timeout_exception_seconds = timeout_exception_seconds
        self.formats = formats
        self.callbacks = callbacks or self.Callbacks()
        self.need_to_store_items = need_to_store_items
        self.notify_after_sequence_of_errors = notify_after_sequence_of_errors
        self.attempts_before_notification = attempts_before_notification
        self.debug_logging_current_items = debug_logging_current_items
        self.debug_logging_get_new_items = debug_logging_get_new_items

        self.log = log__or__log_name
        if isinstance(self.log, str):
            self.log = get_logger(self.log, self.script_dir / 'log.txt')

        self.file_name_items = self.script_dir / self.file_name_saved
        self.file_name_skip = self.script_dir / 'skip'

    def read_items(self) -> List[str]:
        try:
            with open(self.file_name_items, encoding='utf-8') as f:
                obj = json.load(f)

                # Должен быть список, но если в файле будет что-то другое -- это будет неправильно
                if not isinstance(obj, list):
                    return []

                return obj

        except:
            return []

    def save_items(self, items: List[str], items_backup: List[str] = None):
        def _save_to(file_name: str, data: List[str]):
            with open(file_name, mode='w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        _save_to(self.file_name_items, items)

        # Если элементы для бекапа переданы
        if items_backup:
            _save_to(self.file_name_saved_backup, items_backup)

    def _get_text_items(self, items: List[str]) -> str:
        return items if self.debug_logging_current_items else get_short_repr_list(items)

    def run(self):
        global STARTED_WITH_JOB
        STARTED_WITH_JOB = True

        self.log.debug(self.formats.on_start)
        self.callbacks.on_start(self)

        # Если не существует или пустой
        if not self.file_name_items.exists() or not self.file_name_items.stat().st_size:
            self.log.debug(self.formats.first_start_detected)
            self.callbacks.on_first_start_detected(self)

        has_sending_notification = False
        attempts = 0

        while True:
            try:
                self.log.debug(self.formats.on_start_check)
                self.callbacks.on_start_check(self)

                if self.file_name_skip.exists():
                    self.log.info(self.formats.file_skip_exists, self.file_name_skip.name)
                    wait(**self.timeout.as_dict())
                    continue

                # Загрузка текущего списка из файла
                current_items = self.read_items()

                text_current_items = self._get_text_items(current_items)
                self.log.debug(self.formats.current_items, len(current_items), text_current_items)

                self.log.debug(self.formats.get_items)

                items = self.get_new_items(self)
                if not items and self.notify_when_empty:
                    send_telegram_notification_error(self.log.name, self.formats.when_empty_items)

                text_items = self._get_text_items(items)
                self.log.debug(self.formats.items, len(items), text_items)

                # Если текущих список пустой
                if not current_items:
                    self.save_items(items)

                else:
                    new_items = [x for x in items if x not in current_items]
                    if new_items:
                        # Если один элемент и стоит флаг на вывод разницы элементов
                        if len(new_items) == 1 and self.log_new_item_diff:
                            current_item = current_items[0] if current_items else ''
                            new_item = new_items[0]
                            text = self.formats.new_item_diff % (current_item, new_item)
                            self.log.debug(text)
                            if self.need_notification:
                                send_telegram_notification(self.log.name, text)

                        # Если один элемент или стоит флаг, разрешающий каждый элемент логировать отдельно
                        elif len(new_items) == 1 or self.log_new_items_separately:
                            for item in new_items:
                                text = self.formats.new_item % item
                                self.log.debug(text)
                                if self.need_notification:
                                    send_telegram_notification(self.log.name, text)
                        else:
                            # Новые элементы логируем все разом
                            text = self.formats.new_items % (len(new_items), '\n'.join(new_items))
                            self.log.debug(text)
                            if self.need_notification:
                                send_telegram_notification(self.log.name, text)

                        # Если нужно определенное количество элементов хранить
                        if self.need_to_store_items:
                            items = list(current_items)
                            # Добавим новые в начало списка
                            for item in new_items:
                                items.insert(0, item)
                            # Обрежем список, удалив лишние старые элементы
                            items = items[:self.need_to_store_items]

                        # Сохраняем после отправки уведомлений
                        self.save_items(items, current_items)

                    else:
                        self.log.debug(self.formats.no_new_items)

                self.log.debug(self.formats.on_finish_check)
                self.callbacks.on_finish_check(self)

                # Restore
                has_sending_notification = False
                attempts = 0

                wait(**self.timeout.as_dict())

            except KeyboardInterrupt:
                break

            except Exception as e:
                self.log.exception(self.formats.on_exception)
                self.log.debug(self.formats.on_exception_next_attempt)

                attempts += 1
                if self.notify_after_sequence_of_errors \
                        and attempts >= self.attempts_before_notification \
                        and not has_sending_notification:
                    send_telegram_notification_error(self.log.name, str(e))
                    has_sending_notification = True

                # Wait <timeout_exception_seconds> before next attempt
                time.sleep(self.timeout_exception_seconds)

        self.log.debug(self.formats.on_finish)
        self.callbacks.on_finish(self)


def run_notification_job(
    log__or__log_name: Union['logging.Logger', str],
    script_dir: Union[Path, str],
    get_new_items: Callable[['NotificationJob'], List[str]],
    *,
    file_name_saved: str = FILE_NAME_SAVED,
    file_name_saved_backup: str = FILE_NAME_SAVED_BACKUP,
    need_notification=True,
    notify_when_empty=True,
    log_new_items_separately=False,
    log_new_item_diff=False,
    timeout=TimeoutWait(days=1),
    timeout_exception_seconds=5 * 60,
    formats: Formats = FORMATS_DEFAULT,
    callbacks: NotificationJob.Callbacks = None,
    need_to_store_items: int = None,
    notify_after_sequence_of_errors=True,
    attempts_before_notification=5,
    debug_logging_current_items: bool = DEBUG_LOGGING_CURRENT_ITEMS,
    debug_logging_get_new_items: bool = DEBUG_LOGGING_GET_NEW_ITEMS,
):
    NotificationJob(
        log__or__log_name=log__or__log_name,
        script_dir=script_dir,
        get_new_items=get_new_items,
        file_name_saved=file_name_saved,
        file_name_saved_backup=file_name_saved_backup,
        need_notification=need_notification,
        notify_when_empty=notify_when_empty,
        log_new_items_separately=log_new_items_separately,
        log_new_item_diff=log_new_item_diff,
        timeout=timeout,
        timeout_exception_seconds=timeout_exception_seconds,
        formats=formats,
        callbacks=callbacks,
        need_to_store_items=need_to_store_items,
        notify_after_sequence_of_errors=notify_after_sequence_of_errors,
        attempts_before_notification=attempts_before_notification,
        debug_logging_current_items=debug_logging_current_items,
        debug_logging_get_new_items=debug_logging_get_new_items,
    ).run()


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
