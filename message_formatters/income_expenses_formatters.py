import aiogram.utils.markdown as fmt


def summary_information_fmt(data):
    """
    Форматтер сообщения, выводящегося при функции «Доходы/Расходы.Сводная информаци»
    """
    return fmt.text(
        fmt.text(f'Пермь доходы и расходы на {data["Дата"]}:'),
        fmt.text('—'*30),
        fmt.text("ДОХОД:",fmt.hbold(data["Доход за день"]),"|","РАСХОД:", fmt.hbold(data["Расход за день"]),"|","ИТОГ:",fmt.hbold(data["Итог за день"])),
        sep='\n'
    )

    
def money_movement_fmt(data):
    """
    Форматтер сообщения, выводящегося при функции «Доходы/Расходы.Движения средств»
    """
    row_fmt = lambda line: fmt.text(
        fmt.text(fmt.hitalic(line["Отметка времени"]),fmt.hitalic(line["Источник"])), fmt.hbold(line["Сумма"]),fmt.hitalic(line["Примечание"]))
    d=[fmt.text(fmt.hitalic('Движений нет.'))]
    if data['Данные']:
        d = [row_fmt(line) for line in data['Данные']]
    return fmt.text(
        fmt.text(f'Пермь движения денежных средств за {data["Дата"]}:'),
        fmt.text('—'*30),
        *d,
        sep='\n'
    )

    
def summary_information_and_money_movement_fmt(data):
    """
    Форматтер сообщения, выводящегося при функции «Доходы/Расходы.Сводная информаци и Движения средств»
    """
    row_fmt = lambda line: fmt.text(
        fmt.text(fmt.hitalic(line["Отметка времени"]),fmt.hbold(line["Источник"])), fmt.hbold(line["Сумма"]),fmt.hitalic(line["Примечание"]))
    d=[fmt.text(fmt.hitalic('Движений нет.'))]
    if data['Данные']:
        d = [row_fmt(line) for line in data['Данные']]
    return fmt.text(
        fmt.text(f'Пермь доходы и расходы на {data["Дата"]}:'),
        fmt.text(fmt.hbold(data["Доход за день"]),"|", fmt.hbold(data["Расход за день"]),"|","ИТОГ:",fmt.hbold(data["Итог за день"])),
        fmt.text('—'*30),
        *d,
        sep='\n'
    )

    
