from __future__ import annotations

import asyncio
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from telegram_lead_bot.core import Lead, LeadStore, normalize_phone


class LeadForm(StatesGroup):
    name = State()
    phone = State()
    comment = State()


store = LeadStore(Path("leads.db"))
dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(LeadForm.name)
    await message.answer("Здравствуйте! Как вас зовут?")


@dispatcher.message(LeadForm.name, F.text)
async def name_received(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text.strip())
    await state.set_state(LeadForm.phone)
    await message.answer("Укажите телефон для связи.")


@dispatcher.message(LeadForm.phone, F.text)
async def phone_received(message: Message, state: FSMContext) -> None:
    try:
        phone = normalize_phone(message.text)
    except ValueError:
        await message.answer("Не удалось распознать телефон. Пример: +7 900 123-45-67")
        return
    await state.update_data(phone=phone)
    await state.set_state(LeadForm.comment)
    await message.answer("Кратко опишите задачу.")


@dispatcher.message(LeadForm.comment, F.text)
async def comment_received(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lead = Lead(
        telegram_user_id=message.from_user.id,
        name=data["name"],
        phone=data["phone"],
        comment=message.text,
    )
    store.add(lead)
    await state.clear()
    await message.answer("Спасибо! Заявка сохранена.")


async def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")
    store.initialize()
    await dispatcher.start_polling(Bot(token=token))


if __name__ == "__main__":
    asyncio.run(main())

