"""
функции для подготовки текста
"""

def txt_improve(txt_in):
    """
    функция удаляет ненужные символы из текста,
    переводит текст в нижний регистр
    :param txt_in: строка текста, который нужно улучшить
    :return: txt - итоговый текст
    """
    # перевести текст в нижний регистр
    txt = txt_in.lower()

    # удалить разметку и символы
    txt = txt.replace('<highlighttext>', ' ')
    txt = txt.replace('</highlighttext>', ' ')

    bad_symbols = '.,/!%()-–='
    for ch in bad_symbols:
        txt = txt.replace(ch, ' ')

    return txt