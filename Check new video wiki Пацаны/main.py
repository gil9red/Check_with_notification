#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "Пацаны".

"""


import sys

from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(DIR.parent))  # Путь к папке выше
sys.path.append(str(ROOT_DIR / "third_party" / "wikipedia"))

from formats import FORMATS_VIDEO
from root_common import run_notification_job
from third_party.wikipedia.ru_wikipedia_org__wiki__Пацаны_телесериал_Список_эпизодов import get_all_series


run_notification_job(
    "Пацаны",
    DIR,
    lambda _: get_all_series(),
    formats=FORMATS_VIDEO,
)
