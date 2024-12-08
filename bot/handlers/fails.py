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
from bot.models import FailStatus, UserModel, FailModel
from logging import info

router = Router()

class FailStates(StatesGroup):
    """Состояния для обработки создания записи о неудаче."""
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_action = State()
    editing_name = State()
    editing_description = State()

# Базовые утилиты
async def check_user(user_id: int, message: Message | CallbackQuery, session: AsyncSession, l10n: FluentLocalization) -> UserModel | None:
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(user_id)
    if not user:
        await message.answer(l10n.format_value("user-not-found"), show_alert=True)
        return None
    return user

async def check_fail(fail_id: int, session: AsyncSession, message: Message | CallbackQuery, l10n: FluentLocalization) -> FailModel | None:
    fail_service = FailService(session)
    fail = await fail_service.get_fail_by_id(fail_id)
    if not fail:
        await message.answer(l10n.format_value("fail-not-found"), show_alert=True)
        return None
    return fail

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
    
    # Отправляем сообщение и сохраняем его ID
    sent_message = await message.answer(
        l10n.format_value("type-name-fail"),
        reply_markup=keyboard.as_markup()
    )
    # Сохраняем message_id и chat_id в состоянии
    await state.set_state(FailStates.waiting_for_name)
    await state.update_data(message_id=sent_message.message_id, chat_id=message.chat.id)
    
    # Удаляем команду пользователя
    await message.delete()
    
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
    
    # Получаем сохраненные данные
    data = await state.get_data()
    
    # Обновляем существующее сообщение
    await message.bot.edit_message_text(
        l10n.format_value("type-discription-fail"),
        chat_id=data["chat_id"],
        message_id=data["message_id"],
        reply_markup=keyboard.as_markup()
    )
    
    await state.update_data(name=message.text)
    await state.set_state(FailStates.waiting_for_description)
    
    # Удаляем сообщение пользователя
    await message.delete()

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
    # Получаем сохраненные данные
    data = await state.get_data()
    if not data.get("message_id") or not data.get("chat_id"):
        await message.reply("Ошибка: Отсутствуют данные сообщения")
        await state.clear()
        return
    info(f"Сохраненные данные: {data}")
    
    # Проверяем длину описания
    if len(message.text) > 1000:
        await message.reply(l10n.format_value("fail-description-too-long"))
        return
    
    # Сохраняем описание
    await state.update_data(description=message.text)
    
    builder = InlineKeyboardBuilder()
    builder.button(text=l10n.format_value("btn-publish-now"), callback_data="publish_fail")
    builder.button(text=l10n.format_value("btn-save-draft"), callback_data="save_draft")
    builder.button(text=l10n.format_value("btn-cancel"), callback_data="cancel_fail")
    
    await message.bot.edit_message_text(
        l10n.format_value("choose-fail-action"),
        chat_id=data["chat_id"],
        message_id=data["message_id"],
        reply_markup=builder.as_markup()
    )
    # Устанавливаем следующее состояние
    await state.set_state(FailStates.waiting_for_action)
    await message.delete()

@router.callback_query(F.data == "publish_fail")
async def publish_fail(
    callback: CallbackQuery, 
    state: FSMContext, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Публикация фейла.
    
    Создает запись о фейле в базе данных и уведомляет пользователя об успешном добавлении.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """

    user = await check_user(callback.from_user.id, callback, session, l10n)
    if not user:
        return
    
    data = await state.get_data()
    
    fail_service = FailService(session)
    fail = await fail_service.create_fail(
        user_id=user.id,
        name=data["name"],
        description=data["description"],
        status=FailStatus.CHECKING
    )
    
    await callback.message.edit_text(l10n.format_value("fail-checking"))
    await state.clear()

@router.callback_query(F.data == "save_draft")
async def save_draft(
    callback: CallbackQuery, 
    state: FSMContext, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Сохранение фейла как черновика.
    
    Создает запись о фейле в базе данных и уведомляет пользователя об успешном добавлении как черновика.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    
    user = await check_user(callback.from_user.id, callback, session, l10n)
    if not user:
        return
    
    data = await state.get_data()
    
    fail_service = FailService(session)
    fail = await fail_service.create_fail(
        user_id=user.id,
        name=data["name"],
        description=data["description"],
        status=FailStatus.DRAFT
    )
    await callback.message.delete()
    await callback.answer(l10n.format_value("fail-saved-as-draft"), show_alert=True)
    await state.clear()

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

    user = await check_user(message.from_user.id, message, session, l10n)
    if not user:
        return
    
    fail_service = FailService(session)
    drafts = await fail_service.get_user_drafts(user.id)
    
    if not drafts:
        await message.answer(l10n.format_value("no-drafts"))
        await message.delete()
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
    await message.delete()

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
    builder.button(text=l10n.format_value("btn-publish-now"), callback_data=f"publish_draft:{draft_id}")
    builder.button(text=l10n.format_value("btn-edit-draft"), callback_data=f"edit_draft:{draft_id}")
    builder.button(text=l10n.format_value("btn-delete-draft"), callback_data=f"delete_fail:{draft_id}")
    builder.button(text=l10n.format_value("btn-back-to-drafts"), callback_data="back_to_drafts")
    
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

    user = await check_user(callback.from_user.id, callback, session, l10n)
    if not user:
        return
    
    fail_service = FailService(session)
    drafts = await fail_service.get_user_drafts(user.id)

    if not drafts:
        await callback.message.delete()
        await callback.answer(l10n.format_value("no-drafts"), show_alert=True)
        return
    
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
    
    user = await check_user(callback.from_user.id, callback, session, l10n)
    if not user:
        return
        
    fail_service = FailService(session)
    if await fail_service.publish_draft(draft_id, user.id):
        await callback.message.edit_text(l10n.format_value("draft-published"))
    else:
        await callback.answer(l10n.format_value("publish-error"), show_alert=True)
        

     
@router.message(Command("top"))
async def show_top_losers(
    message: Message, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Показывает топ пользователей с наибольшим количеством неудач.
    
    Attributes:
        message (Message): Сообщение от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    fail_service = FailService(session)
    top_users = await fail_service.get_top_losers(10)
    
    if not top_users:
        await message.answer(l10n.format_value("top-losers-no-fails"))
        return
    
    text = l10n.format_value("top-losers-caption") + "\n\n"
    for i, (user, total_rating) in enumerate(top_users, 1):
        text += l10n.format_value(
            "top-loser-caption", 
            {
                "index": i, 
                "user_name": user.username, 
                "total_rating": total_rating
            }
        ) + "\n"
    
    await message.answer(text)
    await message.delete()

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
    await message.delete()
    
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
    
    fail = await check_fail(fail_id, session, callback, l10n)
    if not fail or not fail.user:
        return
    
    builder = InlineKeyboardBuilder()
    builder.button(text=l10n.format_value("vote-down"), callback_data=f"vote:{fail.id}:-1")
    builder.button(text=l10n.format_value("vote-up"), callback_data=f"vote:{fail.id}:1")
    
    await callback.message.edit_text(
        l10n.format_value("vote-info", {
            "user_name": fail.user.username,
            "fail_name": fail.name,
            "fail_description": fail.description,
            "fail_rating": fail.rating
        }),
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
    
    user = await check_user(callback.from_user.id, callback, session, l10n)
    if not user:
        return

    # Обновляем рейтинг фейла в базе данных или выводим сообщение о том, 
    # что пользователь уже голосовал за этот фейл.
    fail_service = FailService(session)
    if await fail_service.update_rating(int(fail_id), user.id, int(rating)):
        await callback.message.edit_text(l10n.format_value("vote-success"))
    else:
        await callback.message.edit_text(l10n.format_value("already-voted"), show_alert=True)
    
@router.message(Command("publics"))
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
    user = await check_user(message.from_user.id, message, session, l10n)
    if not user:
        return
    
    fail_service = FailService(session)
    fails = await fail_service.get_user_fails(user.id)

    if not fails:
        await message.answer(l10n.format_value("i-am-not-a-loser"))
        return
    
    builder = InlineKeyboardBuilder()
    for fail in fails:
        builder.button(
            text=fail.name, 
            callback_data=f"manage_public:{fail.id}"
        )
    builder.adjust(1)
    
    await message.answer(
        l10n.format_value("choose-fail-to-delete"),
        reply_markup=builder.as_markup()
    )
    await message.delete()

@router.callback_query(F.data.startswith("manage_public:"))
async def manage_public_fail(callback: CallbackQuery, session: AsyncSession, l10n: FluentLocalization):
    fail_id = int(callback.data.split(":")[1])
    
    builder = InlineKeyboardBuilder()
    builder.button(text=l10n.format_value("btn-to-draft"), callback_data=f"to_draft:{fail_id}")
    builder.button(text=l10n.format_value("btn-delete-fail"), callback_data=f"delete_fail:{fail_id}")
    
    await callback.message.edit_text(
        l10n.format_value("manage-public-fail"),
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("to_draft:"))
async def to_draft(
    callback: CallbackQuery, 
    session: AsyncSession,
    l10n: FluentLocalization
):
    """
    Переводит фейл в черновик.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    fail_id = int(callback.data.split(":")[1])
    fail_service = FailService(session)
    await fail_service.to_draft(fail_id)
    await callback.message.edit_text(l10n.format_value("fail-to-draft"))
    
    
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
        text=l10n.format_value("btn-confirm-delete"),
        callback_data=f"confirm_delete:{fail_id}"
    )
    builder.button(
        text=l10n.format_value("btn-cancel-delete"),
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
    
    user = await check_user(callback.from_user.id, callback, session, l10n)
    if not user:
        return

    fail_service = FailService(session)
    if await fail_service.delete_fail(fail_id, user.id):
        await callback.answer(l10n.format_value("fail-deleted-popup"))
        await callback.message.delete()
        await callback.answer(l10n.format_value("fail-deleted-popup"), show_alert=True)
    else:
        await callback.answer(l10n.format_value("fail-delete-error"), show_alert=True)

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

@router.callback_query(F.data.in_(["cancel_fail", "cancel_delete"]))
async def handle_cancel(callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization):
    """
    Кнопка отмены.
    
    Attributes:
        callback (CallbackQuery): Объект колбэка от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        l10n (FluentLocalization): Объект локализации.
    """
    await state.clear()
    await callback.message.delete()
    await callback.answer(l10n.format_value("operation-cancelled"), show_alert=True)
    

@router.callback_query(F.data.startswith("edit_draft:"))
async def start_edit_draft(callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization):
    draft_id = int(callback.data.split(":")[1])
    await state.update_data(draft_id=draft_id)
    await state.set_state(FailStates.editing_name)
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=l10n.format_value("btn-cancel"), callback_data="cancel_edit")
    
    await callback.message.edit_text(
        l10n.format_value("type-name-fail"),
        reply_markup=keyboard.as_markup()
    )

@router.message(FailStates.editing_name)
async def edit_draft_name(message: Message, state: FSMContext, l10n: FluentLocalization):
    if len(message.text) > 100:
        await message.answer(l10n.format_value("fail-name-too-long"))
        return
        
    await state.update_data(new_name=message.text)
    await state.set_state(FailStates.editing_description)
    
    await message.answer(l10n.format_value("type-discription-fail"))
    await message.delete()

@router.message(FailStates.editing_description)
async def edit_draft_description(message: Message, state: FSMContext, session: AsyncSession, l10n: FluentLocalization):
    if len(message.text) > 1000:
        await message.answer(l10n.format_value("fail-description-too-long"))
        return
        
    data = await state.get_data()
    fail_service = FailService(session)
    
    if await fail_service.update_draft(data["draft_id"], data["new_name"], message.text):
        await message.answer(l10n.format_value("draft-updated"))
    else:
        await message.answer(l10n.format_value("draft-update-error"))
        
    await state.clear()
    await message.delete()