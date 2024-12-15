import json
from fluent.runtime import FluentLocalization
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

class MenuManager:
    def __init__(self, menu_path: str = 'backend/bot/keyboards/menu.json'):
        with open(
            file=menu_path,
            mode='r',
            encoding='utf-8'
        ) as f:
            self.menu = json.load(f)
    
    def get_menu_text(self, menu_id: str, l10n: FluentLocalization) -> str:
        """Получает локализованный текст меню из конфигурации"""
        menu_item = self.menu.get(menu_id)
        if not menu_item:
            raise ValueError(l10n.format_value("err-menu-not-found", { "menu_id": menu_id } ))
            
        return l10n.format_value(menu_item['label'])
    
    def get_keyboard(self, menu_id: str, l10n: FluentLocalization) -> InlineKeyboardBuilder:
        menu_item = self.menu.get(menu_id)
        if not menu_item:
            raise ValueError(l10n.format_value("err-menu-not-found", { "menu_id": menu_id } ))
            
        builder = InlineKeyboardBuilder()
        
        for button in menu_item['buttons']:
            kwargs = {
                "text": l10n.format_value(button['label']),
                "callback_data": button.get('callback_data')
            }
            
            if "web_app" in button:
                kwargs["web_app"] = WebAppInfo(url=button["web_app"])
            if "url" in button:
                kwargs["url"] = button["url"]
                
            builder.button(**kwargs)
            
        builder.adjust(1)
        return builder