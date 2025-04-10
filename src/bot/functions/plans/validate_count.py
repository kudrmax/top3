from aiogram.types import Message

from src.bot.keyboards import none


async def validate_count(message: Message, text: str) -> int | None:
    try:
        count = int(text)
    except ValueError:
        await message.answer(
            'Количество задач – это число, поэтому введите число',
            reply_markup=none()
        )
        return None

    if count < 1:
        await message.answer(
            'Количество задач не может быть меньше 1',
            reply_markup=none()
        )
        return None

    return count
