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
from root_common import run_notification_job
from third_party.vitaly_zykov_ru_knigi__get_books import get_books


run_notification_job(
    "Новые книги Виталия Зыкова",
    DIR,
    lambda _: get_books(),
    formats=FORMATS_BOOK,
)
