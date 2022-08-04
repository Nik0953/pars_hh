"""
Модуль запускаем бот @barbos13_bot
в Telegram
для поиска вакансий
"""

import telebot
from tele_hh_request import *

TOKEN ='5559195953:AAFofeArstRkBEljQMxcezvGD1PHl1Tym7E'


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help', 'h'])
def send_welcome(message):
    txt = f'Здравствуйте, {message.from_user.first_name}!'
    txt += '\nЭтот бот ищет по ключевым словам вакансии, размещенные на hh.ru за последние сутки работодателями в Москве.'
    txt += '\nНаберите команду \'/find\' и ключевые слова поиска через пробел без тире, точек, запятых и других символов.'
    txt += '\nПример: \n/find провизор технолог'
    bot.reply_to(message, txt)


# поиск вакансии
@bot.message_handler(commands=['find', 'f'])
def find(message):
    # получить то, что после команды
    key_lst = message.text.split()   # список слов после команды
    if len(key_lst) < 2:
        bot.reply_to(message, 'Не заданы параметры поиска\nПовторите в виде \n/find машинист оператор')
        return
    else:
        text_key = ' '.join(key_lst[1:]).lower()
        bot.reply_to(message, f'Работаю над запросом \n\'{text_key}\'...')

        #  получаем список всех вакансий
        vac_lst = get_vacancies_for_telega(text_key, 'vac_for_telega.json')
        #  отправляем в чат лучшую
        if vac_lst:
            txt_top_vac = get_top_vacancy(vac_lst)
        else:
            txt_top_vac = 'Вакансий новых не найдено'

        bot.reply_to(message, txt_top_vac)

        # отправляем в чат список всех вакансий в файле
        if vac_lst:
            with open('vac.txt', 'r', encoding='utf-8') as data:
                bot.send_document(message.chat.id, data)

@bot.message_handler(content_types=['text'])
def thanks_txt(message):
    answer = '\'/h\' for help'

    good_wrds = ['спасибо', 'благодарю', 'ок', 'ok']
    for wrd in good_wrds:
        if wrd in message.text.lower():
            answer = 'Всегда рады помочь!'

    greatings_wrds = ['здравствуйте', 'привет', 'добрый день', 'добрый вечер', 'доброе утро', 'hellow', 'hi']
    for wrd in greatings_wrds:
        if wrd in message.text.lower():
            answer = 'Здравствуйте!\nРады Вам!'

    last_wrds = ['до свидания', 'пока', 'good by']
    for wrd in last_wrds:
        if wrd in message.text.lower():
            answer = 'Ждём Вас снова!'

    bot.reply_to(message, answer)


bot.polling()
