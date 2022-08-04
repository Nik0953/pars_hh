import requests
import json
import time

def get_vacancies_for_telega(requirements, output_file_name):
    """
    функция Московские вакансии с сайта hh.ru
    за последние сутки
    и возвращает их в виде текстового файла для выдачи через telegram
    :param requirements: текстовая строка с требованиями к должности
    :param output_file_name: имя файла вывода
    :return: возвращает список вакансий
    """

    DOMAIN = 'https://api.hh.ru/vacancies/'
    vacancy_filter = {'text': requirements,
                      'area': '1',   # Москва
                      #'only_with_salary': 'true',
                      'period': '1',
                      'page': '0'
                      }

    # запрос к hh.ru
    result = requests.get(DOMAIN, params=vacancy_filter)

    # Успешно - 2XX
    print('Код ответа от сервера: ', result.status_code)

    data = result.json()

    # общее количество страниц выдачи
    vac_pages = int(data['pages'])

    # вакансий на страницу в выдаче
    vac_per_page = int(data['per_page'])

    # общее количество вакансий (возможно, недоступное)
    vac_found = int(data['found'])

    # здесь будет полный список вакансий
    vacancy_list = []

    page_current = 0

    # читаем постранично доступные вакансии
    while page_current < vac_pages:
        print('Вакансии, страница', page_current)
        vacancy_filter['page'] = str(page_current)
        result = requests.get(DOMAIN, params=vacancy_filter)
        data = result.json()
        # дописываем список вакансий с последней страницы к полному списку
        vacancy_list += data['items']
        page_current += 1

    print('\n\n всего собрано вакансий: ', len(vacancy_list))

    # Сохранение в файл
    with open(output_file_name, 'w') as f:
        json.dump(vacancy_list, f, ensure_ascii=False)

    return vacancy_list


def get_top_vacancy(vacancy_list):
    """
    Находит вакансию с самой высокой заработной платой
    и возвращает текст лучшей вакансии для публикации
    также записывает файл "vac.txt" для последующей пересылки
    :param vacancy_list: список словарей с вакансиями
    :return: vac_txt - текстовая строка с названием, [заработной платой] и ссылкой
    """

    # ищем вакансию с максимальной заработной платой
    top_vac = vacancy_list[0]
    top_salary = 0

    for vac in vacancy_list:
        if 'salary' in vac:
            try:
                top_salary = int(vac['salary']['to'])
                top_vac = vac
            except:
                vac['salary'] = {'to': '?', 'currency': 'RUB'}
        else:
            vac['salary'] = {'to': '?', 'currency': 'RUB'}


    # собираем текст для публикации:
    vac_txt = 'Новых вакансий: ' + str(len(vacancy_list)) +'.\n'
    vac_txt += 'Лучшая вакансия,\nопбубликованная сегодня:\n'
    vac_txt += top_vac['id'] + ': ' + top_vac['name'] + '\n'
    if top_vac['salary']:
        vac_txt += str(top_vac['salary']['to']) + ' ' + top_vac['salary']['currency'] + '\n'
    vac_txt += top_vac['alternate_url'] + '\n'

    # формируем краткий файл со всеми вакансиями:
    all_vacs_txt = 'Список новых вакансий\n'
    counter = 1
    for vac in vacancy_list:
        all_vacs_txt += str(counter) + ':  id ' + vac['id'] + ': ' + vac['name'] + '\n'
        if top_vac['salary']:
            all_vacs_txt += str(vac['salary']['to']) + ' ' + vac['salary']['currency'] + '\n'
        all_vacs_txt += vac['alternate_url'] + '\n--------------\n'
        counter += 1

    with open("vac.txt", 'w', encoding = 'utf-8') as f:
        f.write(all_vacs_txt)

    f.close()

    return vac_txt




if __name__ == '__main__':
    vac_lst = get_vacancies_for_telega('провизор технолог', 'vac_for_telega.json')
    print(get_top_vacancy(vac_lst))
