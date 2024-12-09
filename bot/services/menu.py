from typing import Dict, Any
import json
from aiogram.utils.keyboard import InlineKeyboardBuilder

class MenuManager:
    def __init__(self, config_path: str = 'bot/config/menu.json'):
        with open(config_path) as f:
            self.config = json.load(f)
    
    def get_keyboard(self, menu_path: str) -> InlineKeyboardBuilder:
        """Создает клавиатуру из конфигурации"""
        config = self.config
        for key in menu_path.split('.'):
            config = config[key]
            
        builder = InlineKeyboardBuilder()
        for button in config['keyboard']['buttons']:
            builder.button(
                text=button['text'],
                callback_data=button['callback']
            )
        return builder
    
    def get_state_config(self, menu_path: str) -> Dict[str, Any]:
        """Получает конфигурацию состояния"""
        config = self.config
        for key in menu_path.split('.'):
            config = config[key]
        return config

    def build_dynamic_keyboard(
        self, 
        menu_path: str, 
        items: list,
        text_field: str = "name"
    ) -> InlineKeyboardBuilder:
        """
        Создает клавиатуру из списка объектов
        
            Создает кнопки из списка объектов (например, список черновиков)
            Использует атрибуты объектов для текста кнопок
            Один формат callback для всех кнопок
            Подходит для списков: /drafts, /vote, /publics

        Attributes:
            menu_path (str): Путь к конфигурации меню.
            items (list): Список объектов для отображения.
            text_field (str, optional): Поле объекта для отображения. По умолчанию "name".

        Returns:
            InlineKeyboardBuilder: Клавиатура с кнопками для каждого объекта.

        Usage: 
            menu_manager = MenuManager()
            items = [Item(id=1, name="Item 1"), Item(id=2, name="Item 2")]
            keyboard = menu_manager.build_dynamic_keyboard("menu.path", items)
            await bot.send_message(chat_id, "Select an item:", reply_markup=keyboard.as_markup())
        """
        config = self.get_state_config(f"{menu_path}.keyboard")

        builder = InlineKeyboardBuilder()
        for item in items:
            builder.button(
                text=getattr(item, text_field),
                callback_data=f"{config['callback_prefix']}:{item.id}"
            )

        if config.get("adjust"):
            builder.adjust(config["adjust"])

        return builder

    def get_id_keyboard(
        self, 
        menu_path: str,
        item_id: int
    ) -> InlineKeyboardBuilder:
        """
        Создаёт клавиатуру с привязкой к ID
            Создает фиксированный набор разных кнопок для одного объекта
            Кнопки берутся из конфигурации
            Разные callback'и для разных действий
            Подходит для меню управления: "Опубликовать", "Редактировать", "Удалить"
        Attributes:
            menu_path (str): Путь к конфигурации меню.
            item_id (int): ID объекта для привязки.

        Returns:
            InlineKeyboardBuilder: Клавиатура с кнопками для привязки к ID.

        Usage:
            menu_manager = MenuManager()
            keyboard = menu_manager.get_id_keyboard("menu.path", 123)
            await bot.send_message(chat_id, "Select an option:", reply_markup=keyboard.as_markup())
        """
        config = self.get_state_config(f"{menu_path}.keyboard")
        builder = InlineKeyboardBuilder()

        for button in config["buttons"]:
            callback = f"{button['callback']}:{item_id}" if ":" not in button["callback"] else button["callback"]
            builder.button(text=button["text"], callback_data=callback)

        return builder