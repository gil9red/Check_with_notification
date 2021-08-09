#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых видео Рик и Морти.

"""


import sys

from pathlib import Path
from typing import List

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from format import FORMAT_VIDEO
from root_common import run_notification_job
from third_party.rik_i_morti_online import get_season_by_series


def get_video_list() -> List[str]:
    items = []
    for video_list in get_season_by_series().values():
        items += video_list

    return items


run_notification_job(
    'Рик и Морти',
    DIR,
    get_video_list,
    format=FORMAT_VIDEO,
)
