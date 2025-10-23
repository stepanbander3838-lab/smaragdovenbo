from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio

# Твой токен
TOKEN = "8498688133:AAF_lcJSAsiN2Hyo2N3k_SVGoQOg6pTKuII"

# Твой Telegram ID — сюда нужно вставить свой ID, чтобы получать все сообщения
ADMIN_ID = 8371142950  # <-- замени на свой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить номер телефона", request_contact=True),
            KeyboardButton(text="Отправить местоположение", request_location=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет! Отправь свой номер телефона или местоположение, " 
        "или просто напиши сообщение.", 
        reply_markup=keyboard
    )

# Команда /info
@dp.message(Command("info"))
async def info_handler(message: Message):
    await message.answer("Что именно вас интересует?")

# Обработка контакта
@dp.message(lambda message: message.contact is not None)
async def contact_handler(message: Message):
    contact = message.contact.phone_number
    await message.answer(f"Спасибо! Ваш номер телефона: {contact}")
    # Пересылаем админу
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Контакт от {message.from_user.full_name} (@{message.from_user.username}): {contact}"
    )

# Обработка местоположения
@dp.message(lambda message: message.location is not None)
async def location_handler(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    await message.answer(f"Спасибо! Ваша геолокация:\nШирота: {latitude}\nДолгота: {longitude}")
    # Пересылаем админу
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Местоположение от {message.from_user.full_name} (@{message.from_user.username}): "
             f"Широта {latitude}, Долгота {longitude}"
    )

# Перехватываем все остальные текстовые сообщения
@dp.message(lambda message: message.text is not None)
async def forward_to_admin(message: Message):
    # Пересылаем админу
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Сообщение от {message.from_user.full_name} (@{message.from_user.username}):\n{message.text}"
    )
    await message.answer("Спасибо! Ваше сообщение отправлено админу.")

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

