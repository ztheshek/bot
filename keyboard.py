from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import gsheets as gs

categories = gs.get_categories()
list_buttons = [KeyboardButton('*' + i) for i in gs.get_categories()]

markup = ReplyKeyboardMarkup(one_time_keyboard=True)
for button in list_buttons:
    markup.add(button)




#
#
# # button1 = KeyboardButton('1️⃣')
# # button2 = KeyboardButton('2️⃣')
# # button3 = KeyboardButton('3️⃣')
# #
# # markup3 = ReplyKeyboardMarkup().add(button1).add(button2).add(button3)
# # markup4 = ReplyKeyboardMarkup().row(button1, button2, button3)
# # markup5 = ReplyKeyboardMarkup().row(button1, button2, button3).add(KeyboardButton('Средний ряд'))
# #
# # button4 = KeyboardButton('4️⃣')
# # button5 = KeyboardButton('5️⃣')
# # button6 = KeyboardButton('6️⃣')
# # markup5.row(button4, button5)
# # markup5.insert(button6)
#