from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup

def start_kb():
    

    ik = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Send location", request_location=True)]
    ], resize_keyboard=True, one_time_keyboard=True)

    
    return ik

def change_kb():
    
    ikb = InlineKeyboardBuilder()
    ikb.button(text='Изменить', callback_data='change')
    
    return ikb.as_markup()