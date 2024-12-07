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
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from fluent.runtime import FluentLocalization
from bot.services.users import UserService
from bot.services.fails import FailService


router = Router()

class FailStates(StatesGroup):
    """Состояния для обработки создания записи о неудаче."""
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_action = State()
    
@router.message(Command("fail"))
async def start_fail_creation(
    message: Message, 
    state: FSMContext, 
    l10n: FluentLocalization
):
    """
    Начинает процесс создания записи о неудаче.

    Устанавливает состояние ожидания ввода названия фейла и запрашивает
    у пользователя название фейла.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        l10n (FluentLocalization): Объект локализации.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=l10n.format_value("btn-cancel"), callback_data="cancel_fail")
    
    await state.set_state(FailStates.waiting_for_name)
    await message.reply(
        l10n.format_value("type-name-fail"),
        reply_markup=keyboard.as_markup()
    )
    
@router.message(FailStates.waiting_for_name)
async def process_fail_name(
    message: Message, 
    state: FSMContext, 
    l10n: FluentLocalization
):
    """
    Обрабатывает ввод названия фейла.

    Проверяет длину названия и, если оно корректно, сохраняет его
    в состоянии и запрашивает описание фейла.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        l10n (FluentLocalization): Объект локализации.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=l10n.format_value("btn-cancel"), callback_data="cancel_fail")
    
    if len(message.text) > 100:
        await message.reply(l10n.format_value("fail-name-too-long"))
        return
    
    await state.update_data(name=message.text)
    await state.set_state(FailStates.waiting_for_description)
    await message.reply(
        l10n.format_value("type-discription-fail"),
        reply_markup=keyboard.as_markup()
    )

@router.message(FailStates.waiting_for_description)
async def process_description(
    message: Message, 
    state: FSMContext, 
    session: AsyncSession,
    l10n: FluentLocalization
):
    """
    Обрабатывает ввод описания фейла.

    Проверяет длину описания, сохраняет запись о неудаче в базе данных
    и уведомляет пользователя об успешном добавлении.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=l10n.format_value("btn-cancel"), callback_data="cancel_fail")
    
    if len(message.text) > 1000:
        await message.reply(l10n.format_value("fail-description-too-long"))
        return
    
    user_data = await state.get_data()
    await state.clear()
    
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(message.from_user.id)
    
    if not user:
        await message.reply(l10n.format_value("user-not-found"))
        return
    
    await state.update_data(description=message.text)
    
    builder = InlineKeyboardBuilder()
    builder.button(text=l10n.format_value("publish_now"), callback_data="publish_now")
    builder.button(text=l10n.format_value("save-draft"), callback_data="save-draft")
    builder.button(text=l10n.format_value("cancel"), callback_data="cancel_fail")
    
    await message.reply(
        l10n.format_value("choose-fail-action"),
        reply_markup=builder.as_markup()
    )
    await state.set_state(FailStates.waiting_for_action)

@router.callback_query(F.data == "publish_fail")
async def publish_fail(
    message: Message, 
    callback: CallbackQuery, 
    state: FSMContext, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Публикация фейла.
    
    Создает запись о фейле в базе данных и уведомляет пользователя об успешном добавлении.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(message.from_user.id)
    
    if not user:
        await message.reply(l10n.format_value("user-not-found"))
        return
    
    data = await state.get_data()
    
    fail_service = FailService(session)
    fail = await fail_service.create_fail(
        user_id=user.id,
        name=data["name"],
        description=data["description"],
        is_draft=False
    )
    
    await callback.message.edit_text(l10n.format_value("fail-published"))

@router.callback_query(F.data == "save_draft")
async def save_draft(
    message: Message, 
    callback: CallbackQuery, 
    state: FSMContext, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Сохранение фейла как черновика.
    
    Создает запись о фейле в базе данных и уведомляет пользователя об успешном добавлении как черновика.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(message.from_user.id)
    
    if not user:
        await message.reply(l10n.format_value("user-not-found"))
        return
    
    data = await state.get_data()
    
    fail_service = FailService(session)
    fail = await fail_service.create_fail(
        user_id=user.id,
        name=data["name"],
        description=data["description"],
        is_draft=True
    )
    await callback.message.edit_text(l10n.format_value("fail-saved-as-draft"))

@router.message(Command("drafts"))
async def show_drafts(
    message: Message, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Показывает список черновиков фейлов пользователя.

    Attributes:
        message (Message): Сообщение от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(message.from_user.id)
    
    if not user:
        await message.answer(l10n.format_value("user-not-found"))
        return
    
    fail_service = FailService(session)
    drafts = await fail_service.get_user_drafts(user.id)
    
    if not drafts:
        await message.answer(l10n.format_value("no-drafts"))
        return
    
    builder = InlineKeyboardBuilder()
    for draft in drafts:
       builder.button(
            text=draft.name,
            callback_data=f"manage_draft:{draft.id}"
        )
    builder.adjust(1)
    
    await message.answer(
        l10n.format_value("your-drafts"),
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("manage_draft:"))
async def manage_draft(
    callback: CallbackQuery, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Меню управления черновиком фейла.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    
    draft_id = int(callback.data.split(":")[1])
    
    builder = InlineKeyboardBuilder()
    builder.button(text="📢 Опубликовать", callback_data=f"publish_draft:{draft_id}")
    builder.button(text="🗑 Удалить", callback_data=f"delete_fail:{draft_id}")
    builder.button(text="↩️ Назад", callback_data="back_to_drafts")
    
    await callback.message.edit_text(
        l10n.format_value("manage-draft"),
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "back_to_drafts")
async def back_to_drafts(
    callback: CallbackQuery, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Возвращает к списку черновиков
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    fail_service = FailService(session)
    drafts = await fail_service.get_user_drafts(callback.from_user.id)
    
    builder = InlineKeyboardBuilder()
    for draft in drafts:
        builder.button(
            text=draft.name,
            callback_data=f"manage_draft:{draft.id}"
        )
    builder.adjust(1)
    
    await callback.message.edit_text(
        l10n.format_value("your-drafts"),
        reply_markup=builder.as_markup()
    )
    
@router.callback_query(F.data.startswith("publish_draft:"))
async def publish_draft(callback: CallbackQuery, session: AsyncSession, l10n: FluentLocalization):
    """
    Публикует черновик фейла.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    draft_id = int(callback.data.split(":")[1])
    
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(callback.from_user.id)
    
    if not user:
        await callback.answer(l10n.format_value("user-not-found"))
        return
        
    fail_service = FailService(session)
    if await fail_service.publish_draft(draft_id, user.id):
        await callback.message.edit_text(l10n.format_value("draft-published"))
    else:
        await callback.answer(l10n.format_value("publish-error"), show_alert=True)
        
@router.message(StateFilter(FailStates), Command("start", "help", "top", "vote", "fail"))
async def cancel_fail_creation(message: Message, state: FSMContext):
    """
    Отменяет создание фейла при получении другой команды
    
    Attributes:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
    """
    await state.clear()
    # Выполняем команду заново
    await message.forward(message.chat.id)

@router.callback_query(F.data == "cancel_fail")
async def cancel_fail_callback(
    callback: CallbackQuery, 
    state: FSMContext, 
    l10n: FluentLocalization
):
    """
    Отменяет создание фейла при нажатии на кнопку отмены
    
    Attributes:
        callback (CallbackQuery): Объект колбэка от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        l10n (FluentLocalization): Объект локализации.
    """
    await state.clear()
    await callback.message.edit_text(l10n.format_value("fail-cancelled"))
     
@router.message(Command("top"))
async def show_top_losers(
    message: Message, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Показывает топ пользователей с наибольшим количеством неудач.

    Запрашивает данные о пользователях с наибольшим количеством
    неудач и отправляет их пользователю.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    fail_service = FailService(session)
    
    top_users = await fail_service.get_top_losers(10)
    
    if not top_users:
        await message.answer(l10n.format_value("no-fails"))
        return
    
    text = l10n.format_value("top-losers-caption") + "\n\n"
    for i, (user, total_rating) in enumerate(top_users, 1):
        text += l10n.format_value(
            "top-loser-caption", 
            {
                "index": i, 
                "user_name": user.username, 
                "total_rating":total_rating
            }
        ) + "\n"
    
    await message.answer(text)

@router.message(Command("vote"))
async def show_fails_for_voting(
    message: Message, 
    session: AsyncSession,
    l10n: FluentLocalization
):
    """
    Показывает фейлы для голосования.

    Запрашивает фейлы, доступные для голосования, и отправляет их
    пользователю в виде кнопок.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    fail_service = FailService(session)
    fails = await fail_service.get_fails_for_voting(10)
    
    if not fails:
        await message.answer(l10n.format_value("no-fails-for-voting"))
        return
    
    builder = InlineKeyboardBuilder()
    for fail in fails:
        builder.button(
            text=fail.name, 
            callback_data=f"read_fail:{fail.id}"
        )
    builder.adjust(1)
    
    await message.answer(
        l10n.format_value("choose-fail-to-vote"),
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("read_fail:"))
async def read_fail(
    callback: CallbackQuery, 
    session: AsyncSession,
    l10n: FluentLocalization
):
    """
    Отображает информацию о выбранном фейле.

    Загружает данные о фейле и предоставляет возможность голосовать
    за него, добавляя кнопки для голосования.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    fail_id = int(callback.data.split(":")[1])
    fail_service = FailService(session)
    fail = await fail_service.get_fail_by_id(fail_id)
    
    if not fail or not fail.user:
        await callback.answer(
            l10n.format_value("fail-not-found"), 
            show_alert=True
        )
        return
    
    builder = InlineKeyboardBuilder()
    builder.button(text=l10n.format_value("vote-down"), callback_data=f"vote:{fail.id}:-1")
    builder.button(text=l10n.format_value("vote-up"), callback_data=f"vote:{fail.id}:1")
    
    await callback.message.edit_text(
        l10n.format_value("fail-info"),
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("vote:"))
async def vote_fail(
    callback: CallbackQuery, 
    session: AsyncSession,
    l10n: FluentLocalization
):
    """
    Обрабатывает голосование за фейл.

    Обновляет рейтинг фейла в базе данных в зависимости от
    выбора пользователя и подтверждает голос.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    _, fail_id, rating = callback.data.split(":")
    
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(callback.from_user.id)
    
    if not user:
        await callback.answer(l10n.format_value("user-not-found"))
        return

    fail_service = FailService(session)
    if await fail_service.update_rating(int(fail_id), user.id, int(rating)):
        await callback.answer(l10n.format_value("vote-success"))
    else:
        await callback.answer(l10n.format_value("already-voted"), show_alert=True)
    
@router.message(Command("my_fails"))
async def show_user_fails(
    message: Message, 
    session: AsyncSession,
    l10n: FluentLocalization
):
    """
    Отображает список фейлов, созданных пользователем.

    Загружает список фейлов, созданных пользователем, и отправляет
    его в виде кнопок.

    Attributes:
        message (Message): Сообщение от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(message.from_user.id)
    
    if not user:
        await message.answer(l10n.format_value("user-not-found"))
        return
    
    fail_service = FailService(session)
    fails = await fail_service.get_user_fails(user.id)

    if not fails:
        await message.answer(l10n.format_value("i-am-not-loser"))
        return
    
    builder = InlineKeyboardBuilder()
    for fail in fails:
        builder.button(
            text=fail.name, 
            callback_data=f"read_fail:{fail.id}"
        )
    builder.adjust(1)
    
    await message.answer(
        l10n.format_value("choose-fail-to-delete"),
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("delete_fail:"))
async def confirm_delete_fail(
    callback: CallbackQuery, 
    session: AsyncSession,
    l10n: FluentLocalization
):
    """
    Подтверждает удаление фейла.

    Подтверждает удаление выбранного фейла и удаляет его из базы данных.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    fail_id = int(callback.data.split(":")[1])
    
    builder = InlineKeyboardBuilder()
    builder.button(
        text=l10n.format_value("confirm-delete"),
        callback_data=f"confirm_delete:{fail_id}"
    )
    builder.button(
        text=l10n.format_value("cancel"),
        callback_data="cancel_delete"
    )
    
    await callback.message.edit_text(
        l10n.format_value("confirm-delete-message"),
        reply_markup=builder.as_markup()
    )
    
@router.callback_query(F.data.startswith("confirm_delete:"))
async def delete_fail(
    callback: CallbackQuery, 
    session: AsyncSession,
    l10n: FluentLocalization
):
    """
    Удаляет фейл из базы данных.

    Удаляет выбранный фейл из базы данных и подтверждает удаление.

    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    fail_id = int(callback.data.split(":")[1])
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(callback.from_user.id)
    
    if not user:
        await callback.answer(l10n.format_value("user-not-found"))
        return

    fail_service = FailService(session)
    if await fail_service.delete_fail(fail_id, user.id):
        await callback.answer(l10n.format_value("fail-deleted"))
    else:
        await callback.answer(l10n.format_value("fail-delete-error"))
    
@router.callback_query(F.data == "cancel_delete")
async def cancel_delete(
    callback: CallbackQuery, 
    l10n: FluentLocalization
):
    """
    Отменяет удаление.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        l10n (FluentLocalization): Объект локализации.
    """
    await callback.message.edit_text(l10n.format_value("delete-cancelled"))