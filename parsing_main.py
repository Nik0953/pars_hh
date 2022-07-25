"""
Парсинг вакансий (hh api)

"""

import os
from pycbrf import ExchangeRates
from get_hh_vac import *
from txt_modules import *

"""
получаем исходный текст для обработки
"""

json_file_name = 'python_vac.json'

# Если база вакансий уже сформировна
if os.path.exists(json_file_name):
    with open(json_file_name, 'r') as f:
        vac_list = json.load(f)
else:
    vac_list = get_vacancies_from_hh('python developer', 'python_vac.json')


"""
парсинг исходного текста 
"""


# курсы валют
rate = ExchangeRates()

# полный текст для словаря с частотностью
txt_book = ''

# нам нужны вакансии с заполненными полями максимальной заработной платы и требований к кандидату
vac_list_perfect = []

for vac in vac_list:
    if vac['salary']:
        if vac['salary']['to']:
            if vac['salary']['currency']:
                if vac['snippet']:
                    if vac['snippet']['requirement']:
                        # нужные поля у этой вакансии заполнены
                        # заработную плату - в рубли
                        cur = str(vac['salary']['currency']).strip()
                        r = 1
                        if cur == 'BYN':
                            r = rate['BYN'].value
                        elif cur == 'USD':
                            r = rate['USD'].value
                        elif cur == 'EUR':
                            r = rate['EUR'].value

                        vac['zarplata_rub'] = r * vac['salary']['to']

                        # дополняем текст для общего словаря
                        txt_book += ' ' + vac['snippet']['requirement']
                        # добавляем вакансию в "чистый" список
                        vac_list_perfect.append(vac)


print('Всего вакансий:', len(vac_list), '  Отобрано полных вакансий:', len(vac_list_perfect))

# убрать из текста лишние символы
txt_book = txt_improve(txt_book)

# разбить на слова:
txt_lst = txt_book.split()
# уникальные слова:
txt_set = set(txt_lst)

# подсчет числа слов:

# создаем словарь с частотностью
words_fr = dict.fromkeys(txt_set)

for word in words_fr:
    counter = 0
    for slovo in txt_lst:
        if word == slovo:
            counter += 1
    words_fr[word] = counter

# словарь с отсортированными ключами-частотой слов

words_fr_sorted = {}
sorted_keys = sorted(words_fr, key=words_fr.get, reverse=True)

for w in sorted_keys:
    words_fr_sorted[w] = words_fr[w]

"""
Диалог с пользователем 
для определения целевых слов
"""


# печатаем первые элементы
print('*'*20, '   Чаще всего в акетах встречаются слова:   ', '*'*20)
print(list(words_fr_sorted)[:150], '\n')

word_for_research = 'Ожидание ввода пользователя...'

while word_for_research:
    word_for_research = input('Пожалуйста, введите интересующее слово для анализа [или Enter для завершения]: ')
    if word_for_research in words_fr_sorted:
        print('Анализ анкет, содержащих в требованиях слово \"', word_for_research, '\":', sep='')
    else:
        if word_for_research:
            print('Ошибка, такого слова в тексте нет.')





