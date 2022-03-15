from mainbot import *


async def register_handlers_food(dp: Dispatcher):
    dp.register_message_handler(find_game, commands="find", state="*")
    dp.register_message_handler(finder, state=fs.wait_game)
