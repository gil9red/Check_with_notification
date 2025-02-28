#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео плейлиста Fantom АНАЛОГОВЫЕ и ЦИФРОВЫЕ ХОРРОРЫ.

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    SavedModeEnum,
    get_yt_playlist_video_list,
    run_notification_job,
)


run_notification_job(
    "АНАЛОГОВЫЕ и ЦИФРОВЫЕ ХОРРОРЫ [Fantom]",
    DIR,
    lambda _: get_yt_playlist_video_list("PLqZA9icnp9qffDCuClNUL2AExxEbLBtzs"),
    save_mode=SavedModeEnum.DATA_ITEM,
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
