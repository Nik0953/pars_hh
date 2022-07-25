def vacancy_selection(vac_list):
    """
    функция собирает список вакансий с заполненными полями
    требований к должности и максимальной заработной платы
    также создается поле с заработной платой в рублях по текущему курсу
    :param vac_list: список вакансий в форме словаря
    :return: список вакансий в форме словаря; полный текст всех требований в виде строки
    """

    vac_list_selected = []

    txt_book = ''

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