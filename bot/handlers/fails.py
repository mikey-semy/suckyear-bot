"""
Модуль для обработки команд, связанных с неудачами (fail).

Этот модуль содержит маршрутизатор для обработки сообщений, которые
начинаются с команды "/fail". Он использует сервис `FailService`
для создания записей о неудачах в базе данных.

Функции:
- create_fail: Обрабатывает команду "/fail" и создает новую запись о неудаче.
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from bot.services.users import UserService
from bot.services.fails import FailService
from logging import info

router = Router()

class FailStates(StatesGroup):
    """Состояния для обработки создания записи о неудаче."""
    waiting_for_name = State()
    waiting_for_description = State()
    
@router.message(Command("fail"))
async def start_fail_creation(message: Message, state: FSMContext):
    """
    Начинает процесс создания записи о неудаче.

    Устанавливает состояние ожидания ввода названия фейла и запрашивает
    у пользователя название фейла.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
    """
    await state.set_state(FailStates.waiting_for_name)
    await message.reply("Введите название фейла (до 100 символов):")
    
@router.message(FailStates.waiting_for_name)
async def process_fail_name(message: Message, state: FSMContext):
    """
    Обрабатывает ввод названия фейла.

    Проверяет длину названия и, если оно корректно, сохраняет его
    в состоянии и запрашивает описание фейла.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
    """
    if len(message.text) > 100:
        await message.reply("Слишком длинное название. Попробуйте короче:")
        return
    
    await state.update_data(name=message.text)
    await state.set_state(FailStates.waiting_for_description)
    await message.reply("Введите описание фейла (до 1000 символов):")

@router.message(FailStates.waiting_for_description)
async def process_description(
    message: Message, 
    state: FSMContext, 
    session: AsyncSession
):
    """
    Обрабатывает ввод описания фейла.

    Проверяет длину описания, сохраняет запись о неудаче в базе данных
    и уведомляет пользователя об успешном добавлении.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
    """
    if len(message.text) > 1000:
        await message.reply("Слишком длинное описание. Попробуйте короче:")
        return
    
    user_data = await state.get_data()
    await state.clear()
    
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(message.from_user.id)
    
    if not user:
        await message.reply("Ошибка: пользователь не найден")
        return
    
    fail_service = FailService(session)
    fail = await fail_service.create_fail(
        user_id=user.id,
        name=user_data["name"],
        description=message.text
    )
    
    await message.reply(
        f"Фейл успешно добавлен!\n\n"
        f"Название: {fail.name}\n"
        f"Описание: {fail.description}"
    )


@router.message(Command("top"))
async def show_top_losers(message: Message, session: AsyncSession):
    """
    Показывает топ пользователей с наибольшим количеством неудач.

    Запрашивает данные о пользователях с наибольшим количеством
    неудач и отправляет их пользователю.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
    """
    fail_service = FailService(session)
    
    await fail_service.debug_relationships()
    
    top_users = await fail_service.get_top_losers(10)
    
    if not top_users:
        await message.answer("Пока никто не нафейлил!")
        return
    
    info(f"Top losers: {top_users}")
    text = "🏆 Топ лузеров года:\n\n"
    for i, (user, total_rating) in enumerate(top_users, 1):
        text += f"{i}. {user.username}: {total_rating} очков позора\n"
    
    await message.answer(text)

@router.message(Command("vote"))
async def show_fails_for_voting(message: Message, session: AsyncSession):
    """
    Показывает фейлы для голосования.

    Запрашивает фейлы, доступные для голосования, и отправляет их
    пользователю в виде кнопок.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
    """
    fail_service = FailService(session)
    fails = await fail_service.get_fails_for_voting(5)
    
    if not fails:
        await message.answer("Пока нет фейлов для голосования!")
        return
    
    builder = InlineKeyboardBuilder()
    for fail in fails:
        builder.button(
            text=fail.name, 
            callback_data=f"read_fail:{fail.id}"
        )
    builder.adjust(1)
    
    await message.answer(
        "Выберите фейл для чтения:",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("read_fail:"))
async def read_fail(callback: CallbackQuery, session: AsyncSession):
    """
    Отображает информацию о выбранном фейле.

    Загружает данные о фейле и предоставляет возможность голосовать
    за него, добавляя кнопки для голосования.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
    """
    fail_id = int(callback.data.split(":")[1])
    fail_service = FailService(session)
    fail = await fail_service.get_fail_by_id(fail_id)
    
    if not fail or not fail.user:
        await callback.answer("Фейл не найден!", show_alert=True)
        return
    
    builder = InlineKeyboardBuilder()
    builder.button(text="👎 -1", callback_data=f"vote:{fail.id}:-1")
    builder.button(text="👍 +1", callback_data=f"vote:{fail.id}:1")
    
    text = f"🤦‍♂️ Фейл от {fail.user.username}:\n\n"
    text += f"Название: {fail.name}\n"
    text += f"Описание: {fail.description}\n"
    text += f"Текущий рейтинг: {fail.rating}"
    
    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("vote:"))
async def vote_fail(callback: CallbackQuery, session: AsyncSession):
    """
    Обрабатывает голосование за фейл.

    Обновляет рейтинг фейла в базе данных в зависимости от
    выбора пользователя и подтверждает голос.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
    """
    _, fail_id, rating = callback.data.split(":")
    fail_service = FailService(session)
    await fail_service.update_rating(int(fail_id), int(rating))
    await callback.answer("Голос учтен!")