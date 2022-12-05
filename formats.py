#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from dataclasses import dataclass


@dataclass
class Formats:
    on_start: str = 'Запуск'
    on_start_check: str = 'Запуск проверки'
    on_finish_check: str = 'Завершение проверки\n'
    first_start_detected: str = 'Обнаружен первый запуск'
    current_items: str = 'Текущий список (%s): %s'
    get_items: str = 'Запрос списка'
    items: str = 'Список (%s): %s'
    new_item: str = 'Появился новый элемент "%s"'
    new_items: str = 'Появились новые элементы (%s):\n%s'
    new_item_diff: str = 'Изменение "%s" -> "%s"'
    no_new_items: str = 'Новых элементов нет'
    when_empty_items: str = 'Вернулся пустой список!'
    file_skip_exists: str = 'Обнаружен файл "%s", пропускаю проверку.'
    on_exception: str = 'Ошибка:'
    on_exception_next_attempt: str = 'Через 5 минут попробую снова...'
    on_finish: str = 'Завершение'
    postfix: str = ''

    def process(self, text: str) -> str:
        if self.postfix:
            text = f'{text} {self.postfix}'
        return text


FORMATS_DEFAULT = Formats()
FORMATS_VIDEO = Formats(
    current_items='Текущий список видео (%s): %s',
    get_items='Запрос видео',
    items='Список видео (%s): %s',
    new_item='Новое видео "%s"',
    new_items='Появились новые видео (%s):\n%s',
    no_new_items='Изменений нет',
    postfix=' 📺',
)
FORMATS_GAME = Formats(
    current_items='Текущий список игр (%s): %s',
    get_items='Запрос списка игр',
    items='Список игр (%s): %s',
    new_item='Появилась новая игра "%s"',
    new_items='Появились новые игры (%s):\n%s',
    no_new_items='Новых игр нет',
    postfix=' 🎮',
)
FORMATS_SEASON = Formats(
    current_items='Текущий список сезонов (%s): %s',
    get_items='Запрос сезонов',
    items='Список сезонов (%s): %s',
    new_item='Новый сезон "%s"',
    new_items='Появились новые сезоны (%s):\n%s',
    no_new_items='Изменений нет',
    postfix=' 🔢',
)
FORMATS_CHAPTER = Formats(
    current_items='Текущий список глав (%s): %s',
    get_items='Запрос списка глав',
    items='Список глав (%s): %s',
    new_item='Новая глава: "%s"',
    new_items='Появились новые главы (%s):\n%s',
    no_new_items='Новых глав нет',
    postfix=' 📖',
)
FORMATS_BOOK = Formats(
    current_items='Текущий список книг (%s): %s',
    get_items='Запрос списка книг',
    items='Список книг (%s): %s',
    new_item='Появилась новая книга: "%s"',
    new_items='Появились новые книги (%s):\n%s',
    no_new_items='Новых книг нет',
    postfix=' 📚',
)
FORMATS_MANGA = Formats(
    current_items='Текущий список манги (%s): %s',
    get_items='Запрос манги',
    items='Список манги (%s): %s',
    new_item='Новая манга "%s"',
    new_items='Появились новые манги (%s):\n%s',
    no_new_items='Изменений нет',
    postfix=' 📚',
)
