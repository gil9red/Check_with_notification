#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
import json
import logging
import sys
import time
import traceback
import uuid

from dataclasses import asdict, dataclass, field
from logging.handlers import RotatingFileHandler
from typing import Callable
from pathlib import Path

import requests
from requests.exceptions import RequestException

from simple_wait import wait

from formats import Formats, FORMATS_DEFAULT
from root_config import (
    API_ID,
    TO,
    DIR,
    FILE_NAME_SAVED,
    FILE_NAME_SAVED_BACKUP,
    DEBUG_LOGGING_CURRENT_ITEMS,
    DEBUG_LOGGING_GET_NEW_ITEMS,
)

# Добавление точки поиска для модулей в third_party
sys.path.append(str(DIR / "third_party"))

from third_party.add_notify_telegram import add_notify
from third_party.youtube_com__results_search_query import search_youtube
from third_party.jut_su.anime_get_video_list import get_video_list as get_video_list_from_jut_su


session = requests.session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"


@dataclass
class DataItem:
    value: str = field(compare=True)
    title: str = field(compare=False, default="")
    url: str = field(compare=False, default="")
    notification_title: str = field(compare=False, repr=False, default="")
    need_html_escape_content: bool = field(compare=False, repr=False, default=True)

    def __post_init__(self):
        if not self.title:
            self.title = self.value

    def dumps(self) -> dict[str, str]:
        data = asdict(self)
        data.pop("need_html_escape_content")  # Не нужно его выгружать
        return data

    @classmethod
    def loads(cls, data: dict[str, str]):
        return cls(**data)


class SavedModeEnum(enum.Enum):
    SIMPLE = enum.auto()
    DATA_ITEM = enum.auto()


@dataclass
class TimeoutWait:
    days: int = 0
    seconds: int = 0
    microseconds: int = 0
    milliseconds: int = 0
    minutes: int = 0
    hours: int = 0
    weeks: int = 0

    def as_dict(self) -> dict[str, int]:
        return asdict(self)


def get_logger(
    name,
    file="log.txt",
    encoding="utf-8",
    log_stdout=True,
    log_file=True,
) -> logging.Logger:
    log = logging.getLogger(name)

    # Если обработчики есть, значит логгер уже создавали
    if log.handlers:
        return log

    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s"
    )

    if log_file:
        fh = RotatingFileHandler(
            file, maxBytes=10000000, backupCount=5, encoding=encoding
        )
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


def get_short_repr_list(items: list) -> str:
    if len(items) <= 4:
        return str(items)

    first, last = list(map(repr, items[:3])), repr(items[-1])
    return "[" + ", ".join(first) + ", ..., " + last + "]"


def send_sms(api_id: str, to: str, text: str, log):
    api_id = api_id.strip()
    to = to.strip()

    if not api_id or not to:
        log.warning("Параметры api_id или to не указаны, отправка СМС невозможна!")
        return

    log.info(f"Отправка sms: {text!r}")

    if len(text) > 70:
        text = text[: 70 - 3] + "..."
        log.info(
            f"Текст sms будет сокращен, т.к. слишком длинное (больше 70 символов): {text!r}"
        )

    # Отправляю смс на номер
    url = f"https://sms.ru/sms/send?api_id={api_id}&to={to}&text={text}"
    log.debug(repr(url))

    while True:
        try:
            rs = session.get(url)
            log.debug(repr(rs.text))
            break

        except:
            log.exception("При отправке sms произошла ошибка:")
            log.debug("Через 5 минут попробую снова...")

            # Wait 5 minutes before next attempt
            time.sleep(5 * 60)


def simple_send_sms(text: str, log=None):
    # Если логгер не определен, тогда создаем свой, который логирует в консоль
    if not log:
        log = get_logger("all_common", log_file=False)

    return send_sms(API_ID, TO, text, log)


def send_telegram_notification(
    name: str,
    message: str,
    type: str = "INFO",
    url: str = None,
    has_delete_button: bool = False,
    show_type: bool = True,
    group: str = None,
    group_max_number: int = None,
    need_html_escape_content: bool = True,
):
    try:
        add_notify(
            name=name,
            message=message,
            type=type,
            url=url,
            has_delete_button=has_delete_button,
            show_type=show_type,
            group=group,
            group_max_number=group_max_number,
            need_html_escape_content=need_html_escape_content,
        )
    except Exception as e:
        log = get_logger("error_send_telegram", file=str(DIR / "errors.txt"))
        log.exception("")

        simple_send_sms(f"[Error] {e}", log)

        # Пробрасываем ошибку, чтобы она не прошла незаметно для скриптов
        raise e


def send_telegram_notification_error(name: str, message: str):
    send_telegram_notification(name, message, "ERROR", has_delete_button=True)


IS_CAN_SEND_ERROR_NOTIFICATIONS: bool = False
IS_SINGLE: bool = "--single" in sys.argv


def log_uncaught_exceptions(ex_cls, ex, tb):
    # Если было запрошено прерывание
    if isinstance(ex, KeyboardInterrupt):
        sys.exit()

    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)

    # Посылаем уведомление только при запуске через задачу
    if IS_CAN_SEND_ERROR_NOTIFICATIONS:
        send_telegram_notification_error("root_common.py", text)

    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


DEFAULT_TIMEOUT_WAIT = TimeoutWait(hours=8)


class NotificationJob:
    @dataclass
    class Callbacks:
        on_start: Callable[["NotificationJob"], None] = lambda job: None
        on_first_start_detected: Callable[["NotificationJob"], None] = lambda job: None
        on_start_check: Callable[["NotificationJob"], None] = lambda job: None
        on_finish_check: Callable[["NotificationJob"], None] = lambda job: None
        on_finish: Callable[["NotificationJob"], None] = lambda job: None

    def __init__(
        self,
        log__or__log_name: logging.Logger | str,
        script_dir: Path | str,
        get_new_items: Callable[["NotificationJob"], list[str | DataItem]],
        *,
        file_name_saved: str = FILE_NAME_SAVED,
        file_name_saved_backup: str = FILE_NAME_SAVED_BACKUP,
        need_notification: bool = True,
        notify_when_empty: bool = True,
        send_new_items_separately: bool = False,
        send_new_items_as_group: bool = False,
        send_new_item_diff: bool = False,
        timeout: TimeoutWait = DEFAULT_TIMEOUT_WAIT,
        timeout_exception_seconds: int = 5 * 60,  # 5 minutes
        formats: Formats = FORMATS_DEFAULT,
        save_mode: SavedModeEnum = SavedModeEnum.SIMPLE,
        url: str = None,
        callbacks: Callbacks = None,
        need_to_store_items: int = None,
        notify_after_sequence_of_errors: bool = True,
        report_errors_for_first_time_after_attempts: int = 5,  # NOTE: Default after 25 minutes
        report_errors_after_each_attempts: int = 100,  # NOTE: Default every 8 hours
        is_single: bool = IS_SINGLE,
        max_attempts_for_is_single: int = 5,  # NOTE: Default after 25 minutes
        debug_logging_current_items: bool = DEBUG_LOGGING_CURRENT_ITEMS,
        debug_logging_get_new_items: bool = DEBUG_LOGGING_GET_NEW_ITEMS,
    ):
        self.script_dir = script_dir
        self.get_new_items = get_new_items
        self.file_name_saved = file_name_saved
        self.file_name_saved_backup = file_name_saved_backup
        self.need_notification = need_notification
        self.notify_when_empty = notify_when_empty
        self.send_new_items_separately = send_new_items_separately
        self.send_new_items_as_group = send_new_items_as_group
        self.send_new_item_diff = send_new_item_diff
        self.timeout = timeout
        self.timeout_exception_seconds = timeout_exception_seconds
        self.formats = formats
        self.save_mode = save_mode
        self.url = url
        self.callbacks = callbacks or self.Callbacks()
        self.need_to_store_items = need_to_store_items
        self.notify_after_sequence_of_errors = notify_after_sequence_of_errors
        self.report_errors_for_first_time_after_attempts = report_errors_for_first_time_after_attempts
        self.report_errors_after_each_attempts = report_errors_after_each_attempts
        self.is_single = is_single
        self.max_attempts_for_is_single = max_attempts_for_is_single
        self.debug_logging_current_items = debug_logging_current_items
        self.debug_logging_get_new_items = debug_logging_get_new_items

        self.log = log__or__log_name
        if isinstance(self.log, str):
            self.log = get_logger(self.log, self.script_dir / "log.txt")

        self.file_name_items = self.script_dir / self.file_name_saved
        self.file_name_skip = self.script_dir / "skip"

    def read_items(self) -> list[DataItem]:
        try:
            with open(self.file_name_items, encoding="utf-8") as f:
                obj = json.load(f)

                # Должен быть список, но если в файле будет что-то другое - это будет неправильно
                if not isinstance(obj, list):
                    return []

                # Поддержка старого формата
                if self.save_mode == SavedModeEnum.SIMPLE or isinstance(obj[0], str):
                    return [DataItem(value=x) for x in obj]
                else:
                    return [DataItem.loads(x) for x in obj]

        except:
            return []

    def save_items(self, items: list[DataItem], items_backup: list[DataItem] = None):
        def _save_to(file_name: str, data: list[DataItem]):
            with open(file_name, mode="w", encoding="utf-8") as f:
                if self.save_mode == SavedModeEnum.SIMPLE:
                    result = [x.value for x in data]
                else:
                    result = [x.dumps() for x in data]

                json.dump(result, f, ensure_ascii=False, indent=4)

        _save_to(self.file_name_items, items)

        # Если элементы для бекапа переданы
        if items_backup:
            _save_to(self.file_name_saved_backup, items_backup)

    def _get_text_items(self, items: list[DataItem]) -> str:
        items = [x.title for x in items]
        return (
            str(items)
            if self.debug_logging_current_items
            else get_short_repr_list(items)
        )

    def run(self):
        global IS_CAN_SEND_ERROR_NOTIFICATIONS
        IS_CAN_SEND_ERROR_NOTIFICATIONS = self.need_notification

        self.log.debug(self.formats.on_start, self.log.name)
        self.callbacks.on_start(self)

        # Если не существует или пустой
        if not self.file_name_items.exists() or not self.file_name_items.stat().st_size:
            self.log.debug(self.formats.first_start_detected)
            self.callbacks.on_first_start_detected(self)

        title = self.formats.process(self.log.name)

        has_sending_first_report_error = False
        attempts = 0

        while True:
            try:
                self.log.debug(self.formats.on_start_check)
                if self.is_single:
                    self.log.debug(self.formats.on_run_is_single)

                self.callbacks.on_start_check(self)

                if self.file_name_skip.exists():
                    self.log.info(
                        self.formats.file_skip_exists, self.file_name_skip.name
                    )
                    if self.is_single:
                        break
                    else:
                        wait(**self.timeout.as_dict())
                        continue

                # Загрузка текущего списка из файла
                current_items = self.read_items()

                text_current_items = self._get_text_items(current_items)
                self.log.debug(
                    self.formats.current_items, len(current_items), text_current_items
                )

                self.log.debug(self.formats.get_items)

                items = self.get_new_items(self)
                if not items and self.notify_when_empty and self.need_notification:
                    self.log.info("An empty list was returned. Sending a notification")
                    send_telegram_notification_error(
                        title, self.formats.when_empty_items
                    )

                # Поддержка старого формата
                if items and isinstance(items[0], str):
                    items = [DataItem(value=x) for x in items]

                text_items = self._get_text_items(items)
                self.log.debug(self.formats.items, len(items), text_items)

                # Если текущих список пустой
                if not current_items:
                    self.save_items(items)

                else:
                    new_items = [x for x in items if x not in current_items]
                    if new_items:
                        number_new_items = len(new_items)

                        # Если один элемент и стоит флаг на вывод разницы элементов
                        if number_new_items == 1 and self.send_new_item_diff:
                            current_item: str = (
                                current_items[0].title if current_items else ""
                            )
                            new_item: DataItem = new_items[0]
                            text = self.formats.new_item_diff % (
                                current_item,
                                new_item.title,
                            )
                            self.log.debug(text)
                            if self.need_notification:
                                url = self.url if self.url else new_item.url

                                notification_title = title
                                if new_item.notification_title:
                                    notification_title = self.formats.process(
                                        new_item.notification_title
                                    )

                                send_telegram_notification(
                                    name=notification_title,
                                    message=text,
                                    url=url,
                                    show_type=False,
                                    need_html_escape_content=new_item.need_html_escape_content,
                                )

                        # Если один элемент или стоит флаг, разрешающий каждый элемент логировать отдельно
                        elif (
                            number_new_items == 1
                            or self.send_new_items_separately
                            or self.send_new_items_as_group
                        ):
                            if self.send_new_items_as_group and number_new_items > 1:
                                group = str(uuid.uuid4())
                                group_max_number = number_new_items
                            else:
                                group = None
                                group_max_number = None

                            for item in new_items:
                                text = self.formats.new_item % item.title
                                self.log.debug(text)
                                if self.need_notification:
                                    url = self.url if self.url else item.url

                                    notification_title = title
                                    if item.notification_title:
                                        notification_title = self.formats.process(
                                            item.notification_title
                                        )

                                    send_telegram_notification(
                                        name=notification_title,
                                        message=text,
                                        url=url,
                                        show_type=False,
                                        group=group,
                                        group_max_number=group_max_number,
                                        need_html_escape_content=item.need_html_escape_content,
                                    )

                        else:
                            # Новые элементы логируем все разом
                            text = self.formats.new_items % (
                                number_new_items,
                                "\n".join(x.title for x in new_items),
                            )
                            self.log.debug(text)
                            if self.need_notification:
                                send_telegram_notification(
                                    title, text, url=self.url, show_type=False
                                )

                        # Если нужно определенное количество элементов хранить
                        if self.need_to_store_items:
                            items = list(current_items)
                            # Добавим новые в начало списка
                            for item in new_items:
                                items.insert(0, item)
                            # Обрежем список, удалив лишние старые элементы
                            items = items[: self.need_to_store_items]

                        # Сохраняем после отправки уведомлений
                        self.save_items(items, current_items)

                    else:
                        self.log.debug(self.formats.no_new_items)

                self.log.debug(self.formats.on_finish_check)
                self.callbacks.on_finish_check(self)

                if self.is_single:
                    break

                # Restore
                has_sending_first_report_error = False
                attempts = 0

                try:
                    wait(**self.timeout.as_dict())
                except OSError as e:
                    # OSError: [Errno 22] Invalid argument
                    if "Invalid argument" in str(e):
                        text = "Unexpected happened - unable to write to stdout, script will exit"
                        self.log.warning(text)
                        if self.need_notification:
                            send_telegram_notification_error(self.log.name, text)
                        sys.exit(0)
                    raise e

            except KeyboardInterrupt:
                break

            except Exception as e:
                # При ошибках с сетью пишем текст ошибке, а не стек
                if isinstance(e, RequestException):
                    self.log.error(f"{self.formats.on_exception} {e}")
                else:
                    self.log.exception(self.formats.on_exception)

                attempts += 1

                # При повторных подряд идущих неуспешных выполнениях сначала отправляется ошибка
                # в первый раз после, на каждые N-раз ошибка с указанием номера попытки
                if (
                    self.notify_after_sequence_of_errors
                    and attempts >= self.report_errors_for_first_time_after_attempts
                    and self.need_notification
                ):
                    if not has_sending_first_report_error:
                        self.log.info("Sending a notification")

                        send_telegram_notification_error(self.log.name, str(e))
                        has_sending_first_report_error = True

                    elif attempts % self.report_errors_after_each_attempts == 0:
                        self.log.info("Sending a notification")

                        text = self.formats.on_exception_with_attempts % (attempts, e)
                        send_telegram_notification_error(self.log.name, text)

                # Слишком много подряд неудачных попыток в режиме is_single
                if self.is_single and attempts >= self.max_attempts_for_is_single:
                    # Отключение отправки уведомления из log_uncaught_exceptions
                    # Т.к. выше уже будет отправлено уведомление об ошибке
                    global IS_CAN_SEND_ERROR_NOTIFICATIONS
                    IS_CAN_SEND_ERROR_NOTIFICATIONS = False

                    raise e

                self.log.debug(self.formats.on_exception_next_attempt, self.timeout_exception_seconds)

                # Wait <timeout_exception_seconds> before next attempt
                time.sleep(self.timeout_exception_seconds)

        self.log.debug(self.formats.on_finish)
        self.callbacks.on_finish(self)


def get_yt_video_list(text_or_url: str) -> list[DataItem]:
    return [
        DataItem(value=video.id, title=video.title, url=video.url)
        for video in search_youtube(text_or_url)
    ]


def get_yt_playlist_video_list(playlist_id: str) -> list[DataItem]:
    url = f"https://www.youtube.com/playlist?list={playlist_id}"
    return get_yt_video_list(url)


def get_yt_video_list_from_playlists(
    job: NotificationJob,
    playlists: list[tuple[str, str]],
) -> list[DataItem]:
    name = job.log.name

    items = []
    for playlist_title, playlist_id in playlists:
        video_list = get_yt_playlist_video_list(playlist_id)
        job.log.info(
            f"Из плейлиста '{playlist_title}' загружено {len(video_list)} видео"
        )

        for item in video_list:
            item.notification_title = f"{playlist_title} [{name}]"
            items.append(item)

    return items


def get_items_from_jut_su(_: NotificationJob, url: str) -> list[DataItem]:
    items = []
    for season, video_list in get_video_list_from_jut_su(url).items():
        for video in video_list:
            title = video.title
            if season:
                title = f"{season}. {title}"

            items.append(
                DataItem(value=title, url=video.url)
            )

    return items


def run_notification_job(
    log__or__log_name: logging.Logger | str,
    script_dir: Path | str,
    get_new_items: Callable[["NotificationJob"], list[str | DataItem]],
    *,
    file_name_saved: str = FILE_NAME_SAVED,
    file_name_saved_backup: str = FILE_NAME_SAVED_BACKUP,
    need_notification: bool = True,
    notify_when_empty: bool = True,
    send_new_items_separately: bool = False,
    send_new_items_as_group: bool = False,
    send_new_item_diff: bool = False,
    timeout: TimeoutWait = DEFAULT_TIMEOUT_WAIT,
    timeout_exception_seconds: int = 5 * 60,  # 5 minutes
    formats: Formats = FORMATS_DEFAULT,
    save_mode: SavedModeEnum = SavedModeEnum.SIMPLE,
    url: str = None,
    callbacks: NotificationJob.Callbacks = None,
    need_to_store_items: int = None,
    notify_after_sequence_of_errors: bool = True,
    report_errors_for_first_time_after_attempts: int = 5,  # NOTE: Default after 25 minutes
    report_errors_after_each_attempts: int = 100,  # NOTE: Default every 8 hours
    is_single: bool = IS_SINGLE,
    max_attempts_for_is_single: int = 5,  # NOTE: Default after 25 minutes
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
        send_new_items_separately=send_new_items_separately,
        send_new_items_as_group=send_new_items_as_group,
        send_new_item_diff=send_new_item_diff,
        timeout=timeout,
        timeout_exception_seconds=timeout_exception_seconds,
        formats=formats,
        save_mode=save_mode,
        url=url,
        callbacks=callbacks,
        need_to_store_items=need_to_store_items,
        notify_after_sequence_of_errors=notify_after_sequence_of_errors,
        report_errors_for_first_time_after_attempts=report_errors_for_first_time_after_attempts,
        report_errors_after_each_attempts=report_errors_after_each_attempts,
        is_single=is_single,
        max_attempts_for_is_single=max_attempts_for_is_single,
        debug_logging_current_items=debug_logging_current_items,
        debug_logging_get_new_items=debug_logging_get_new_items,
    ).run()


if __name__ == "__main__":
    try:
        items = get_short_repr_list([])
        assert items == "[]"

        items = get_short_repr_list([1, 2, 3])
        assert items == "[1, 2, 3]"

        items = get_short_repr_list([1, 2, 3, 4])
        assert items == "[1, 2, 3, 4]"

        items = get_short_repr_list([1, 2, 3, 4, 5])
        assert items == "[1, 2, 3, ..., 5]"

    except:
        print(traceback.format_exc())

    from uuid import uuid4

    item_1 = DataItem(value=uuid4().hex, title=uuid4().hex, url=uuid4().hex)
    item_2 = DataItem.loads(item_1.dumps())
    assert item_1 == item_2
    assert item_1.value == item_2.value
    assert item_1.title == item_2.title
    assert item_1.url == item_2.url

    item_1 = DataItem(value=uuid4().hex, url=uuid4().hex)
    assert item_1.value == item_1.title

    # Проверка совпадения DataItem проверяется только по полю value
    value = uuid4().hex
    item_1 = DataItem(value=uuid4().hex, title=uuid4().hex, url=uuid4().hex)
    item_2 = DataItem(value=item_1.value, title=uuid4().hex, url=uuid4().hex)
    assert item_1 == item_2
