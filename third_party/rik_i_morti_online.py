#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
from typing import Dict, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


def get_season_by_series() -> Dict[str, List[str]]:
    url = 'https://rick-i-morty.online/'

    s = requests.session()
    rs = s.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    season_by_series = dict()

    for season in root.select('#dz-seasons > .seasons'):
        title = season.select_one('h3').get_text(strip=True)
        href = season.select_one('a')['href']
        season_url = urljoin(rs.url, href)

        rs_season = s.get(season_url)
        root = BeautifulSoup(rs_season.content, 'html.parser')

        series = []
        for x in root.select('.episodios > li'):
            series_num = x.select_one('.serie').get_text(strip=True)
            series_title = x.select_one('.episodiotitle > a').get_text(strip=True)
            series.append(f'{series_num}: {series_title}')

        season_by_series[title] = series

        # Не нужно напрягать сайт
        time.sleep(1)

    return season_by_series


if __name__ == '__main__':
    season_by_series = get_season_by_series()
    print('Total seasons:', len(season_by_series))
    print('Total episodes:', sum(map(len, season_by_series.values())))
    # Total seasons: 5
    # Total episodes: 50

    print(season_by_series)
    # {'5 Сезон': ['5 сезон спецвыпуск: Спецвыпуск', '5 сезон 1 серия: Морт Ужин с Рикандре', '5 сезон 2 серия: Смертность', '5 сезон 3 серия: Удобная смерть для Рика', '5 сезон 4 серия: Спрей Рикзависимости', '5 сезон 5 серия: Амортикан Грикфитти', '5 сезон 6 серия: Дед Благодарения', '5 сезон 7 серия: Риквангелион готрового джеррисхождения', '5 сезон 8 серия: Риктернальное сияние дружбы чистого Морта'], '4 Сезон': ['4 сезон 1 серия: Кристаллы смерти', '4 сезон 2 серия: Старик и сиденье', '4 сезон 3 серия: Пролетая над гнездом Морти', '4 сезон 4 серия: Клоунада и беспорядок: Специальный Риковый Морти', '4 сезон 5 серия: Рикрейсер Риклактика', '4 сезон 6 серия: Бесриконечный Морти', '4 сезон 7 серия: Промортиус', '4 сезон 8 серия: Эпизод с чаном кислоты', '4 сезон 9 серия: Чайлдрик Морт', '4 сезон 10 серия: Звездный Морт: Риквращение Джерри'], '3 Сезон': ['3 сезон 1 серия: Побег из Рикшенка', '3 сезон 2 серия: Рикман с камнем', '3 сезон 3 серия: Огурчик Рик', '3 сезон 4 серия: Заступники 3: Возвращение Губителя Миров', '3 сезон 5 серия: Запутанный грязный заговор', '3 сезон 6 серия: Отдых и Риклаксация', '3 сезон 7 серия: Риклантидическая путаница', '3 сезон 8 серия: Проветренный мозг Морти', '3 сезон 9 серия: Азбука Бет', '3 сезон 10 серия: Рикчжурский Мортидат'], '2 Сезон': ['2 сезон 1 серия: Рик во времени', '2 сезон 2 серия: Успеть до Мортиночи', '2 сезон 3 серия: Аутоэротическая ассимиляция', '2 сезон 4 серия: Вспомрикнуть всё', '2 сезон 5 серия: Пора швифтануться', '2 сезон 6 серия: Рики, наверное, сошли с ума', '2 сезон 7 серия: Большой переполох в маленьком Санчезе', '2 сезон 8 серия: Межпространственный кабель 2: Искушение судьбы', '2 сезон 9 серия: Посмотрите кто сейчас зачищает', '2 сезон 10 серия: Свадебные сквончеры'], '1 Сезон': ['1 сезон 1 серия: Пилотный эпизод', '1 сезон 2 серия: Пёс-газонокосильщик', '1 сезон 3 серия: Анатомический парк', '1 сезон 4 серия: М. Найт Шьямал-Инопланетяне!', '1 сезон 5 серия: Мисикс и разрушение', '1 сезон 6 серия: Вакцина Рика #9', '1 сезон 7 серия: Взрослеющий газорпазорп', '1 сезон 8 серия: Рикдцать минут', '1 сезон 9 серия: Надвигается нечто риканутое', '1 сезон 10 серия: Поймать рикоразновидности рода Рика', '1 сезон 11 серия: Риксованное дело']}
