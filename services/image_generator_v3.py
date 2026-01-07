"""
Модуль генерации изображений открыток с использованием Pillow.

Назначение:
- Наложение заголовка и текста на фоновые изображения
- Автоматический подбор размера шрифта
- Центрирование текста
- Поддержка различных цветовых стилей
- Сохранение результата в пользовательскую директорию

Модуль используется Telegram-ботом для генерации поздравительных открыток.
Часть логики подбора шрифтов и работы с Pillow была разработана
с использованием AI-ассистента, затем адаптирована, протестирована
и интегрирована в проект вручную.

Основные особенности:
- Адаптация текста под размеры изображения
- Поддержка 1–2 строк заголовка
- Автоматический перенос текста
- Центрирование текстового блока по вертикали
- Работа с RGBA (поддержка обводки текста)

Точка входа для бота:
    pic_creator(...)
"""


from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from services.file_storage import get_user_dir

# ===== PATHS =====
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"
IMAGES = ASSETS / "images"
FONTS = ASSETS / "fonts"
OUTPUT = BASE_DIR / "output"
OUTPUT.mkdir(exist_ok=True)


# ===== FONTS =====
FONT_TITLE = FONTS / "Montserrat-Bold.ttf"
FONT_TEXT = FONTS / "Montserrat-Bold.ttf"


# ===== STYLES =====
STYLES = {
    "blue_bright_white": {
        "fill": (9, 52, 190, 255),
        "stroke": (235, 235, 198, 255),
        "stroke_width": 10,
    },
    "fuchsia_white": {
        "fill": (190, 7, 90, 255),
        "stroke": (245, 245, 245, 150),
        "stroke_width": 10,
    },
    "white": {
        "fill": (255, 255, 255, 255),
        "stroke": (0, 0, 0, 160),
        "stroke_width": 10,
    },
    "santa_red": {
        "fill": (200, 20, 20, 255),
        "stroke": (255, 255, 255, 255),
        "stroke_width": 10,
    },
    "gold": {
        "fill": (229, 152, 35, 255),
        "stroke": (255, 255, 255, 200),
        "stroke_width": 10,
    },
    "red_big": {
        "fill": (180, 0, 0, 255),
        "stroke": (255, 255, 255, 200),
        "stroke_width": 8,
    },
    "silver_white": {
        "fill": (110, 39, 0, 255),
        "stroke": (245, 235,119, 180),
        "stroke_width": 10,
},
}


# ===== HELPERS =====
def wrap_text(text, draw, font, max_width):
    """
    Разбивает текст на строки так, чтобы каждая строка
    умещалась в заданную максимальную ширину.
    Используется для основного текста открытки.
    """

    words = text.split()
    lines, current = [], ""

    for word in words:
        test = f"{current} {word}".strip()
        w = draw.textbbox((0, 0), test, font=font)[2]
        if w <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)
    return lines


def split_title_two_lines(title, draw, font, max_width):
    """
    Пытается разделить заголовок на 1–2 строки,
    если это позволяет ширина изображения.
    Короткие заголовки оставляет в одну строку.
    """
    words = title.split()

    # ✅ Короткие заголовки всегда в одну строку
    if len(words) <= 3:
        return [title]

    for i in range(1, len(words)):
        l1 = " ".join(words[:i])
        l2 = " ".join(words[i:])

        if (
            draw.textbbox((0, 0), l1, font=font)[2] <= max_width
            and draw.textbbox((0, 0), l2, font=font)[2] <= max_width
        ):
            return [l1, l2]

    return [title]


def fit_title_font(
    title: str,
    draw: ImageDraw.ImageDraw,
    font_path: Path,
    max_width: int,
    start_size: int,
    min_size: int = 40,
) -> tuple[ImageFont.ImageFont, list[str]]:
    """
    Подбирает размер шрифта заголовка таким образом,
    чтобы текст уместился максимум в две строки
    и не выходил за пределы изображения по ширине.
    """
    size = start_size

    while size >= min_size:
        font = ImageFont.truetype(font_path, size=size)
        lines = split_title_two_lines(title, draw, font, max_width)

        # если получилось 1 или 2 строки и каждая влезает — ок
        if len(lines) <= 2:
            fits = True
            for line in lines:
                w = draw.textbbox((0, 0), line, font=font)[2]
                if w > max_width:
                    fits = False
                    break

            if fits:
                return font, lines

        size -= 4  # уменьшаем шрифт

    # fallback
    font = ImageFont.truetype(font_path, size=min_size)
    return font, [title]


# ===== MAIN GENERATOR =====
def generate_card(
    user_id: int,
    background: Path,
    title: str,
    message: str | None,
    style_id: str = "santa_red"
) -> Path:
    """
    Основная функция генерации открытки.

    Параметры:
    - user_id: идентификатор пользователя
    - background: путь к фоновому изображению
    - title: заголовок открытки
    - message: основной текст (может быть None)
    - style_id: идентификатор цветового стиля

    Функция:
    - открывает фон
    - подбирает размеры шрифтов
    - размещает заголовок и текст
    - сохраняет результат в пользовательскую директорию

    Возвращает путь к сохранённому изображению.
    """

    img = Image.open(background).convert("RGBA")
    w, h = img.size
    draw = ImageDraw.Draw(img)
    if w < h:
        max_width = int(w * 0.8)
    else:
        max_width = int(w * 0.55)

    title_font, title_lines = fit_title_font(
        title=title,
        draw=draw,
        font_path=FONT_TITLE,
        max_width=max_width,
        start_size=int(h * 0.14),
    )

    text_font_size = int(title_font.size * 0.7)
    text_font = ImageFont.truetype(FONT_TEXT, size=text_font_size)

    message_lines = wrap_text(message, draw, text_font, max_width) if message else []

    title_height = len(title_lines) * (title_font.size + 10)
    message_height = len(message_lines) * (text_font.size + 6)
    block_height = title_height + message_height + (20 if message_lines else 0)

    y = int((h - block_height) / 2)

    style = STYLES[style_id]

    # --- DRAW TITLE ---
    for line in title_lines:
        tw = draw.textbbox((0, 0), line, font=title_font)[2]
        x = (w - tw) // 2
        draw.text(
            (x, y),
            line,
            font=title_font,
            fill=style["fill"],
            stroke_width=style["stroke_width"],
            stroke_fill=style["stroke"],
        )
        y += title_font.size+10

    y += 20

    # --- DRAW MESSAGE ---
    for line in message_lines:
        tw = draw.textbbox((0, 0), line, font=text_font)[2]
        x = (w - tw) // 2
        draw.text(
            (x, y),
            line,
            font=text_font,
            fill=style["fill"],
            stroke_width=max(1, style["stroke_width"] - 2)+1,
            stroke_fill=style["stroke"],
        )
        y += text_font.size + 6
    user_dir = get_user_dir(user_id)
    output_path = user_dir / f"{background.stem}_{style_id}.png"
    img.save(output_path)

    return output_path


# ===== LOCAL TEST =====
def pic_creator(fon, title, message, user_id):
    """
    Вспомогательная функция-обёртка.

    Используется ботом для генерации серии открыток
    в разных стилях на основе одного фона и текста.
    """

    for stile in STYLES:
            generate_card(
                user_id=user_id,
                background=fon,
                title=title,
                message=message,
                style_id=stile)
    return

'''"black": {
        "fill": (20, 20, 20, 255),
        "stroke": (255, 255, 255, 180),
        "stroke_width": 3,
    },
     "gold_gray": {
        "fill": (185, 150, 45, 255),     # тёмное золото
        "stroke": (90, 90, 90, 220),     # мягкий серый
        "stroke_width": 4,
},
"gold_ice": {
        "fill": (212, 175, 55, 255),
        "stroke": (180, 220, 255, 255),
        "stroke_width": 4,
    },
    "gold_lilac": {
        "fill": (212, 175, 55, 255),
        "stroke": (200, 180, 255, 255),   # мягкий сиреневый
        "stroke_width": 5,
    },
   "ice_gold ": {
        "fill": (180, 220, 255, 255),     # ледяной голубой
        "stroke": (212, 175, 55, 255),    # золото
        "stroke_width": 5, '''