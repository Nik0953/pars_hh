from pycbrf import ExchangeRates
import requests

def vacancy_selection(vac_list):
    """
    функция собирает список вакансий с заполненными полями
    требований к должности и максимальной заработной платы
    также создается поле с заработной платой в рублях по текущему курсу
    :param vac_list: список вакансий в форме словаря
    :return: список вакансий в форме словаря; полный текст всех требований в виде строки
    """
    # список отобранных вакансий
    vac_list_selected = []
    # все тексты требований
    txt_book = ''

    # курсы валют
    rate = ExchangeRates()

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
                            vac_list_selected.append(vac)

    return vac_list_selected, txt_book

def vacancy_stat(vac_list, txt_to_search):
    """
    функция находит все вакансии из vac_list
    с требованием к должности из 'txt_to_search'
    и возвращает количество таких вакансий и общую сумму из поля 'zarplata_rub'
    """
    vac_count = 0
    zarplata_total = 0

    if txt_to_search:
        for vac in vac_list:
            if vac['snippet']:
                if vac['snippet']['requirement']:
                    if vac['snippet']['requirement'].lower().find(txt_to_search) > 0:
                        vac_count += 1
                        if vac['zarplata_rub']:
                            zarplata_total += vac['zarplata_rub']

    # этот случай, если не передается подстрока для поиска,
    # значит, нужно вернуть общую информацию о вакансиях
    else:
        vac_count = len(vac_list)
        for vac in vac_list:
            if vac['zarplata_rub']:
                zarplata_total += vac['zarplata_rub']

    return vac_count, zarplata_total
