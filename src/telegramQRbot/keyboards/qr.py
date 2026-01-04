def build_qr_keyboard():
    # Telegram reply_markup в формате dict
    return {
        "inline_keyboard": [
            [{"text": "Создать ещё", "callback_data": "create_qr"}],
            [{"text": "Отблагодарить автора бота", "callback_data": "gift_creator"}],
            [{"text": "Вернуться в меню", "callback_data": "/menu"}],
        ]
    }
