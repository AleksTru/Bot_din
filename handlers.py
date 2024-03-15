import datetime
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import html
from db import create_dinner, create_lanch, delete_din_lanch, on_dinner_lanch

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    
    kb = [
        [types.KeyboardButton(text="Обед", callback_query="dinner"), types.KeyboardButton(text="Личные потребности", callback_query="вернулся")],
        [types.KeyboardButton(text="Вернулся", callback_query="comeback")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите действие")
    await message.answer("Давайте отдыхать разумно", reply_markup=keyboard)

@router.message(F.text.lower() == "обед")
async def obed(message: types.Message):
    curent_time = datetime.datetime.now()

    user_id = message.from_user.id
    name = html.quote(message.from_user.full_name)
    starttime = curent_time.strftime('%H:%M:%S')
    dinner = 1
    lanch = 0
    await create_dinner(user_id, name, dinner, lanch, starttime)

    text_fin = f'{on_dinner_lanch()}'
    await message.answer(f'{text_fin}')
    
@router.message(F.text.lower() == "личные потребности")
async def coffee_break(message: types.Message):
    curent_time = datetime.datetime.now()    
    user_id = message.from_user.id
    name = html.quote(message.from_user.full_name)
    starttime = curent_time.strftime('%H:%M:%S')
    dinner = 0
    lanch = 1
    await create_lanch(user_id, name, dinner, lanch, starttime)
        
    text_fin = f'{on_dinner_lanch()}'
    await message.answer(f'{text_fin}')


@router.message(F.text.lower() == "вернулся")
async def back_to_zal(message: types.Message):
    user_id = message.from_user.id
    await delete_din_lanch(user_id)
    text_fin = f'{on_dinner_lanch()}'
    await message.answer(f'{text_fin}')


    