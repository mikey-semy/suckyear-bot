"""
Модуль bot.handlers.base содержит обработчики команд для бота, реализованного с использованием библиотеки aiogram.

Этот модуль предоставляет:
1. Обработчик команды /start, который отправляет приветственное сообщение пользователю.
2. Обработчик команды /help, который предоставляет справочную информацию пользователю.

Обработчики:
- command_start: Обрабатывает команду /start и отправляет пользователю приветственное сообщение.
- command_help: Обрабатывает команду /help и отправляет пользователю справочную информацию.
"""
from aiogram import Router
from aiogram.types import Message
from fluent.runtime import FluentLocalization
from backend.bot.keyboards.menu import MenuManager

router = Router()
menu_manager = MenuManager()

@router.message(commands=["start"])
async def cmd_start(message: Message, l10n: FluentLocalization):
    """
    Обработчик команды /start. 
    Отправляет приветственное сообщение пользователю.
    Выводит клавиатуру меню.

    Attributes:
        message (Message): Сообщение пользователя.
        l10n (FluentLocalization): Локализация.

    """
    keyboard = menu_manager.get_keyboard("main_menu", l10n)
    text = menu_manager.get_menu_text("main_menu", l10n)
    await message.answer(text, reply_markup=keyboard.as_markup())