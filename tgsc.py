import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio

API_TOKEN = '7425457401:AAHgnJ1kGdeTm-XvrTLvfTnQnd5Wumi7zl0'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Подключение к базе данных
conn = sqlite3.connect('school_data.db')
cursor = conn.cursor()

# Создание таблицы students, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    grade TEXT NOT NULL
                )''')
conn.commit()

# Словарь для хранения временных данных пользователя
user_data = {}


# Команда /start
@dp.message(CommandStart())
async def send_welcome(message: Message):
    await message.reply("Добро пожаловать! Пожалуйста, введите ваше имя:")


# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    user_info = user_data[user_id]

    if 'name' not in user_info:
        user_info['name'] = message.text
        await message.reply("Введите ваш возраст:")
    elif 'age' not in user_info:
        try:
            user_info['age'] = int(message.text)
            await message.reply("Введите ваш класс:")
        except ValueError:
            await message.reply("Пожалуйста, введите корректное число для возраста.")
    elif 'grade' not in user_info:
        user_info['grade'] = message.text

        # Сохранение данных в базу данных
        cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
                       (user_info['name'], user_info['age'], user_info['grade']))
        conn.commit()

        await message.reply("Спасибо! Ваши данные сохранены.")

        # Очистка данных пользователя
        user_data.pop(user_id)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main()
)