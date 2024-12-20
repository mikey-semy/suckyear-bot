from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from fluent.runtime import FluentLocalization
from bot.keyboards.menu import MenuManager

router = Router()
menu_manager = MenuManager()

@router.message(Command("help"))
async def cmd_help(message: Message, l10n: FluentLocalization):
    """
    Обработчик команды /help.
    Отправляет справочную информацию пользователю.
    Выводит клавиатуру меню.
    
    Args:
        message (Message): Сообщение пользователя.
        l10n (FluentLocalization): Локализация.

    """
    keyboard = menu_manager.get_keyboard("help_menu", l10n)
    text = menu_manager.get_menu_text("help_menu", l10n)
    await message.answer(text, reply_markup=keyboard.as_markup())
    
@router.callback_query(lambda c: c.data == "menu_help")
async def callback_help(callback_query: CallbackQuery, l10n: FluentLocalization):
    """
    Обработчик нажатия на кнопку "Help" в меню.
    Отправляет справочную информацию пользователю.
    Выводит клавиатуру меню.
    
    Args:
        callback_query (types.CallbackQuery): Запрос обратного вызова.
        l10n (FluentLocalization): Локализация.
    """
    keyboard = menu_manager.get_keyboard("help_menu", l10n)
    text = menu_manager.get_menu_text("help_menu", l10n)
    await callback_query.message.edit_text(text, reply_markup=keyboard.as_markup())
    
@router.callback_query(F.data == "help_usage")
async def process_help_usage(callback_query: CallbackQuery, l10n: FluentLocalization):
    """
    Обработчик кнопки "Как использовать".
    Показывает инструкцию по использованию бота.

    Args:
        callback_query (CallbackQuery): Колбэк от нажатия кнопки
        l10n (FluentLocalization): Локализация
    """
    keyboard = menu_manager.get_keyboard("help_menu_usage", l10n)
    text = menu_manager.get_menu_text("help_menu_usage", l10n)
    await callback_query.message.edit_text(text, reply_markup=keyboard.as_markup())

@router.callback_query(F.data == "help_rules")
async def process_help_rules(callback_query: CallbackQuery, l10n: FluentLocalization):
    """
    Обработчик кнопки "Правила".
    Показывает правила использования бота и сервиса.

    Args:
        callback_query (CallbackQuery): Колбэк от нажатия кнопки
        l10n (FluentLocalization): Локализация для текстов
    """
    keyboard = menu_manager.get_keyboard("help_menu_rules", l10n)
    text = menu_manager.get_menu_text("help_menu_rules", l10n)
    await callback_query.message.edit_text(text, reply_markup=keyboard.as_markup())

@router.callback_query(F.data == "menu_main")
async def process_back_to_main(callback_query: CallbackQuery, l10n: FluentLocalization):
    """
    Обработчик кнопки "Назад в главное меню".
    Возвращает пользователя в главное меню.

    Args:
        callback_query (CallbackQuery): Колбэк от нажатия кнопки
        l10n (FluentLocalization): Локализация
    """
    keyboard = menu_manager.get_keyboard("main_menu", l10n)
    text = menu_manager.get_menu_text("main_menu", l10n)
    await callback_query.message.edit_text(text, reply_markup=keyboard.as_markup())
    
@router.callback_query(F.data == "menu_help")
async def process_back_to_help(callback_query: CallbackQuery, l10n: FluentLocalization):
    """
    Обработчик кнопки "Назад в меню помощи".
    Возвращает пользователя в меню помощи.

    Args:
        callback_query (CallbackQuery): Колбэк от нажатия кнопки
        l10n (FluentLocalization): Локализация
    """
    keyboard = menu_manager.get_keyboard("help_menu", l10n)
    text = menu_manager.get_menu_text("help_menu", l10n)
    await callback_query.message.edit_text(text, reply_markup=keyboard.as_markup())