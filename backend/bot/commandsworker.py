"""
Модуль для установки команд бота с использованием библиотеки aiogram.

Этот модуль содержит функцию `set_bot_commands`, которая создает и устанавливает
команды для бота, используя локализацию для описаний команд.

Functions:
- set_bot_commands: Устанавливает команды для бота с их описаниями.
"""
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from fluent.runtime import FluentLocalization

async def set_bot_commands(bot: Bot, l10n: FluentLocalization):
    """
    Устанавливает команды для бота.

    Эта функция создает список команд с их описаниями, используя локализацию,
    и устанавливает их для бота.

    :param bot: Экземпляр бота, для которого устанавливаются команды.
    :param l10n: Объект локализации для получения описаний команд.
    
    Returns:
        None
    """
    commands = [
        BotCommand(command="start", description=l10n.format_value("start-description")),
        BotCommand(command="help", description=l10n.format_value("help-description"))
    ]   
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
