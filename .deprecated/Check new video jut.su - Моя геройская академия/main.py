#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых серий аниме "Моя геройская академия".

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import run_notification_job, get_items_from_jut_su


URL = "https://jut.su/boku-hero-academia/"


run_notification_job(
    "Моя геройская академия",
    DIR,
    lambda job: get_items_from_jut_su(job, URL),
    formats=FORMATS_VIDEO,
)
