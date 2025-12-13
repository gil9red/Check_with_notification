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
from typing import Any, Callable
from pathlib import Path

import requests
from requests.exceptions import RequestException

from simple_wait import wait

from formats import Formats, FORMATS_DEFAULT, FORMATS_VIDEO
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
from third_party.jut_su.anime_get_video_list import (
    get_video_list as get_video_list_from_jut_su,
)
from third_party.rutube.get_videos_from_playlist import (
    get_videos as get_videos_from_playlist_rutube,
)
from third_party.rutube.get_videos_from_channel import (
    get_videos as get_videos_from_channel_rutube,
)
from third_party.youtube_com.api.search import search_youtube


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"


@dataclass
class DataItem:
    value: str = field(compare=True)
    title: str = field(compare=False, default="")
    url: str = field(compare=False, default="")
    notification_title: str = field(compare=False, repr=False, default="")
    prefix: str = field(compare=False, repr=False, default="")
    need_html_escape_content: bool = field(compare=False, repr=False, default=True)

    def __post_init__(self):
        if not self.title:
            self.title = self.value

    def process_notification_title(self, formats: Formats, default: str) -> str:
        notification_title: str = self.notification_title or default
        if self.prefix:
            formats = formats.replace(prefix=self.prefix)
        return formats.process(notification_title)

    def dumps(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("need_html_escape_content")  # Не нужно его выгружать
        data.pop("prefix")
        return data

    @classmethod
    def loads(cls, data: dict[str, Any]):
        return cls(**data)


class SavedModeEnum(enum.Enum):
    SIMPLE = enum.auto()
    DATA_ITEM = enum.auto()


class SendNewItemsModeEnum(enum.Enum):
    SINGLE_MESSAGE = enum.auto()
    SEPARATELY = enum.auto()
    GROUP = enum.auto()


def read_data_items(
    file_name: str | Path,
    save_mode: SavedModeEnum,
) -> list[DataItem]:
    try:
        with open(file_name, encoding="utf-8") as f:
            obj = json.load(f)

            # Должен быть список, но если в файле будет что-то другое - это будет неправильно
            if not isinstance(obj, list):
                return []

            # Поддержка старого формата
            if save_mode == SavedModeEnum.SIMPLE or isinstance(obj[0], str):
                return [DataItem(value=x) for x in obj]

            return [DataItem.loads(x) for x in obj]

    except:
        return []


def write_data_items(
    file_name: str | Path,
    items: list[DataItem],
    save_mode: SavedModeEnum,
):
    with open(file_name, mode="w", encoding="utf-8") as f:
        if save_mode == SavedModeEnum.SIMPLE:
            result: list[str] = [x.value for x in items]
        else:
            result: list[dict[str, Any]] = [x.dumps() for x in items]

        json.dump(result, f, ensure_ascii=False, indent=4)


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
    file: str | Path = "log.txt",
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
            file, maxBytes=10_000_000, backupCount=5, encoding=encoding
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
    show_type: bool = False,
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
    send_telegram_notification(
        name=name,
        message=message,
        type="ERROR",
        has_delete_button=True,
        show_type=True,
    )


IS_CAN_SEND_ERROR_NOTIFICATIONS: bool = False
IS_SINGLE: bool = "--single" in sys.argv

DEFAULT_NEED_TO_STORE_ITEMS: int = 10_000
DEFAULT_SEND_NEW_ITEMS_MODE: SendNewItemsModeEnum = SendNewItemsModeEnum.GROUP


def log_uncaught_exceptions(ex_cls, ex, tb):
    # Если было запрошено прерывание
    if isinstance(ex, KeyboardInterrupt):
        sys.exit()

    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)

    # Посылаем уведомление только при запуске через задачу
    if IS_CAN_SEND_ERROR_NOTIFICATIONS:
        send_telegram_notification_error(name="root_common.py", message=text)

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
        timeout_for_when_empty_seconds: int = 60,  # 1 minute
        max_attempts_for_when_empty: int = 3,  # NOTE: Default after 3 minutes
        send_new_items_mode: SendNewItemsModeEnum = DEFAULT_SEND_NEW_ITEMS_MODE,
        send_new_item_diff: bool = False,
        timeout: TimeoutWait = DEFAULT_TIMEOUT_WAIT,
        timeout_exception_seconds: int = 5 * 60,  # 5 minutes
        formats: Formats = FORMATS_DEFAULT,
        save_mode: SavedModeEnum = SavedModeEnum.SIMPLE,
        url: str | None = None,
        callbacks: Callbacks | None = None,
        need_to_store_items: int | None = DEFAULT_NEED_TO_STORE_ITEMS,
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
        self.timeout_for_when_empty_seconds = timeout_for_when_empty_seconds
        self.max_attempts_for_when_empty = max_attempts_for_when_empty
        self.send_new_items_mode = send_new_items_mode
        self.send_new_item_diff = send_new_item_diff
        self.timeout = timeout
        self.timeout_exception_seconds = timeout_exception_seconds
        self.formats = formats
        self.save_mode = save_mode
        self.url = url
        self.callbacks = callbacks or self.Callbacks()
        self.need_to_store_items = need_to_store_items
        self.notify_after_sequence_of_errors = notify_after_sequence_of_errors
        self.report_errors_for_first_time_after_attempts = (
            report_errors_for_first_time_after_attempts
        )
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
        return read_data_items(
            file_name=self.file_name_items,
            save_mode=self.save_mode,
        )

    def save_items(self, items: list[DataItem], items_backup: list[DataItem] = None):
        write_data_items(
            file_name=self.file_name_items,
            items=items,
            save_mode=self.save_mode,
        )

        # Если элементы для бекапа переданы
        if items_backup:
            write_data_items(
                file_name=self.file_name_saved_backup,
                items=items_backup,
                save_mode=self.save_mode,
            )

    def _get_text_items(self, items: list[DataItem]) -> str:
        items: list[str] = [x.title for x in items]
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

        title_formatted: str = self.formats.process(self.log.name)

        has_sending_first_report_error: bool = False
        attempts: int = 0
        attempts_for_when_empty: int = 0

        if self.is_single:
            self.log.debug(self.formats.on_run_is_single)

        while True:
            try:
                self.log.debug(self.formats.on_start_check)

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
                current_items: list[DataItem] = self.read_items()

                text_current_items: str = self._get_text_items(current_items)
                self.log.debug(
                    self.formats.current_items, len(current_items), text_current_items
                )

                self.log.debug(self.formats.get_items)

                items: list[DataItem | str] = self.get_new_items(self)
                if not items and self.notify_when_empty:
                    attempts_for_when_empty += 1

                    if attempts_for_when_empty < self.max_attempts_for_when_empty:
                        self.log.debug(
                            self.formats.on_with_attempts,
                            attempts_for_when_empty,
                            self.formats.when_empty_items
                        )
                        self.log.debug(
                            self.formats.on_next_attempt_timeout,
                            self.timeout_for_when_empty_seconds,
                        )

                        # Wait <timeout_exception_seconds> before next attempt
                        time.sleep(self.timeout_for_when_empty_seconds)

                        continue

                    if self.need_notification:
                        self.log.info("An empty list was returned. Sending a notification")
                        self.send_telegram_notification_error(
                            name=title_formatted,
                            message=self.formats.when_empty_items,
                        )

                # Поддержка старого формата
                if items and isinstance(items[0], str):
                    items: list[DataItem] = [DataItem(value=x) for x in items]

                text_items: str = self._get_text_items(items)
                self.log.debug(self.formats.items, len(items), text_items)

                # Если текущих список пустой
                if not current_items:
                    self.save_items(items)
                else:
                    new_items: list[DataItem] = [
                        x for x in items if x not in current_items
                    ]
                    if new_items:
                        number_new_items: int = len(new_items)

                        # Если один элемент и стоит флаг на вывод разницы элементов
                        if number_new_items == 1 and self.send_new_item_diff:
                            current_item: str = (
                                current_items[0].title if current_items else ""
                            )
                            item: DataItem = new_items[0]
                            text: str = self.formats.new_item_diff % (
                                current_item,
                                item.title,
                            )
                            self.log.debug(text)

                            self.send_telegram_notification_from_item(
                                text=text,
                                item=item,
                            )

                        # Если один элемент или стоит флаг, разрешающий каждый элемент логировать отдельно
                        elif number_new_items == 1 or self.send_new_items_mode in (
                            SendNewItemsModeEnum.SEPARATELY,
                            SendNewItemsModeEnum.GROUP,
                        ):
                            if (
                                self.send_new_items_mode == SendNewItemsModeEnum.GROUP
                                and number_new_items > 1
                            ):
                                group: str | None = str(uuid.uuid4())
                                group_max_number: int | None = number_new_items
                            else:
                                group: str | None = None
                                group_max_number: int | None = None

                            for item in new_items:
                                text: str = self.formats.new_item % item.title
                                self.log.debug(text)

                                self.send_telegram_notification_from_item(
                                    text=text,
                                    item=item,
                                    group=group,
                                    group_max_number=group_max_number,
                                )

                        else:
                            # Новые элементы логируем все разом
                            text: str = self.formats.new_items % (
                                number_new_items,
                                "\n".join(x.title for x in new_items),
                            )
                            self.log.debug(text)

                            self.send_telegram_notification(
                                name=title_formatted,
                                message=text,
                                url=self.url,
                            )

                        # Если нужно определенное количество элементов хранить
                        if self.need_to_store_items:
                            items: list[DataItem] = list(current_items)
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

                # NOTE: Сброс счетчика попыток для пустого списка в рамках одного запуска
                attempts_for_when_empty: int = 0

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

                        self.send_telegram_notification_error(
                            name=title_formatted,
                            message=text,
                        )

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
                    self.need_notification
                    and self.notify_after_sequence_of_errors
                    and attempts >= self.report_errors_for_first_time_after_attempts
                ):
                    if not has_sending_first_report_error:
                        self.log.info("Sending a notification")

                        self.send_telegram_notification_error(
                            name=title_formatted,
                            message=str(e),
                        )
                        has_sending_first_report_error = True

                    elif attempts % self.report_errors_after_each_attempts == 0:
                        self.log.info("Sending a notification")

                        text = self.formats.on_with_attempts % (attempts, e)
                        self.send_telegram_notification_error(
                            name=title_formatted,
                            message=text,
                        )

                # Слишком много подряд неудачных попыток в режиме is_single
                if self.is_single and attempts >= self.max_attempts_for_is_single:
                    # Отключение отправки уведомления из log_uncaught_exceptions
                    # Т.к. выше уже будет отправлено уведомление об ошибке
                    IS_CAN_SEND_ERROR_NOTIFICATIONS = False

                    raise e

                self.log.debug(
                    self.formats.on_next_attempt_timeout,
                    self.timeout_exception_seconds,
                )

                # Wait <timeout_exception_seconds> before next attempt
                time.sleep(self.timeout_exception_seconds)

        self.log.debug(self.formats.on_finish)
        self.callbacks.on_finish(self)

    def send_telegram_notification(
        self,
        name: str,
        message: str,
        type: str = "INFO",
        url: str = None,
        has_delete_button: bool = False,
        show_type: bool = False,
        group: str = None,
        group_max_number: int = None,
        need_html_escape_content: bool = True,
    ):
        if not self.need_notification:
            return

        send_telegram_notification(
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

    def send_telegram_notification_error(self, name: str, message: str):
        self.send_telegram_notification(
            name=name,
            message=message,
            type="ERROR",
            has_delete_button=True,
            show_type=True,
        )

    def send_telegram_notification_from_item(
        self,
        text: str,
        item: DataItem,
        group: str | None = None,
        group_max_number: int | None = None,
    ):
        self.send_telegram_notification(
            name=item.process_notification_title(
                formats=self.formats,
                # NOTE: Тут нельзя использовать title_formatted,
                #       чтобы не было дублирования префиксов
                default=self.log.name,
            ),
            message=text,
            url=self.url or item.url,
            group=group,
            group_max_number=group_max_number,
            need_html_escape_content=item.need_html_escape_content,
        )


def get_yt_video_list(text_or_url: str, *args, **kwargs) -> list[DataItem]:
    return [
        DataItem(value=video.id, title=video.title, url=video.url)
        for video in search_youtube(text_or_url, *args, **kwargs)
        # NOTE: У видео с названием вида "[Deleted video]" duration_text = None
        if video.duration_text
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

            items.append(DataItem(value=title, url=video.url))

    return items


def get_items_from_rutube(
    _: NotificationJob,
    url: str,
    max_items: int | None = None,
) -> list[DataItem]:
    if "/plst/" in url:
        videos = get_videos_from_playlist_rutube(url, max_items=max_items)
    else:
        videos = get_videos_from_channel_rutube(url, max_items=max_items)

    return [
        DataItem(value=video.id, title=video.title, url=video.url) for video in videos
    ]


def run_notification_job(
    log__or__log_name: logging.Logger | str,
    script_dir: Path | str,
    get_new_items: Callable[["NotificationJob"], list[str | DataItem]],
    *,
    file_name_saved: str = FILE_NAME_SAVED,
    file_name_saved_backup: str = FILE_NAME_SAVED_BACKUP,
    need_notification: bool = True,
    notify_when_empty: bool = True,
    timeout_for_when_empty_seconds: int = 60,  # 1 minute
    max_attempts_for_when_empty: int = 3,  # NOTE: Default after 3 minutes
    send_new_items_mode: SendNewItemsModeEnum = DEFAULT_SEND_NEW_ITEMS_MODE,
    send_new_item_diff: bool = False,
    timeout: TimeoutWait = DEFAULT_TIMEOUT_WAIT,
    timeout_exception_seconds: int = 5 * 60,  # 5 minutes
    formats: Formats = FORMATS_DEFAULT,
    save_mode: SavedModeEnum = SavedModeEnum.SIMPLE,
    url: str | None = None,
    callbacks: NotificationJob.Callbacks | None = None,
    need_to_store_items: int | None = DEFAULT_NEED_TO_STORE_ITEMS,
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
        timeout_for_when_empty_seconds=timeout_for_when_empty_seconds,
        max_attempts_for_when_empty=max_attempts_for_when_empty,
        send_new_items_mode=send_new_items_mode,
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


def run_notification_job_rutube(
    name: str,
    script_dir: Path,
    url: str,
    many: bool = True,
    formats=FORMATS_VIDEO,
):
    title = f"{name} [Rutube]"

    max_items = callbacks = None
    if many:
        max_items = 100

        def on_first_start_detected(job: NotificationJob):
            job.log.debug("На первый запуск выполняется сохранение всех видео")

            items = get_items_from_rutube(job, url)
            job.save_items(items)

        callbacks = NotificationJob.Callbacks(
            on_first_start_detected=on_first_start_detected,
        )

    run_notification_job(
        title,
        script_dir,
        lambda job: get_items_from_rutube(job, url, max_items=max_items),
        formats=formats.replace(
            get_items=f"Запрос {max_items} видео",
        ),
        save_mode=SavedModeEnum.DATA_ITEM,
        callbacks=callbacks,
    )


if __name__ == "__main__":
    # TODO: В тесты

    item = DataItem(
        value="1s1e",
        title="1 season. 1 episode",
    )
    assert "MYSITE" == item.process_notification_title(
        formats=FORMATS_DEFAULT.replace(prefix=""),
        default="MYSITE",
    )
    assert "[#] MYSITE" == item.process_notification_title(
        formats=FORMATS_DEFAULT.replace(prefix="[#]"),
        default="MYSITE",
    )

    item = DataItem(
        value="1s1e",
        title="1 season. 1 episode",
        notification_title="OTHER_SITE",
    )
    assert "[#] OTHER_SITE" == item.process_notification_title(
        formats=FORMATS_DEFAULT.replace(prefix="[#]"),
        default="MYSITE",
    )

    item = DataItem(
        value="1s1e",
        title="1 season. 1 episode",
        notification_title="OTHER_SITE",
        prefix="@",
    )
    assert "@ OTHER_SITE" == item.process_notification_title(
        formats=FORMATS_DEFAULT.replace(prefix="[#]"),
        default="MYSITE",
    )

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
