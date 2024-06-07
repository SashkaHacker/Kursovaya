import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from engine import photo_to_text
import os

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(F.photo)
async def photo2text(message: Message):
    photo = message.photo[-1]
    photo_id = photo.file_id

    file_info = await bot.get_file(photo_id)
    file_path = file_info.file_path
    destination = f"photos/{photo_id}.jpg"

    await bot.download_file(file_path, destination)
    text = photo_to_text(f"photos/{photo_id}.jpg")
    if text == '':
        await message.answer('На изображении не найден текст.')
    elif text == RuntimeError:
        await message.answer(
            '''Время ожидания ответа программы превышено, попробуйте отправить фото с меньшим количеством текста.''')
    elif not text:
        await message.answer(
            'Произошла непредвиденная ошибка, попробуйте повторить запрос.')
    else:
        await message.answer(text)


@dp.message(CommandStart())
async def hello_world(message: Message):
    await message.answer("""Привет, я бот для распознавания текста из изображений.\n
    Просто пришлите фото с текстом, а я отправлю вам текст с него!""")


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        '''Если вы столкнулись с непредвиденной ошибкой, сообщите о ней разработчику: @Ssasska''')


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
