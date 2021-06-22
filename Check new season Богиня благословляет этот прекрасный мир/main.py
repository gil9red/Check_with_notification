#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых сезонов аниме "Богиня благословляет этот прекрасный мир".

"""


import re
import sys

from typing import List
from pathlib import Path

import requests

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from format import FORMAT_SEASON
from root_common import run_notification_job


def get_items() -> List[str]:
    rs = requests.get('https://en.wikipedia.org/wiki/List_of_KonoSuba_episodes')
    items = re.findall(r'Season \w+', rs.text)
    return sorted(set(items))


run_notification_job(
    'Богиня благословляет этот прекрасный мир',
    DIR,
    get_items,
    format=FORMAT_SEASON,
)
