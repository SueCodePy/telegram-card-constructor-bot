from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"


def get_user_dir(user_id: int) -> Path:
    """
    Возвращает папку пользователя.
    Создаёт, если её нет.
    """
    user_dir = OUTPUT_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


def clear_user_dir(user_id: int) -> Path:
    """
    Полностью очищает папку пользователя
    и создаёт её заново.
    """
    user_dir = OUTPUT_DIR / str(user_id)

    if user_dir.exists():
        shutil.rmtree(user_dir)

    user_dir.mkdir(parents=True)
    return user_dir


def remove_user_dir(user_id: int):
    """
    Полностью удаляет папку пользователя
    (когда всё завершено).
    """
    user_dir = OUTPUT_DIR / str(user_id)
    if user_dir.exists():
        shutil.rmtree(user_dir)
