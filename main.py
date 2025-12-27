import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, DB_PATH, CHECK_INTERVAL_SECONDS, DATETIME_FORMAT
from db import (
    init_db,
    add_reminder,
    get_due_reminders,
    get_active_reminders,
    mark_done,
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "Привіт! Я бот-нагадувач.\n\n"
        "Щоб створити нагадування, надішли команду у форматі:\n"
        "/add YYYY-MM-DD HH:MM текст\n\n"
        "Наприклад:\n"
        "/add 2025-12-28 15:00 подзвонити клієнту\n\n"
        "Подивитися список активних нагадувань: /list"
    )
    await message.answer(text)

@dp.message(Command("add"))
async def cmd_add(message: Message):
    full_text = message.text or ""
    parts = full_text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "Потрібні аргументи. Формат:\n"
            "/add YYYY-MM-DD HH:MM текст"
        )
        return

    payload = parts[1].strip()

    if len(payload) < 17:
        await message.answer(
            "Невірний формат. Приклад:\n"
            "/add 2025-12-28 15:00 подзвонити клієнту"
        )
        return

    datetime_str = payload[:16]
    text = payload[16:].strip()

    if not text:
        await message.answer(
            "Не знайдений текст нагадування. Приклад:\n"
            "/add 2025-12-28 15:00 подзвонити клієнту"
        )
        return

    try:
        dt = datetime.strptime(datetime_str, DATETIME_FORMAT)
    except ValueError:
        await message.answer(
            "Невірний формат дати/часу. Очікується:\n"
            "YYYY-MM-DD HH:MM\n"
            "Наприклад:\n"
            "/add 2025-12-28 15:00 подзвонити клієнту"
        )
        return

    add_reminder(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        remind_at=dt.strftime(DATETIME_FORMAT),
        text=text,
        db_path=DB_PATH,
    )

    await message.answer(
        f"Ок, нагадаю {dt.strftime(DATETIME_FORMAT)}:\n{text}"
    )

@dp.message(Command("list"))
async def cmd_list(message: Message):
    reminders = get_active_reminders(
        user_id=message.from_user.id,
        db_path=DB_PATH,
    )

    if not reminders:
        await message.answer("У вас немає активних нагадувань.")
        return

    lines = []
    for idx, (rem_id, remind_at, text) in enumerate(reminders, start=1):
        lines.append(f"{idx}) {remind_at} — {text} (id={rem_id})")

    await message.answer("\n".join(lines))


async def check_reminders():
    now_str = datetime.now().strftime(DATETIME_FORMAT)
    rows = get_due_reminders(now_str, db_path=DB_PATH)

    for rem_id, user_id, chat_id, remind_at, text in rows:
        try:
            await bot.send_message(chat_id, f"Нагадування:\n{text}")
        except Exception:
            pass
        finally:
            mark_done(rem_id, db_path=DB_PATH)


async def main():
    init_db(DB_PATH)

    scheduler.add_job(check_reminders, "interval", seconds=CHECK_INTERVAL_SECONDS)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
