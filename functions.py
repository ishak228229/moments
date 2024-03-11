from telebot import types
import time

def typing(bot, cht, text, next_func = None, markup = None):
    if next_func == None and markup == None:
        bot.send_chat_action(cht, 'typing')
        time.sleep(1)
        bot.send_message(cht, text, parse_mode='HTML')
    elif markup == 'start':
        bot.send_chat_action(cht, 'typing')
        time.sleep(1)
        bot.send_message(cht, text, parse_mode='HTML', reply_markup=start_buttons())
    else:
        bot.send_chat_action(cht, 'typing')
        time.sleep(1)
        msg = bot.send_message(cht, text, parse_mode='HTML')
        bot.register_next_step_handler(msg, next_func)

def start_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    new_post = types.KeyboardButton('➕')
    home = types.KeyboardButton('Профіль 👤')
    friends = types.KeyboardButton('Друзі 🤝')
    markup.add(new_post)
    markup.add(home, friends)
    return markup