import logging
import gsheets as gs
from aiogram import Bot, Dispatcher, executor, types
from secret import TG_TOKEN
from aiogram.types import ReplyKeyboardMarkup
from keyboard import markup

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)



# 108571458 dima
# 286991194 dasha

def auth(func):
    async def wrapper(message):
        if message['from']['id'] not in (108571458, 286991194):
            return await message.reply('Access Denied', reply=False)
        return await func(message)

    return wrapper


@dp.message_handler(lambda message: message.text and message.text == '!!')
async def get_text(message: types.Message):
    info = gs.get_plan_fact()
    PLAN = 0
    BALANCE = 1
    gs_info = []
    for plan, bal in zip(info[PLAN], info[BALANCE]):
        gs_info.append(plan + bal)

    table = """"""
    for row in gs_info:
        table += ' | '.join(row) + '\n'

    await message.answer(text=table)


@dp.message_handler(lambda message: message.text and message.text.startswith('*'))
async def get_text(message: types.Message):
    print(message.text)
    print(waiting_msg_id)
    category_name = message.text.replace('*', '')
    gs.add_chosen_category(category_name, waiting_msg_id)
    gs.insert_category_alias(category_name, waiting_text)


@dp.message_handler(lambda message: message.text and message.text.split()[0].replace('+', '').isdigit())
@auth
async def get_text(message: types.Message):
    msg_id, date, author = message.message_id, message.date, message.from_user.full_name
    msg = message.text.split()
    value, text = msg[0], msg[1:]

    # Узнаем категорию
    category = gs.find_category_msg(text)
    if category is None:
        global waiting_msg_id
        global waiting_text
        waiting_msg_id = message.message_id
        waiting_text = text
        await message.reply("Выбери категорию", reply_markup=markup)

    state = 'cost'
    print(msg_id, value, text, date, author, category, state)
    if value.startswith('+'):
        value = value.replace('+', '')
        state = 'income'
    if value.isdigit():
        gs.append_row_gsheets(msg_id, int(value), text, category, state, date, author)


@dp.edited_message_handler()
async def replace_row_in_gsheet(message: types.Message):
    msg_id, date, author = message.message_id, message.date, message.from_user.full_name
    msg = message.text.split()
    value, text = msg[0], msg[1:]
    category, state = gs.get_state_category(msg_id)
    cell_row = gs.get_cell_row(msg_id)
    gs.delete_row_gsheets(msg_id)
    gs.update_row_gsheets(cell_row, msg_id, value, text, category, state, date, author)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
