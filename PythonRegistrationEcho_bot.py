import time

import telebot
import buttons
import database

from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()
API_KEY = str(os.getenv('API_KEY'))
bot = telebot.TeleBot(API_KEY)

trash_messages = []

# Dictionary to store user data during registration
user_data = {}


# Command handler for '/start'
@bot.message_handler(commands=['start'])
def start_bot(message):
    user_id = message.from_user.id
    bot.send_message(user_id, f'Hi, {message.from_user.first_name}'
                              f'\n\nDo you want to register new staff member, sir ?',
                     reply_markup=buttons.registration_buttons())
    bot.register_next_step_handler(message, register_first_name)


# Function to delete unnecessary messages from chat (clean UI)
def clear_trash_messages(message):
    user_id = message.from_user.id
    if len(trash_messages) > 0:
        for i in trash_messages:
            bot.delete_message(user_id, i)
        trash_messages.clear()
    return trash_messages


# Function to handle first step of registration (choosing Register or Delete)
def register_first_name(message):
    user_id = message.from_user.id
    if message.text == '📝 Register':
        bot.send_message(user_id, '💬 Please type in First Name 💬', reply_markup=buttons.cancel_buttons())
        bot.register_next_step_handler(message, register_last_name)
    elif message.text == '‼️ Delete':
        bot.send_message(user_id, '💬 Please type in staff unique id 💬', reply_markup=buttons.cancel_buttons())
        bot.register_next_step_handler(message, delete_staff)
    else:
        user_trash_response = message.message_id
        trash_messages.append(user_trash_response)
        bot_trash_response = bot.send_message(user_id, '⬇️ Please register new staff member by using button below ⬇️ ')
        trash_messages.append(bot_trash_response)
        bot.register_next_step_handler(message, register_first_name)


# Function to handle second step of registration (last name)
def register_last_name(message):
    user_id = message.from_user.id
    user_text = message.text
    if user_text == '❌ Cancel':
        bot.send_message(user_id, '‼️ Registration is canceled ‼️\n\n',
                         reply_markup=buttons.registration_buttons())
        clear_trash_messages(message)
        bot.register_next_step_handler(message, register_first_name)

    else:
        if user_text.isalpha():
            user_text = user_text.capitalize()
            user_data['first_name'] = user_text
            print(user_data)
            bot.send_message(user_id, 'Please type in your Last Name 💬', reply_markup=buttons.cancel_buttons())
            clear_trash_messages(message)
            bot.register_next_step_handler(message, register_email_address)
        else:
            user_trash_response = message.message_id
            trash_messages.append(user_trash_response)
            bot_trash_response = bot.send_message(user_id, '❌ Error invalid First Name! ❌\n\n'
                                                           '🔄 Please try again to type in your First Name 🔄')
            trash_messages.append(bot_trash_response.message_id)
            bot.register_next_step_handler(message, register_first_name)


# Function to handle email input
def register_email_address(message):
    user_id = message.from_user.id
    user_text = message.text
    if user_text == '❌ Cancel':
        bot.send_message(user_id, '‼️ Registration is canceled ‼️\n\n',
                         reply_markup=buttons.registration_buttons())
        clear_trash_messages(message)
        bot.register_next_step_handler(message, register_first_name)
    else:
        if user_text.isalpha():
            user_text = user_text.capitalize()
            user_data['last_name'] = user_text
            clear_trash_messages(message)
            print(user_data)
            bot.send_message(user_id, 'Please type in Email address  📩', reply_markup=buttons.cancel_buttons())
            bot.register_next_step_handler(message, register_phone_number)
        else:
            user_trash_response = message.message_id
            trash_messages.append(user_trash_response)
            bot_trash_response = bot.send_message(user_id, '❌ Error invalid Last Name! ❌\n\n'
                                                           '🔄 Please try again to type in your Last Name 🔄')
            trash_messages.append(bot_trash_response.message_id)
            bot.register_next_step_handler(message, register_first_name)


# Function to validate and register phone number
def register_phone_number(message):
    user_id = message.from_user.id
    email_address = message.text.strip()
    parts = email_address.split('.')
    if email_address == '❌ Cancel':
        bot.send_message(user_id, '‼️ Registration is canceled ‼️\n\n', reply_markup=buttons.registration_buttons())
        clear_trash_messages(message)
        bot.register_next_step_handler(message, register_first_name)
    else:
        if '@' in email_address and not email_address.startswith('@') and not email_address.endswith('@') \
                and email_address.count('@') == 1 and ".." not in email_address and not email_address.startswith('.') \
                and not email_address.endswith('.') and '.' in email_address.split('@')[-1] and parts[-1].isalpha() \
                and len(parts[-1]) >= 2:
            user_data['email_address'] = email_address
            clear_trash_messages(message)
            print(user_data)
            bot.send_message(user_id, ' Please share your contact 📞 ', reply_markup=buttons.phone_number_buttons())
            bot.register_next_step_handler(message, finalizing_registration)
        else:
            user_trash_response = message.message_id
            trash_messages.append(user_trash_response)
            bot_trash_response = bot.send_message(user_id, '❌ Error invalid Email address! ❌\n\n'
                                                           '🔄 Please try again to type in Email address 🔄')
            trash_messages.append(bot_trash_response.message_id)
            bot.register_next_step_handler(message, register_phone_number)


# Function to finalize registration and store user data
def finalizing_registration(message):
    user_id = message.from_user.id
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '‼️ Registration is canceled ‼️\n\n', reply_markup=buttons.registration_buttons())
        clear_trash_messages(message)
        bot.register_next_step_handler(message, register_first_name)
    elif message.text == '☎️ Another phone number':
        bot.send_message(user_id, 'Please type in new Phone Number(+998) 💬', reply_markup=buttons.cancel_buttons())
        clear_trash_messages(message)
        bot.register_next_step_handler(message, registering_another_phone_number)
    elif message.contact:
        clear_trash_messages(message)
        phone_number = '+' + message.contact.phone_number
        user_data['phone_number'] = phone_number
        creating_random_password()
        print(user_data)
        adding_to_the_database = database.add_new_staff_member(user_data)
        if adding_to_the_database:
            bot.send_message(user_id,
                             f'🎉🎉🎉 Congratulations, {user_data['first_name']} {user_data['last_name']}   🎉🎉🎉\n\n'
                             f'Sir, you have successfully added new staff member ✅',
                             reply_markup=buttons.registration_buttons())
            user_data.clear()
        else:
            bot.send_message(user_id, f'⁉️ Error. Could not add the staff member details to the database ⁉️'
                                      f'\n\n❕ Please try again later ❕')
            bot.register_next_step_handler(message, start_bot)
    else:
        user_trash_response = message.message_id
        trash_messages.append(user_trash_response)

        bot_trash_response = bot.send_message(user_id, ' 🔽 Please use buttons below 🔽',
                                              reply_markup=buttons.phone_number_buttons())
        trash_messages.append(bot_trash_response.message_id)
        bot.register_next_step_handler(message, finalizing_registration)


# Function to register another phone number
def registering_another_phone_number(message):
    user_id = message.from_user.id
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '‼️ Registration is canceled ‼️\n\n', reply_markup=buttons.registration_buttons())
        clear_trash_messages(message)
        bot.register_next_step_handler(message, register_first_name)
    else:
        phone_number = message.text.strip()
        if phone_number.startswith('+998'):
            phone_number_second_part = phone_number[4:]
            if phone_number_second_part.isdigit() and len(phone_number_second_part) == 9:
                clear_trash_messages(message)
                user_data['phone_number'] = phone_number
                creating_random_password()
                print(user_data)
                adding_staff_member_to_the_database = database.add_new_staff_member(user_data)
                if adding_staff_member_to_the_database:
                    bot.send_message(user_id,
                                     f'🎉🎉🎉 Congratulations, {user_data['first_name']} {user_data['last_name']}   🎉🎉🎉\n\n'
                                     f'Sir, you have successfully added new staff member ✅',
                                     reply_markup=buttons.registration_buttons())
                    user_data.clear()
                else:
                    bot.send_message(user_id, f'⁉️ Error. Could not add the staff member details to the database ⁉️'
                                              f'\n\n❕ Please try again later ❕')
                    bot.register_next_step_handler(message, start_bot)
            else:
                user_trash_response = message.message_id
                trash_messages.append(user_trash_response)
                bot_trash_response = bot.send_message(user_id,
                                                      '‼️ Error: Invalid format. Ensure the number after +998'
                                                      ' is 9 digits long and contains only numbers ‼️',
                                                      reply_markup=buttons.cancel_buttons())
                trash_messages.append(bot_trash_response.message_id)
                bot.register_next_step_handler(message, registering_another_phone_number)
        else:
            user_trash_response = message.message_id
            trash_messages.append(user_trash_response)

            bot_response = bot.send_message(user_id, '‼️ Error: Ensure your new phone number starts with "+998". ‼️',
                                            reply_markup=buttons.cancel_buttons())
            trash_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, registering_another_phone_number)


# Function to create a random password
def creating_random_password():
    import random
    password_list = []
    random_length = random.randint(17, 20)
    while True:
        if len(password_list) == random_length:
            password = ''.join(password_list)
            user_data['user_unique_id'] = str(password)
            break
        else:
            random_ASCII = random.randint(33, 126)
            random_symbol = chr(random_ASCII)
            password_list.append(random_symbol)


# Function to delete staff member
def delete_staff(message):
    user_id = message.from_user.id
    if message.text == '❌ Cancel':
        bot.send_message(user_id, '‼️ Registration is canceled ‼️\n\n', reply_markup=buttons.registration_buttons())
        clear_trash_messages(message)
        user_data.clear()
        bot.register_next_step_handler(message, register_first_name)
    else:
        staff_unique_id_number = message.text
        check_id = database.check_staff_id(staff_unique_id_number)
        if check_id:
            bot.send_message(user_id, f'❕❕Deleting {check_id[2]} {check_id[3]} from database❕❕')
            time.sleep(2)
            bot.send_message(user_id, 'Loading changes ...')
            time.sleep(2)
            bot.send_message(user_id, 'Finishing ...')
            time.sleep(1)
            delete_staff_member = database.delete_staff_member(staff_unique_id_number)
            if delete_staff_member:
                bot.send_message(user_id, 'Successfully deleted ✅', reply_markup=buttons.registration_buttons())
                user_data.clear()
                clear_trash_messages(message)
                bot.register_next_step_handler(message, register_first_name)
            else:
                bot.send_message(user_id,
                                 '‼️ Error. Could you delete staff details ‼️'
                                 '\n\nPlease try again later',
                                 reply_markup=buttons.cancel_buttons())
                bot.register_next_step_handler(message, delete_staff)
        else:
            user_trash_response = message.message_id
            trash_messages.append(user_trash_response)

            bot_response = bot.send_message(user_id, '‼️ Error. Invalid staff id ‼️'
                                                     '\n\nPlease try again',
                                            reply_markup=buttons.cancel_buttons())
            trash_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, delete_staff)


# Starts bot and runs indefinitely
bot.polling(non_stop=True)
