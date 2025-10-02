#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup, Tag
from common import session


def get_seasons() -> dict[str, list[str]]:
    url = "https://ru.wikipedia.org/wiki/Пацаны_(телесериал)#Список_эпизодов"

    rs = session.get(url)
    rs.raise_for_status()

    soup = BeautifulSoup(rs.content, "html.parser")

    season_by_series: dict[str, list[str]] = dict()

    for season_title_el in soup.select('div:has(> h3[id *= "_сезон_"])'):
        season_title: str = season_title_el.h3.get_text(strip=True)

        table_series: Tag | None = season_title_el.find_next(
            "table", attrs={"class": "wikiepisodetable"}
        )
        if not table_series:
            continue

        series_list: list[str] = []
        for title_el in table_series.select("tr > td.summary > b"):
            # Удаление сносок, типа "«Финал четвёртого сезона»[b]«Убийственный забег»"
            if sup_el := title_el.find("sup"):
                sup_el.decompose()

            series_title: str = title_el.get_text(strip=True)
            series_list.append(series_title)

        season_by_series[season_title] = series_list

    assert season_by_series, "Не найден ни один сезон!"

    return season_by_series


def get_all_series() -> list[str]:
    return [
        f"{season}. {series}"
        for season, series_list in get_seasons().items()
        for series in series_list
    ]


if __name__ == "__main__":
    season_by_series: dict[str, list[str]] = get_seasons()
    for season, series_list in season_by_series.items():
        print(f"{season} ({len(series_list)}):")
        for series in series_list:
            print(f"    {series}")

        print()
    """
    1 сезон (2019) (8):
        Такая игра
        Вишенка
        Получи!
        Самка человека
        Полезно для души
        Невинные
        Общество самосохранения
        Ты меня нашёл
    
    2 сезон (2020) (8):
        Большая поездка
        Правильная подготовка и планирование
        За холмом тысячи людей с мечами
        Ничего подобного в мире нет
        Нам пора идти
        Прочь чёртовы двери
        Мясник, пекарь, свечник
        Что я знаю
    
    3 сезон (2022) (8):
        Расплата
        Единственный в небе
        Берег варваров
        Славная пятилетка
        Последний взор на сей мир лжи
        Героргазм
        Вот зажгу я пару свеч — ты в постельку можешь лечь
        До белого каления
    
    4 сезон (2024) (8):
        Отдел грязных трюков
        Жизнь среди заразы
        Вейся, красный наш флаг
        Мудрость пожилых
        Остерегайся бармаглота, сын мой
        Грязный бизнес
        Инсайдер
        Финал четвёртого сезона»«Убийственный забег
    """

    print("\n" + "-" * 10 + "\n")

    all_series: list[str] = get_all_series()
    print(f"All series ({len(all_series)}): {all_series}")
    """
    All series (32): ['1 сезон (2019). Такая игра', '1 сезон (2019). Вишенка', '1 сезон (2019). Получи!', '1 сезон (2019). Самка человека', '1 сезон (2019). Полезно для души', '1 сезон (2019). Невинные', '1 сезон (2019). Общество самосохранения', '1 сезон (2019). Ты меня нашёл', '2 сезон (2020). Большая поездка', '2 сезон (2020). Правильная подготовка и планирование', '2 сезон (2020). За холмом тысячи людей с мечами', '2 сезон (2020). Ничего подобного в мире нет', '2 сезон (2020). Нам пора идти', '2 сезон (2020). Прочь чёртовы двери', '2 сезон (2020). Мясник, пекарь, свечник', '2 сезон (2020). Что я знаю', '3 сезон (2022). Расплата', '3 сезон (2022). Единственный в небе', '3 сезон (2022). Берег варваров', '3 сезон (2022). Славная пятилетка', '3 сезон (2022). Последний взор на сей мир лжи', '3 сезон (2022). Героргазм', '3 сезон (2022). Вот зажгу я пару свеч — ты в постельку можешь лечь', '3 сезон (2022). До белого каления', '4 сезон (2024). Отдел грязных трюков', '4 сезон (2024). Жизнь среди заразы', '4 сезон (2024). Вейся, красный наш флаг', '4 сезон (2024). Мудрость пожилых', '4 сезон (2024). Остерегайся бармаглота, сын мой', '4 сезон (2024). Грязный бизнес', '4 сезон (2024). Инсайдер', '4 сезон (2024). Финал четвёртого сезона»«Убийственный забег']
    """
