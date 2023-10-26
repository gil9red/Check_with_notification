#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для примера режима is_single.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job


run_notification_job(
    "Тест",
    DIR,
    lambda _: ["1", "2", "3"],
    is_single=True,
    need_notification=False,
)
