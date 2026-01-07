"""
FSM-состояния бота для создания открыток.

Описывает этапы взаимодействия с пользователем:
- выбор фона
- выбор текста
- ввод пользовательского текста
- предпросмотр результата
"""
from aiogram.fsm.state import State, StatesGroup

class StateImage(StatesGroup):
    index_image = State()
    occasion = State()
    text = State()
    index_preview = State()
