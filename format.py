#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import NamedTuple


class Format(NamedTuple):
    on_start: str = 'Запуск'
    on_start_check: str = 'Запуск проверки'
    on_finish_check: str = 'Завершение проверки\n'
    first_start_detected: str = 'Обнаружен первый запуск'
    current_items: str = 'Текущий список (%s): %s'
    get_items: str = 'Запрос списка'
    items: str = 'Список (%s): %s'
    new_item: str = 'Появился новый элемент "%s"'
    no_new_items: str = 'Новых элементов нет'
    when_empty_items: str = 'Вернулся пустой список!'
    file_skip_exists: str = 'Обнаружен файл "%s", пропускаю проверку.'
    on_exception: str = 'Ошибка:'
    on_exception_next_attempt: str = 'Через 5 минут попробую снова...'


FORMAT_DEFAULT = Format()
FORMAT_VIDEO = Format(
    current_items='Текущий список видео (%s): %s',
    get_items='Запрос видео',
    items='Список видео (%s): %s',
    new_item='Новое видео "%s"',
    no_new_items='Изменений нет',
)
FORMAT_GAME = Format(
    current_items='Текущий список игр (%s): %s',
    get_items='Запрос списка игр',
    items='Список игр (%s): %s',
    new_item='Появилась новая игра "%s"',
    no_new_items='Новых игр нет',
)
FORMAT_SEASON = Format(
    current_items='Текущий список сезонов (%s): %s',
    get_items='Запрос сезонов',
    items='Список сезонов (%s): %s',
    new_item='Новый сезон "%s"',
    no_new_items='Изменений нет',
)
FORMAT_CHAPTER = Format(
    current_items='Текущий список глав (%s): %s',
    get_items='Запрос списка глав',
    items='Список глав (%s): %s',
    new_item='Лунный скульптор: "%s"',
    no_new_items='Новых глав нет',
)
FORMAT_BOOK = Format(
    current_items='Текущий список книг (%s): %s',
    get_items='Запрос списка книг',
    items='Список книг (%s): %s',
    new_item='Появилась новая книга: "%s"',
    no_new_items='Новых книг нет',
)