import requests
import json

def get_vacancies_from_hh(requirements, output_file_name):
    """
    функция получает Московские вакансии с сайта hh.ru
    и [пере-] записывает их в файл в формате json
    :param requirements: текстовая строка с требованиями к должности
    :param output_file_name: имя файла вывода
    :return: возвращает список вакансий
    """

    DOMAIN = 'https://api.hh.ru/vacancies/'
    vacancy_filter = {'text': requirements,
                      'area': '1',   # Москва
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
        json.dump(vacancy_list, f)

    return vacancy_list

if __name__ == '__main__':
    get_vacancies_from_hh('python developer', 'python_vac.json')
