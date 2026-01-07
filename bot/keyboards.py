"""
Inline-клавиатуры Telegram-бота для создания открыток.

Содержит набор функций для формирования клавиатур:
- выбора фона
- выбора режима текста
- выбора повода
- навигации по текстам и изображениям
"""
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def select_image_first():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Выбрать', callback_data='select'), InlineKeyboardButton(text='Следующая', callback_data='next'))
    return kb.as_markup()


def select_image():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Назад', callback_data='back'), InlineKeyboardButton(text='Выбрать', callback_data='select') ,InlineKeyboardButton(text='Следующая', callback_data='next'))
    return kb.as_markup()


def select_resp_for_text():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Да', callback_data='bot_text'), InlineKeyboardButton(text='Нет', callback_data='not_select_text'))
    kb.row(InlineKeyboardButton(text='Вставить свой', callback_data='user_text'))
    return kb.as_markup()

def select_occasion():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='С новым годом!', callback_data='new_year'))
    kb.row(InlineKeyboardButton(text='С наступающим!', callback_data='coming'))
    kb.row(InlineKeyboardButton(text='С Рождеством', callback_data='christmas'))
    kb.row(InlineKeyboardButton(text='Со Старым Новым годом', callback_data='old_new_year'))
    return kb.as_markup()

def continue_select_image():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Продолжить создание открыток', callback_data='continue'))
    kb.row(InlineKeyboardButton(text='Продолжить в следующий раз', callback_data='stop'))
    return kb.as_markup()

def start_selector():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Продолжить создание открыток', callback_data='continue'))
    return kb.as_markup()


def select_text_first():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Выбрать', callback_data='select_text'),
           InlineKeyboardButton(text='Следующий', callback_data='next_text'))
    return kb.as_markup()


def select_text():
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text='Назад', callback_data='back_text'), InlineKeyboardButton(text='Выбрать', callback_data='select_text') ,InlineKeyboardButton(text='Следующая', callback_data='next_text'))
    return kb.as_markup()