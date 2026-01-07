from pydantic_settings import BaseSettings, SettingsConfigDict
"""
Конфигурация проекта.

Содержит пути, списки изображений, словари поводов
и другие константы, используемые в боте.
"""

from pathlib import Path


# для указания пути к .env. без этого конфиг не работал/ тфк же если .env находится в той же папке что и config  то прописываем путь Path(__file__).resolve().parent если config глубже env то прописываем Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parent # .../PythonProject1
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):

    BOT: str
    model_config = SettingsConfigDict(env_file=str(ENV_FILE),
                                      env_file_encoding="utf-8")

settings = Settings()

OUTPUT_DIR = BASE_DIR / "output"
IMAGES_DIR = BASE_DIR / "assets" / "previews"


image_files = [
    p for p in IMAGES_DIR.iterdir()
    if p.suffix.lower() in (".jpg", ".jpeg", ".png")
]

# словарь для файла хендлерс. с темами для текста открыток. словарь содержит ключ - колбак от кнопки выбора повода и значение словарь заголовок поздравления и имя файла с текстом под нужный повод
OCCASIONS = {
        "coming": {
            "title": "С наступающим Новым годом!",
            "file": "coming",
        },
        "new_year": {
            "title": "С Новым годом!",
            "file": "new_year",
        },
        "christmas": {
            "title": "С Рождеством!",
            "file": "christmas",
        },
        "old_new_year": {
            "title": "Со Старым Новым годом!",
            "file": "old_new_year",
        },
    }
