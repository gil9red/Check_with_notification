#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для уведомления о появлении новых видео "Разбор спидрана".

"""


import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from formats import FORMATS_VIDEO
from root_common import (
    run_notification_job,
    SavedModeEnum,
    get_playlist_video_list_v2 as get_playlist_video_list,
)


run_notification_job(
    "Разбор спидрана! [Naritsa]",
    DIR,
    lambda _: get_playlist_video_list("PLgHXSvDpcJQiG_H7HTpAEhUP6JbOEbg3Q"),
    save_mode=SavedModeEnum.DATA_ITEM,
    send_new_items_separately=True,
    formats=FORMATS_VIDEO,
)
