#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для уведомления о появлении новых главах Berserk.

"""


import time
import traceback
import sys

from typing import List
from pathlib import Path

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent))  # Путь к папке выше

from root_common import run_notification_job


def get_chapters() -> List[str]:
    URL = 'https://risens.team/title/28/berserk-manga/4333'

    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)
    try:
        driver.get(URL)
        print(f'Title: {driver.title!r}')

        time.sleep(5)

        driver.find_element_by_id('vs2__combobox').click()
        return [x.text for x in driver.find_elements_by_css_selector('ul#vs2__listbox > li')]

    except:
        # TODO: не ловить исключение, пусть его обрабатывает run_notification_job
        print(traceback.format_exc())

    finally:
        driver.quit()

    return []


run_notification_job(
    'Манга Berserk',
    DIR,
    get_chapters,
    notified_by_sms=True,
    timeout={'days': 1},
    format_current_items='Текущий список глав (%s): %s',
    format_get_items='Запрос глав',
    format_items='Список глав (%s): %s',
    format_new_item='Новая глава "%s"',
    format_no_new_items='Изменений нет',
)
