"""
Хендлеры Telegram-бота для создания открыток.

Отвечают за:
- сценарий общения с пользователем
- переключение состояний FSM
- обработку сообщений и callback-запросов
- вызов сервисов генерации изображений и текстов

Бизнес-логика и генерация изображений вынесены в services.
"""

import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from bot.fsm import StateImage
from config import image_files, OCCASIONS
from bot.keyboards import (select_image_first, select_image, select_resp_for_text, select_occasion,
                           continue_select_image, start_selector, select_text_first, select_text)
from services.image_service import get_user_images
from aiogram.fsm.context import FSMContext
from services.image_generator_v3 import pic_creator
from services.file_storage import clear_user_dir
from services.text_service import load_texts
from bot.fsm_data_keys import CardFSMData
from tools.edit_media_with_click_guard import edit_media_prevent_duplicate
from aiogram.exceptions import TelegramBadRequest
import logging


logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start_pic(message: Message, state: FSMContext):
    logger.info(
        "Пользователь %s запустил бота",
        message.from_user.id
    )
    data = await state.get_data()

    await state.clear()
    user_id = message.from_user.id
    clear_user_dir(user_id)
    index_image = 0
    photo = FSInputFile(image_files[index_image])

    await message.answer_photo(photo=photo, caption='Выберите фон для открытки', reply_markup=select_image_first())
    await state.set_state(StateImage.index_image)
    await state.update_data(image=0)


@router.callback_query(F.data.in_({'next', 'back'}), StateFilter(StateImage.index_preview, StateImage.index_image))
async def navigate_image(call: CallbackQuery, state: FSMContext):
    """
        Обрабатывает навигацию по изображениям (вперёд / назад).

        Используется в двух режимах:
        - выбор фонового изображения
        - предпросмотр сгенерированных открыток

        Направление навигации определяется по callback-данным.
        """

    data: CardFSMData = await state.get_data()
    current_state = await state.get_state()
    files = []
    if current_state == StateImage.index_image:
        files = image_files
        index_key = "image"
    elif current_state == StateImage.index_preview:
        files = get_user_images(call.from_user.id)
        index_key = "prev"
        if not files:
            await call.answer("Нет изображений")
            return
    else:
        await call.answer()
    ind_image = data.get(index_key, 0)

    delta = 1 if call.data == "next" else -1
    ind_image = (ind_image + delta) % len(files)

    media = InputMediaPhoto(media=FSInputFile(files[ind_image]))
    ok = await edit_media_prevent_duplicate(
        call,
        media,
        select_image()
    )
    if not ok:
        return
    await state.update_data(**{index_key: ind_image})


@router.callback_query(F.data=='select', StateFilter(StateImage.index_image, StateImage.index_preview))
async def select_pic(call: CallbackQuery, state: FSMContext):
    data: CardFSMData = await state.get_data()
    current_state = await state.get_state()

    if current_state == StateImage.index_image:
        await state.update_data(image=data.get("image", 0))
        await call.message.delete()
        await call.message.answer('Выбрать текст для открытки', reply_markup=select_resp_for_text())
        await state.set_state(StateImage.occasion)
        await call.answer()

    elif current_state == StateImage.index_preview:
        files = get_user_images(call.from_user.id)
        ind_key = data.get("prev")
        await call.message.delete()
        if files:
            photo = FSInputFile(files[ind_key])
            await call.message.answer_photo(photo=photo, reply_markup=start_selector())
            await call.answer()
        else:
            await call.message.answer('Что-то пошло не так. Попробуйте еще раз.', reply_markup=start_selector())
        await state.clear()
    else:
        await call.answer()


@router.callback_query(F.data=='not_select_text', StateFilter(StateImage.occasion))
async def pic_without_text(call: CallbackQuery, state: FSMContext):
    """Отправляет открытку фон без текста"""
    data: CardFSMData = await state.get_data()
    index = data.get("image", 0)
    image = image_files[index]

    media = InputMediaPhoto(
        media=FSInputFile(image),
        caption='Открытка без добавления текста'
    )

    try:
        await call.message.edit_media(media=media)
    except TelegramBadRequest:
        await call.answer("Пожалуйста, подождите 🙂", show_alert=True)
        return
    await call.answer()
    await call.message.answer('Хотите продолжить?', reply_markup=continue_select_image())
    await state.clear()


@router.callback_query(F.data == 'continue')
async def continue_select_pic(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    clear_user_dir(user_id)
    index_image = 0
    photo = FSInputFile(image_files[index_image])

    await call.message.answer_photo(photo=photo, caption='Выберите фон для открытки', reply_markup=select_image_first())
    await call.answer()
    await state.set_state(StateImage.index_image)
    await state.update_data(image=0)



@router.callback_query(F.data=='stop')
async def stop_creator_pic(call: CallbackQuery, state: FSMContext):
    """
    Останавливает генерацию открыток пользователем.
    Очищается ФСМ
    """

    await call.message.answer('Возвращайтесь за новыми открытками! Запустить бота можно с помощью команды /start или нажать кнопку ниже', reply_markup=start_selector())
    await state.clear()



@router.callback_query(F.data.in_({"coming", "new_year", "christmas", "old_new_year"}), StateFilter(StateImage.occasion))
async def select_occasion_coming(call: CallbackQuery, state: FSMContext):
    """
       Обрабатывает выбор повода для открытки.

       В зависимости от режима:
       - user: запрашивает ввод текста от пользователя
       - bot: загружает готовые тексты и запускает их просмотр

       После выбора переводит FSM в состояние ввода / выбора текста.
       """
    data: CardFSMData = await state.get_data()
    occasion_key = call.data
    # OCCASIONS словарь для выбора текста по колбаку и имени файла
    await state.update_data(occasion=OCCASIONS[occasion_key]["title"])
    role = data.get('text_role')
    if role == 'user':
        await call.message.delete()
        msg = await call.message.answer(
            'Введите текст для открытки. Не более 10 слов'
        )
        await state.update_data(prompt_message_id=msg.message_id)
    elif role == 'bot':
        texts = load_texts(occasion_key)
        await state.update_data(
            texts=texts,
            text_index=0
        )
        await call.message.edit_text(
            texts[0],
            reply_markup=select_text_first()
        )
    await state.set_state(StateImage.text)


@router.callback_query(F.data.in_({'user_text','bot_text'}), StateFilter(StateImage.occasion))
async def get_occasion(call: CallbackQuery, state: FSMContext):
    """
        Обрабатывает выбор режима текста для открытки.

        Режимы:
        - user_text: пользователь вводит текст вручную
        - bot_text: бот предлагает готовые тексты

        После выбора предлагает выбрать повод,
        который будет использован как заголовок открытки.
        """
    await call.message.delete()
    await call.message.answer('Выберите повод для поздравления. Повод будет установлен в виде заголовка', reply_markup=select_occasion())

    role = call.data
    if role == 'user_text':
        await state.update_data(text_role='user')
    elif role == 'bot_text':
        await state.update_data(text_role='bot')


@router.message(StateFilter(StateImage.text))
async def create_pic_user_text(message: Message, state: FSMContext):
    """
        Создаёт открытку на основе текста,
        введённого пользователем вручную.

        Этапы:
        - принимает текст
        - удаляет служебное сообщение бота
        - запускает генерацию изображения в отдельном потоке
        - переводит пользователя в режим предпросмотра

        Используется только в режиме user_text.
        """
    data: CardFSMData = await state.get_data()

    text_for_pic = message.text
    user_id = message.from_user.id
    logger.info(
        "Начата генерация открытки | пользователь=%s | изображение=%s | повод=%s",
        user_id,
        data["image"],
        data["occasion"]
    )
    await state.update_data(user_text=text_for_pic)

    prompt_id = data.get("prompt_message_id")
    if prompt_id:                 # удаляю предыдущее сообщение бота, после принятия сообщения от пользователя.
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=prompt_id
        )
    status_msg = await message.answer("Текст принят 👍\nМинуточку, идет процесс создания открытки")
    try:
        await asyncio.to_thread(
            pic_creator,
            image_files[data["image"]],
            data["occasion"],
            text_for_pic,
            user_id
        )
        logger.info(
            "Открытка успешно создана | пользователь=%s | режим=текст_пользователя",
            user_id
        )
    except Exception:
        logger.exception(
            "Ошибка при создании открытки | пользователь=%s",
            user_id
        )
        await message.answer("Ошибка при создании открытки 😔")
        return

    list_image = get_user_images(user_id)
    if not list_image:
        await message.answer("Нет изображений")
        return
    await state.set_state(StateImage.index_preview)
    await state.update_data(prev=0)
    media = InputMediaPhoto(
    media=FSInputFile(list_image[0]))
    try:
        await status_msg.edit_media(media=media, reply_markup=select_image_first())
    except TelegramBadRequest:
        return



@router.callback_query(F.data.in_({'next_text','back_text'}), StateFilter(StateImage.text))
async def selector_text_next(call: CallbackQuery,state: FSMContext):
    """
    Листает готовые тексты открытки (вперёд / назад).

    Если список текстов недоступен, возвращает пользователя
    к выбору повода и переводит FSM в состояние StateImage.occasion.
    """
    data: CardFSMData = await state.get_data()
    texts = data.get('texts')  # список текстов
    index = data.get('text_index', 0)
    if texts:
        delta = 1 if call.data == "next_text" else -1
        new_index = (index + delta) % len(texts)
        await call.message.delete()
        msg = await call.message.answer(
            text=texts[new_index],
            reply_markup=select_text()
        )
        await state.update_data(
            text_index=new_index,
            prompt_message_id=msg.message_id
        )

        await call.answer()
    else:
        await call.message.delete()
        await call.message.answer(
            "Тексты недоступны. Пожалуйста, выберите повод заново.",
             reply_markup=select_occasion()
        )
        await state.set_state(StateImage.occasion)
        await call.answer()




@router.callback_query(F.data=='select_text', StateFilter(StateImage.text))
async def create_pic_with_bot_text(call: CallbackQuery, state: FSMContext):
    """
    Создаёт открытку с выбранным готовым текстом.

    Использует текст из списка, сохранённого в FSM,
    запускает генерацию изображения и переводит пользователя
    в режим предпросмотра результата.
    """
    data: CardFSMData = await state.get_data()
    user_id = call.from_user.id
    text_list = data['texts']
    ind = data['text_index']

    await call.message.delete()

    status_msg = await call.message.answer("Минуточку, идет процесс создания открытки")
    try:
        await asyncio.to_thread(
            pic_creator,
            image_files[data["image"]],
            data["occasion"],
            text_list[ind],
            user_id
        )
        logger.info(
            "Открытка успешно создана | пользователь=%s | режим=готовый_текст",
            user_id
        )
    except Exception:
        logger.exception(
            "Ошибка при создании открытки | пользователь=%s",
            user_id
        )
        await call.message.answer("Ошибка при создании открытки 😔")
        return
    list_image = get_user_images(user_id)
    if not list_image:
        await call.message.answer("Нет изображений")
        return
    await state.set_state(StateImage.index_preview)
    await state.update_data(prev=0)

    media = InputMediaPhoto(media=FSInputFile(list_image[0]))
    try:
        await status_msg.edit_media(media=media, reply_markup=select_image_first())
    except TelegramBadRequest:
        return
    await call.answer()