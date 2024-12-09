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
from bot.services.menu import MenuManager
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

    menu_manager = MenuManager()

# Базовые утилиты
async def check_user(user_id: int, message: Message | CallbackQuery, session: AsyncSession, l10n: FluentLocalization) -> UserModel | None:
    user_service = UserService(session)
    user = await user_service.get_by_chat_id(user_id)
    if not user:
        await message.answer(l10n.format_value("user-not-found"), show_alert=True)
        return None
    return user

async def check_fail(fail_id: int, message: Message | CallbackQuery, session: AsyncSession, l10n: FluentLocalization) -> FailModel | None:
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
    # Получаем клавиатуру из конфигурации
    keyboard = menu_manager.get_keyboard('fail_creation')
    state_config = menu_manager.get_state_config('fail_creation.states.name')
    
    # Отправляем сообщение с inline клавиатурой
    sent_message = await message.answer(
        l10n.format_value("type-name-fail"),
        reply_markup=keyboard.as_markup()
    )

    # Сохраняем данные и устанавливаем состояние
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
    # Получаем конфигурацию для текущего состояния
    name_config = menu_manager.get_state_config('fail_creation.states.name')
    desc_config = menu_manager.get_state_config('fail_creation.states.description')
    
    # Проверяем длину названия согласно конфигурации
    if len(message.text) > name_config['validation']['max_length']:
        await message.answer(
            l10n.format_value(name_config['validation']['error']),
            show_alert=True
        )
        return
    
    # Получаем сохраненные данные и клавиатуру для следующего шага
    data = await state.get_data()
    keyboard = menu_manager.get_keyboard('fail_creation')
    
    try:
        # Обновляем существующее сообщение
        await message.bot.edit_message_text(
            l10n.format_value(desc_config['message']),
            chat_id=data["chat_id"],
            message_id=data["message_id"],
            reply_markup=keyboard.as_markup()
        )
        
        # Обновляем состояние
        await state.update_data(name=message.text)
        await state.set_state(FailStates.waiting_for_description)
        
        # Удаляем сообщение пользователя
        await message.delete()

    except Exception as e:
        logging.error(f"Ошибка в process_fail_name: {e}")
        await message.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
        )
        await state.clear()

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

    # Получаем конфигурацию
    desc_config = menu_manager.get_state_config('fail_creation.states.description')
    action_config = menu_manager.get_state_config('fail_creation.states.action')

    # Проверяем сохраненные данные
    data = await state.get_data()
    if not data.get("message_id") or not data.get("chat_id"):
        await message.answer(
            l10n.format_value("error-missing-data"),
            show_alert=True
        )
        await state.clear()
        return
    
    # Валидация длины описания
    if len(message.text) > desc_config['validation']['max_length']:
        await message.answer(
            l10n.format_value(desc_config['validation']['error']),
            show_alert=True
        )
        return
    
    try:
        # Сохраняем описание
        await state.update_data(description=message.text)
        
        # Получаем клавиатуру для действий
        keyboard = menu_manager.get_keyboard('fail_creation.states.action')
        
        # Обновляем сообщение с кнопками действий
        await message.bot.edit_message_text(
            l10n.format_value(action_config['message']),
            chat_id=data["chat_id"],
            message_id=data["message_id"],
            reply_markup=keyboard.as_markup()
        )
        
        # Устанавливаем следующее состояние
        await state.set_state(FailStates.waiting_for_action)
        
        # Удаляем сообщение пользователя
        await message.delete()
        
    except Exception as e:
        logging.error(f"Error in process_description: {e}")
        await message.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
        )
        await state.clear()

@router.callback_query(F.data == "publish_fail")
async def publish_fail(
    callback: CallbackQuery, 
    state: FSMContext, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Публикация фейла (отправка на проверку перед публикацией).
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """

    config = menu_manager.get_state_config('fail_creation.callbacks.publish')

    try:
        user = await check_user(callback.from_user.id, callback, session, l10n)
        if not user:
            return
            
        data = await state.get_data()
        fail_service = FailService(session)
        
        await fail_service.create_fail(
            user_id=user.id,
            name=data["name"],
            description=data["description"],
            status=FailStatus[config["status"]]
        )
        
        await callback.message.edit_text(
            l10n.format_value(config["message"])
        )
        await state.clear()
        
    except Exception as e:
        logging.error(f"Ошибка в publish_fail: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
        )

@router.callback_query(F.data == "save_draft")
async def save_draft(
    callback: CallbackQuery, 
    state: FSMContext, 
    session: AsyncSession, 
    l10n: FluentLocalization
):
    """
    Сохранение фейла как черновика.
    
    Attributes:
        callback (CallbackQuery): Запрос обратного вызова от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
        l10n (FluentLocalization): Объект локализации.
    """
    
    config = menu_manager.get_state_config('fail_creation.callbacks.draft')
    
    try:
        user = await check_user(callback.from_user.id, callback, session, l10n)
        if not user:
            return
            
        data = await state.get_data()
        fail_service = FailService(session)
        
        await fail_service.create_fail(
            user_id=user.id,
            name=data["name"],
            description=data["description"], 
            status=FailStatus[config["status"]]
        )
        
        await callback.message.delete()
        await callback.answer(
            l10n.format_value(config["message"]),
            show_alert=config["popup"]
        )
        await state.clear()
        
    except Exception as e:
        logging.error(f"Error in save_draft: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
        )

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

    try:
        # Проверяем пользователя
        user = await check_user(message.from_user.id, message, session, l10n)
        if not user:
            return

        # Получаем черновики
        fail_service = FailService(session)
        drafts = await fail_service.get_user_drafts(user.id)

        if not drafts:
            await message.answer(
                l10n.format_value(config["empty"]),
                show_alert=True
            )
            await message.delete()
            return

        # Создаем клавиатуру из черновиков
        keyboard = menu_manager.build_dynamic_keyboard(
            'drafts',
            drafts
        )

        # Отправляем сообщение со списком
        await message.answer(
            l10n.format_value(config["list"]),
            reply_markup=keyboard.as_markup()
        )
        await message.delete()

    except Exception as e:
        logging.error(f"Ошибка в show_drafts: {e}")
        await message.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
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
    
    try:
        # Получаем конфигурацию
        config = menu_manager.get_state_config('draft_management')
        
        # Извлекаем ID черновика
        draft_id = int(callback.data.split(":")[1])
        
        keyboard = menu_manager.get_id_keyboard(
            'draft_management',
            draft_id
        )
        
        await callback.message.edit_text(
            l10n.format_value(config["message"]),
            reply_markup=keyboard.as_markup()
        )
        
    except Exception as e:
        logging.error(f"Ошибка в manage_draft: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
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
    try:
        # Получаем конфигурацию
        config = menu_manager.get_state_config('draft_publishing.messages')
        
        # Извлекаем ID черновика
        draft_id = int(callback.data.split(":")[1])
        
        # Проверяем пользователя
        user = await check_user(callback.from_user.id, callback, session, l10n)
        if not user:
            return
            
        # Публикуем черновик
        fail_service = FailService(session)
        if await fail_service.publish_draft(draft_id, user.id):
            await callback.message.edit_text(
                l10n.format_value(config["success"])
            )
        else:
            await callback.answer(
                l10n.format_value(config["error"]),
                show_alert=True
            )
            
    except ValueError:
        logging.error(f"Invalid draft_id in callback data: {callback.data}")
        await callback.answer(
            l10n.format_value("error-invalid-id"),
            show_alert=True
        )
    except Exception as e:
        logging.error(f"Error publishing draft: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
        )
        

@router.callback_query(F.data.startswith("edit_draft:"))
async def start_edit_draft(callback: CallbackQuery, state: FSMContext, l10n: FluentLocalization):
    try:
        config = menu_manager.get_state_config('draft_editing.states.name')
        keyboard = menu_manager.get_keyboard('draft_editing')
        
        draft_id = int(callback.data.split(":")[1])
        await state.update_data(draft_id=draft_id)
        await state.set_state(FailStates.editing_name)
        
        await callback.message.edit_text(
            l10n.format_value(config["message"]),
            reply_markup=keyboard.as_markup()
        )
        
    except Exception as e:
        logging.error(f"Error starting draft edit: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
        )

@router.message(FailStates.editing_name)
async def edit_draft_name(message: Message, state: FSMContext, l10n: FluentLocalization):
    config = menu_manager.get_state_config('draft_editing.states.name')
    desc_config = menu_manager.get_state_config('draft_editing.states.description')
    
    if len(message.text) > config["validation"]["max_length"]:
        await message.answer(
            l10n.format_value(config["validation"]["error"]),
            show_alert=True
        )
        return
        
    await state.update_data(new_name=message.text)
    await state.set_state(FailStates.editing_description)
    
    await message.answer(l10n.format_value(desc_config["message"]))
    await message.delete()

@router.message(FailStates.editing_description)
async def edit_draft_description(message: Message, state: FSMContext, session: AsyncSession, l10n: FluentLocalization):
    try:
        config = menu_manager.get_state_config('draft_editing')
        
        if len(message.text) > config["states"]["description"]["validation"]["max_length"]:
            await message.answer(
                l10n.format_value(config["states"]["description"]["validation"]["error"]),
                show_alert=True
            )
            return
            
        data = await state.get_data()
        fail_service = FailService(session)
        
        if await fail_service.update_draft(
            data["draft_id"], 
            data["new_name"], 
            message.text
        ):
            await message.answer(
                l10n.format_value(config["messages"]["success"])
            )
        else:
            await message.answer(
                l10n.format_value(config["messages"]["error"])
            )
            
        await state.clear()
        await message.delete()
        
    except Exception as e:
        logging.error(f"Error updating draft: {e}")
        await message.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
        )
        await state.clear()

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
    try:
        fail_id = int(callback.data.split(":")[1])
        config = menu_manager.get_state_config('fail_deletion.confirm')
        
        # Создаем клавиатуру с привязкой к ID
        keyboard = menu_manager.get_id_keyboard(
            'fail_deletion.confirm',
            fail_id
        )
        
        await callback.message.edit_text(
            l10n.format_value(config["message"]),
            reply_markup=keyboard.as_markup()
        )
        
    except Exception as e:
        logging.error(f"Error in confirm_delete: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
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
    try:
        fail_id = int(callback.data.split(":")[1])
        config = menu_manager.get_state_config('fail_deletion.messages')
        
        user = await check_user(callback.from_user.id, callback, session, l10n)
        if not user:
            return

        fail_service = FailService(session)
        if await fail_service.delete_fail(fail_id, user.id):
            # Показываем всплывающее уведомление
            await callback.answer(
                l10n.format_value(config["success"]),
                show_alert=True
            )
            # Удаляем сообщение с кнопками
            await callback.message.delete()
        else:
            await callback.answer(
                l10n.format_value(config["error"]),
                show_alert=True
            )
            
    except Exception as e:
        logging.error(f"Error deleting fail: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
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

    try:
        config = menu_manager.get_state_config('drafts.messages')
        
        # Проверяем пользователя
        user = await check_user(callback.from_user.id, callback, session, l10n)
        if not user:
            return
            
        # Получаем черновики
        fail_service = FailService(session)
        drafts = await fail_service.get_user_drafts(user.id)
        
        # Если черновиков нет
        if not drafts:
            await callback.message.delete()
            await callback.answer(
                l10n.format_value(config["empty"]),
                show_alert=True
            )
            return
            
        # Создаем клавиатуру из черновиков
        keyboard = menu_manager.build_dynamic_keyboard(
            'drafts',
            drafts
        )
        
        # Обновляем сообщение
        await callback.message.edit_text(
            l10n.format_value(config["list"]),
            reply_markup=keyboard.as_markup()
        )
        
    except Exception as e:
        logging.error(f"Error in back_to_drafts: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
        )

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
    try:
        config = menu_manager.get_state_config('top_losers')
        
        # Получаем топ пользователей
        fail_service = FailService(session)
        top_users = await fail_service.get_top_losers(config["limit"])
        
        if not top_users:
            await message.answer(
                l10n.format_value(config["messages"]["empty"])
            )
            await message.delete()
            return
            
        # Формируем текст
        text = l10n.format_value(config["messages"]["caption"]) + "\n\n"
        
        for i, (user, total_rating) in enumerate(top_users, 1):
            text += l10n.format_value(
                config["messages"]["item"],
                {
                    "index": i,
                    "user_name": user.username,
                    "total_rating": total_rating
                }
            ) + "\n"
            
        await message.answer(text)
        await message.delete()
        
    except Exception as e:
        logging.error(f"Error showing top losers: {e}")
        await message.answer(
            l10n.format_value("error-try-again")
        )

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
    try:
        config = menu_manager.get_state_config('voting')
        
        # Получаем фейлы
        fail_service = FailService(session)
        fails = await fail_service.get_fails_for_voting(config["limit"])
        
        if not fails:
            await message.answer(
                l10n.format_value(config["messages"]["empty"])
            )
            await message.delete()
            return
            
        # Создаем клавиатуру
        keyboard = menu_manager.build_dynamic_keyboard(
            'voting',
            fails
        )
        
        await message.answer(
            l10n.format_value(config["messages"]["choose"]),
            reply_markup=keyboard.as_markup()
        )
        await message.delete()
        
    except Exception as e:
        logging.error(f"Error showing fails for voting: {e}")
        await message.answer(
            l10n.format_value("error-try-again")
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
    try:
        config = menu_manager.get_state_config('fail_reading')
        fail_id = int(callback.data.split(":")[1])
        
        # Проверяем существование фейла
        fail = await check_fail(fail_id, session, callback, l10n)
        if not fail or not fail.user:
            return
            
        # Создаем клавиатуру для голосования
        builder = InlineKeyboardBuilder()
        for button in config["keyboard"]["buttons"]:
            builder.button(
                text=l10n.format_value(button["text"]),
                callback_data=f"vote:{fail.id}:{button['rating']}"
            )
            
        # Отображаем информацию
        await callback.message.edit_text(
            l10n.format_value(
                config["messages"]["info"],
                {
                    "user_name": fail.user.username,
                    "fail_name": fail.name,
                    "fail_description": fail.description,
                    "fail_rating": fail.rating
                }
            ),
            reply_markup=builder.as_markup()
        )
        
    except Exception as e:
        logging.error(f"Error reading fail: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
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
    try:
        config = menu_manager.get_state_config('voting.messages')
        _, fail_id, rating = callback.data.split(":")
        
        user = await check_user(callback.from_user.id, callback, session, l10n)
        if not user:
            return
            
        fail_service = FailService(session)
        if await fail_service.update_rating(int(fail_id), user.id, int(rating)):
            await callback.message.edit_text(
                l10n.format_value(config["success"])
            )
        else:
            await callback.answer(
                l10n.format_value(config["already"]),
                show_alert=True
            )
            
    except Exception as e:
        logging.error(f"Error voting for fail: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
        )
    
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
    try:
        config = menu_manager.get_state_config('user_fails')
        
        # Проверяем пользователя
        user = await check_user(message.from_user.id, message, session, l10n)
        if not user:
            return
            
        # Получаем фейлы
        fail_service = FailService(session)
        fails = await fail_service.get_user_fails(user.id)
        
        if not fails:
            await message.answer(
                l10n.format_value(config["messages"]["empty"])
            )
            await message.delete()
            return
            
        # Создаем клавиатуру
        keyboard = menu_manager.build_dynamic_keyboard(
            'user_fails',
            fails
        )
        
        await message.answer(
            l10n.format_value(config["messages"]["choose"]),
            reply_markup=keyboard.as_markup()
        )
        await message.delete()
        
    except Exception as e:
        logging.error(f"Error showing user fails: {e}")
        await message.answer(
            l10n.format_value("error-try-again")
        )

@router.callback_query(F.data.startswith("manage_public:"))
async def manage_public_fail(callback: CallbackQuery, session: AsyncSession, l10n: FluentLocalization):
    try:
        fail_id = int(callback.data.split(":")[1])
        config = menu_manager.get_state_config('public_fail.management')
        
        keyboard = menu_manager.get_id_keyboard(
            'public_fail.management',
            fail_id
        )
        
        await callback.message.edit_text(
            l10n.format_value(config["message"]),
            reply_markup=keyboard.as_markup()
        )
        
    except Exception as e:
        logging.error(f"Ошибка в manage_public_fail: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
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
    try:
        fail_id = int(callback.data.split(":")[1])
        config = menu_manager.get_state_config('public_fail.messages')
        
        fail_service = FailService(session)
        await fail_service.to_draft(fail_id)
        
        await callback.message.edit_text(
            l10n.format_value(config["to_draft"])
        )
        
    except Exception as e:
        logging.error(f"Ошибка в to_draft: {e}")
        await callback.answer(
            l10n.format_value("error-try-again"),
            show_alert=True
        )
    
@router.message(StateFilter(FailStates), Command("start", "help", "top", "vote", "fail"))
async def cancel_fail_creation(message: Message, state: FSMContext):
    """
    Отменяет создание фейла при получении другой команды
    
    Attributes:
        message (Message): Сообщение от пользователя.
        state (FSMContext): Контекст состояния для управления состоянием.
    """
    try:
        await state.clear()
        await message.forward(message.chat.id)
        
    except Exception as e:
        logging.error(f"Ошибка в cancel_fail_creation: {e}")

@router.callback_query(F.data == "cancel_fail")
async def cancel_fail(
    callback: CallbackQuery,
    state: FSMContext,
    l10n: FluentLocalization
):
    """Отмена создания фейла"""
    try:
        config = menu_manager.get_state_config('cancellation.fail_creation')
        await state.clear()
        await callback.message.delete()
        await callback.answer(
            l10n.format_value(config["message"]),
            show_alert=config["show_alert"]
        )
    except Exception as e:
        logging.error(f"Ошибка отмены создания: {e}")

@router.callback_query(F.data == "cancel_delete")
async def cancel_delete(
    callback: CallbackQuery,
    l10n: FluentLocalization
):
    """Отмена удаления фейла"""
    try:
        config = menu_manager.get_state_config('cancellation.fail_deletion')
        await callback.message.delete()
        await callback.answer(
            l10n.format_value(config["message"]),
            show_alert=config["show_alert"]
        )
    except Exception as e:
        logging.error(f"Ошибка отмены удаления: {e}")