#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео TVG (Time Video Game).

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    run_notification_job,
    SavedModeEnum,
    get_video_list_from_playlists,
)


PLAYLISTS = [
    ("Психоанализ героев видеоигр", "PLfCe0Mzdeup0kYxejFl8Vjw6DtZCmuR-Z"),
    ("ТОПы", "PLfCe0Mzdeup3T-JaqrSvUhmVPNpVotU5L"),
    ("Расцвет и Упадок", "PLfCe0Mzdeup2GUW_1lH0q-_rRmxubo8c5"),
]


run_notification_job(
    "TVG",
    DIR,
    lambda job: get_video_list_from_playlists(job, PLAYLISTS),
    save_mode=SavedModeEnum.DATA_ITEM,
    # Чтобы не было "каши", т.к. видео собирается из нескольких плейлистов
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
