import logging
from os import getenv
from sys import exit
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import KeyboardButton
import asyncio

# если настройки не импортируются по подсказкам (alt+enter) сделай pip install aiogram

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)
logging.basicConfig(level=logging.INFO)



class Form(StatesGroup):
    some_state = State()  # start
    # another_state = State() # add more states to make more logic


# @router.message(state='*', commands='cancel') # state='*' for any current state
@router.message(Command('cancel', ignore_case=True)) # state='*' for any current state
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear() # reset the state to default
    await message.answer('ОК')


@router.message(lambda message: message.text == 'Start')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Form.some_state) # this thing is to make bot process the block with (state=Form.name_s) next
    await message.answer('Enter your name:')


@router.message(Form.some_state) # this block will be processed after 'cmd_start'
async def process_name(message: types.Message, state: FSMContext):
    await state.clear()

    buttons = [[KeyboardButton(text='Finish'), KeyboardButton(text='Do Nothing')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer(f"Hello, {message.text}", reply_markup=keyboard)


@router.message(lambda message: message.text == 'Finish') # some logic foe finish button
async def cmd_start(message: types.Message):
    buttons = [[KeyboardButton(text='Start'), KeyboardButton(text='/cancel')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Okay", reply_markup=keyboard)


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))

