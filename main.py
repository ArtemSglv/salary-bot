from datetime import datetime

import telebot
from telebot.types import Message

import db
from model.User import User

telebot.apihelper.proxy = {'https': ''}
bot = telebot.TeleBot('')
# keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
# keyboard.row('Yes', 'No')
# current User
curUser = User()


def is_login():
    return curUser.id is not None


@bot.message_handler(commands=['new_user'])
def registry_user(message: Message):
    curUser.name = message.from_user.first_name
    msg = bot.reply_to(message, 'What is your salary?')
    bot.register_next_step_handler(msg, process_salary_step)


def process_salary_step(m):
    curUser.name = m.from_user.first_name
    curUser.salary = m.text
    curUser.id = m.from_user.id
    if not curUser.salary.isdigit():
        msg = bot.reply_to(m, 'Salary should be a number. What is your salary?')
        bot.register_next_step_handler(msg, process_salary_step)
        return
    db.execute_insert_query('insert into users (user_id, name, salary) values (%s, %s, %s)',
                            (curUser.id, curUser.name, curUser.salary))
    bot.send_message(m.chat.id, 'User successfully registered!')


@bot.message_handler(commands=['record_progress'])
def record_progress_message(message):
    if is_login():
        msg = bot.send_message(message.chat.id, 'Enter your hours worked:')
        bot.register_next_step_handler(msg, record_progress)
    else:
        check_user(message)


@bot.message_handler(commands=['show_my_statistics'])
def show_statistics(message):
    if is_login():
        msg = bot.send_message(message.chat.id, 'Enter your hours worked:')
        bot.register_next_step_handler(msg, record_progress)
    else:
        check_user(message)


def record_progress(m):
    db.execute_insert_query('insert into progress (user_id, work_day, number_of_hours) values (%s, date%s, %s)',
                            (curUser.id, datetime.now().strftime('%Y-%m-%d'), m.text))
    bot.send_message(m.chat.id, 'Progress recorded!')


@bot.message_handler(func=lambda m: True, content_types=['text'])
def check_user(m):
    user = db.execute_select_query('select * from users where user_id = %s', (m.from_user.id,))
    print(user)
    if len(user) != 0:
        curUser.id = user[0][0]
        curUser.name = user[0][1]
        curUser.salary = user[0][2]
        bot.send_message(m.chat.id, 'User {} activated!'.format(curUser.name))
    else:
        bot.send_message(m.chat.id, 'User don\'t exist! Create user by taping /new_user')


bot.polling()
