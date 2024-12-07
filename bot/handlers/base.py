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
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

router = Router()


@router.message(Command("start"))
async def command_start(message: Message, l10n: FluentLocalization):
    """
    Приветственное сообщение от бота пользователю

    :param message: сообщение от пользователя с командой /start
    :param l10n: объект локализации
    """
    await message.answer(l10n.format_value("intro"))


@router.message(Command("help"))
async def command_help(message: Message, l10n: FluentLocalization):
    """
    Справка для пользователя

    :param message: сообщение от пользователя с командой /help
    :param l10n: объект локализации
    """
    await message.answer(l10n.format_value("help"))
