from telebot import types


def registration_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    registration_button = types.KeyboardButton('📝 Register')
    delete_button = types.KeyboardButton('‼️ Delete')
    markup.row(registration_button, delete_button)
    return markup


def cancel_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.KeyboardButton('❌ Cancel')
    markup.add(cancel_button)
    return markup


def phone_number_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.KeyboardButton('❌ Cancel')
    phone_number_button = types.KeyboardButton(' 📲Share Contact', request_contact=True)
    another_new_phone_number_button = types.KeyboardButton('☎️ Another phone number')
    markup.row(phone_number_button, another_new_phone_number_button)
    markup.add(cancel_button)
    return markup

