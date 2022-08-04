"""
Парсинг вакансий (hh api)
Основной модуль

"""

import os
from get_hh_vac import *
from txt_modules import *
from vacancy_analysis import *

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

# оставляем только вакансии с заполненными полями
# требований и заработной платы
# также получаем в один текст txt_book все требования к должности
vac_list_perfect, txt_book = vacancy_selection(vac_list)

# общая информация об отобранных вакансиях:
vac_total, zarplata_total = vacancy_stat(vac_list_perfect, '')

print('Всего вакансий:', len(vac_list))
print('Отобрано полных вакансий:', vac_total, 'средняя заработная плата по ним:', int(zarplata_total/vac_total), 'руб.')

# убрать из текста лишние символы
txt_book = txt_improve(txt_book)

# разбить на слова:
txt_lst = txt_book.split()
# уникальные слова:
txt_set = set(txt_lst)

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

for word in sorted_keys:
    words_fr_sorted[word] = words_fr[word]

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
        vac_req, zarpl_req = vacancy_stat(vac_list_perfect, word_for_research)
        print('Всего вакансий:', vac_req)
        if vac_req:
            print('Средний предел оплаты', int(zarpl_req / vac_req), 'руб, это', int(100*vac_req/len(vac_list_perfect)), '% вакансий от общего числа')
    else:
        if word_for_research:
            print('Ошибка, такого слова в тексте нет.')





