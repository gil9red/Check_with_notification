#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых книг Зыкова.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_BOOK
from root_common import NotificationJob, run_notification_job
from third_party.litres_ru.get_books_by_author import get_books


URL = "https://www.litres.ru/author/vitaliy-zykov/"


def get_items(_: NotificationJob) -> list[str]:
    return [book.get_full_name() for book in get_books(URL)]


run_notification_job(
    "Новые книги Виталия Зыкова",
    DIR,
    get_items,
    formats=FORMATS_BOOK,
    url=URL,
)
