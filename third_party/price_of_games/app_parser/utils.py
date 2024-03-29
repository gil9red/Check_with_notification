#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import re
from logging import Logger
from typing import List, Tuple, Union, Optional

from bs4 import BeautifulSoup
import requests

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'

# Думаю, это станет дополнительной гарантией получения русскоязычной версии сайта
session.headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'


def steam_search_game_price_list(name: str, log_common: Logger = None) -> List[Tuple[str, Union[float, int]]]:
    """
    Функция принимает название игры, после ищет его в стиме и возвращает результат как список
    кортежей из (название игры, цена).

    """

    log_common and log_common.debug(f'Поиск в стиме "{name}"')

    # Дополнения с категорией Game не ищутся, например: "Pillars of Eternity: The White March Part I", поэтому url
    # был упрощен для поиска всего
    url = "https://store.steampowered.com/search/"

    # Из цикла не выйти, пока не получится скачать и распарсить страницу
    while True:
        try:
            rs = session.get(url, params=dict(term=name, ndl=1))
            root = BeautifulSoup(rs.content, "html.parser")
            break

        except Exception:
            log_common and log_common.exception('При поиске в стиме что-то пошло не так:')

            # Если произошла какая-то ошибка попытаемся через 5 минут попробовать снова
            time.sleep(5 * 60)

    game_price_list = []

    for div in root.select(".search_result_row"):
        name = div.select_one(".title").text.strip()

        # Ищем тег скидки, чтобы вытащить оригинальную цену, а не ту, что получилась со скидкой
        price_el = div.select_one(".discount_original_price") or div.select_one(".discount_final_price")

        # Если цены нет (например, игра еще не продается)
        if not price_el:
            price = None
        else:
            price = price_el.get_text(strip=True)

            # Если в цене нет цифры считаем, что это "Free To Play" или что-то подобное
            m = re.search(r"\d", price)
            if not m:
                price = 0
            else:
                # Только значение цены
                if "pуб" not in price and "руб" not in price:
                    log_common and log_common.warning(
                        f'АХТУНГ! Неизвестный формат цены: "{price}".'
                    )

                price = price.replace(" pуб.", "").strip()

                # "799,99" -> "799.99"
                price = price.replace(",", ".")

            if isinstance(price, str):
                price = re.sub(r"[^\d.]", "", price)
                price = int(float(price))  # Всегда храним как целые числа

        game_price_list.append((name, price))

    log_common and log_common.debug(f'game_price_list ({len(game_price_list)}): {game_price_list}')

    time.sleep(0.5)

    return game_price_list


def smart_comparing_names(name_1: str, name_2: str) -> bool:
    """
    Функция для сравнивания двух названий игр.
    Возвращает True, если совпадают, иначе -- False.
    """

    # Приведение строк к одному регистру
    name_1 = name_1.lower()
    name_2 = name_2.lower()

    def remove_postfix(text: str) -> str:
        for postfix in ('dlc', 'expansion'):
            if text.endswith(postfix):
                return text[:-len(postfix)]
        return text

    # Удаление символов кроме буквенных, цифр и _: "the witcher®3:___ вася! wild hunt" -> "thewitcher3___васяwildhunt"
    def clear_name(name: str) -> str:
        return re.sub(r'\W', '', name)

    name_1 = clear_name(name_1)
    name_1 = remove_postfix(name_1)

    name_2 = clear_name(name_2)
    name_2 = remove_postfix(name_2)

    return name_1 == name_2


def get_price(game_name: str, log_common: Logger = None, log_append_game: Logger = None) -> Optional[Union[int, float]]:
    def _on_found_price(game_name: str, name_from_site: str, price: Union[int, float]):
        log_common and log_common.info(f'Нашли игру: {game_name!r} ({name_from_site}) -> {price}')
        log_append_game and log_append_game.info(f'Нашли игру: {game_name!r} ({name_from_site}) -> {price}')

    # Поищем игру и ее цену в стиме
    game_price_list = steam_search_game_price_list(game_name, log_common)

    # Сначала пытаемся найти игру по полному совпадению
    for name, price in game_price_list:
        if game_name == name:
            _on_found_price(game_name, name, price)
            return price

    # Если по полному совпадению на нашли, пытаемся найти предварительно очищая названия игр от лишних символов
    for name, price in game_price_list:
        # Если нашли игру, запоминаем цену и прерываем сравнение с другими найденными играми
        if smart_comparing_names(game_name, name):
            _on_found_price(game_name, name, price)
            return price

    return


if __name__ == '__main__':
    game_name = 'JUMP FORCE'
    print(steam_search_game_price_list(game_name))
    print(get_price(game_name))

    print()

    game_name = 'Alone in the Dark: Illumination'
    print(steam_search_game_price_list(game_name))
    print(get_price(game_name))
