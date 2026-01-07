# 🎴 Telegram Card Generator Bot

##  Описание

Telegram-бот для создания поздравительных открыток.  
Пользователь выбирает фон из заранее подготовленной коллекции изображений
(бесплатные фотостоки и открытые источники),
затем добавляет текст (свой или готовый), после чего бот формирует открытку
и позволяет просмотреть результат.

Проект оформлен как полноценный pet-проект
с пошаговой логикой, обработкой ошибок и подготовкой к деплою.

Бот представляет собой интерактивный конструктор открыток
с мгновенной визуальной обратной связью.

---

##  Зачем нужен такой бот

Несмотря на наличие AI-генераторов и графических редакторов,
такой формат остаётся востребованным за счёт простоты и понятности.

Не всем пользователям комфортно работать с промтами,
подбирать формулировки или разбираться в настройках AI-инструментов.
В данном боте процесс создания открытки сводится к понятным шагам:
выбор фона и добавление текста.

Пользователь может собрать персональную открытку —
с понравившимся фоном и именным поздравлением —
без необходимости изучать дополнительные инструменты.

Формат конструктора делает процесс похожим на небольшую игру,
а мгновенная визуальная обратная связь усиливает вовлечённость
и ощущение индивидуального результата.

___


##  Возможности

- Выбор фона для открытки
- Навигация по изображениям (вперёд / назад)
- Добавление:
  - собственного текста
  - готовых вариантов текста
- Генерация изображений
- Предпросмотр результата
- Защита от повторных кликов
- Логирование основных действий и ошибок

---

## 🧠 Как работает логика

- Используется FSM (машина состояний) для пошагового сценария
- Тяжёлая генерация изображений выполняется асинхронно, без блокировки бота
- Ошибки обрабатываются и логируются
- Пользователь всегда получает понятный ответ от бота

---

## 🛠 Технологии

- Python
- aiogram 3
- FSM (Finite State Machine)
- Pillow (обработка изображений)
- asyncio
- logging

---

## 📌 Статус проекта

Pet-project  
Проект активно дорабатывается и используется для практики архитектуры, асинхронности и деплоя.

---

## 🤝 Использование AI-инструментов

Часть логики обработки изображений (Pillow) была разработана с использованием AI-ассистента.  
Код был адаптирован под проект, протестирован и интегрирован в общую архитектуру вручную.

Использование AI рассматривалось как инструмент ускорения разработки, при сохранении полного контроля над логикой, структурой проекта и поведением приложения.
___

## 🚀 Планы на развитие

- Деплой на Linux-сервер
- Улучшение логирования
- README с примерами
- Тестирование
- Добавление функционала

---

# 🎴 Telegram Card Generator Bot

## 🇬🇧 Description

Telegram bot for creating greeting cards.  
The user selects a background from a predefined image collection
(free stock images and public sources),
then adds text (custom or predefined), after which the bot generates a card
and allows the user to preview the result.

The project is structured as a full-fledged pet project
with step-by-step logic, error handling, and deployment preparation.

The bot acts as an interactive card constructor
with instant visual feedback.

---

##  Why this bot exists

Despite the availability of AI generators and graphic editors,
this format remains relevant due to its simplicity and clarity.

Not all users feel comfortable working with prompts,
adjusting wording, or navigating AI tool settings.
In this bot, the card creation process is reduced to clear steps:
selecting a background and adding text.

Users can create a personalized greeting card —
with a chosen background and a custom message —
without the need to learn additional tools.

The constructor-like flow makes the process feel slightly game-like,
while instant visual feedback increases engagement
and the sense of a unique, personal result.

___

## ✨ Features

- Background selection
- Image navigation (next / back)
- Text options:
  - custom user text
  - predefined text variants
- Image generation
- Result preview
- Protection from rapid duplicate clicks
- Logging of key actions and errors

---

## 🧠 Logic Overview

- FSM is used to manage step-by-step user flow
- Heavy image generation runs asynchronously without blocking the bot
- Errors are safely handled and logged
- User always receives clear feedback

---

## 🛠 Tech Stack

- Python
- aiogram 3
- FSM (Finite State Machine)
- Pillow
- asyncio
- logging

---

## 📌 Project Status

Pet-project  
Actively developed as a practice project for architecture, async logic, and deployment skills.

---

## 🤝 AI Assistance

Part of the image processing logic (Pillow) was developed with the help of an AI assistant.  
The code was adapted, tested, and manually integrated into the project architecture.

AI tools were used as a development accelerator while maintaining full control over logic, structure, and application behavior.


___

## 🚀 Future Plans

- Linux server deployment
- Improved logging
- Extended documentation
- Possible monetization
- Testing
