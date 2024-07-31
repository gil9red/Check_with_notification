#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео Аля иногда кокетничает со мной по-русски в Rutube.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT_DIR = DIR.parent

sys.path.append(str(ROOT_DIR))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import SavedModeEnum, run_notification_job, get_items_from_rutube


URL = "https://rutube.ru/plst/423679/"


run_notification_job(
    "Аля иногда кокетничает со мной по-русски [Rutube]",
    DIR,
    lambda job: get_items_from_rutube(job, URL),
    formats=FORMATS_VIDEO,
    save_mode=SavedModeEnum.DATA_ITEM,
)
