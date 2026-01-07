"""
Ключи данных, используемые в FSMContext.

Служит для унификации доступа к данным FSM
и предотвращения опечаток в ключах.
"""
from typing import TypedDict

class CardFSMData(TypedDict):
    prev: int
    image: int
    occasion: str
    text_role: str
    text_index: int
    texts:list[str]
    user_text: str
    prompt_message_id: int