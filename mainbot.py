from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from config import bottoken, findgame
from config.service.service import FindState as fs
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text


bot = Bot(token=bottoken.token)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Hello, i can help find game!\nEnter /find', reply=False)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply('У меня безграничные возможности', reply=False)


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Cancelled.', reply=False)


@dp.message_handler(state="*", commands=['find'])
async def find_game(message: types.Message, state: FSMContext):
    await message.answer(" Enter game name\nOr enter /cancel for cancel", reply=False)
    await fs.wait_game.set()


@dp.message_handler(state=fs.wait_game)
async def finder(message: types.ContentType, state: FSMContext):
    game_text = message.text
    await message.reply(findgame.main(text=game_text))
    # user_data = await state.get_data()
    await state.finish()


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
