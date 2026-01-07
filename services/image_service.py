from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"


def get_user_images(user_id: int) -> list[Path]:
    """
    Возвращает список готовых открыток пользователя.
    """
    user_dir = OUTPUT_DIR / str(user_id)

    if not user_dir.exists():
        return []

    return sorted(user_dir.glob("*.png"))