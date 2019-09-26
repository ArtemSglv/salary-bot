import telebot

# telebot.apihelper.proxy = {'https': 'socks5://167.71.182.13:3128'}
bot = telebot.TeleBot('')
keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('Yes', 'No')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hi, are Maxim stupid?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Yes':
        bot.send_message(message.chat.id, 'Yes')
    elif message.text == 'No':
        bot.send_message(message.chat.id, 'Anyway, yes!')


bot.polling()
