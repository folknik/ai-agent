from typing import Tuple
from aiogram.types import Message


def get_user_data(message: Message, url: str) -> Tuple:
    return (
        message.from_user.id,
        message.chat.id,
        message.from_user.is_bot,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
        message.from_user.is_premium,
        url
    )
