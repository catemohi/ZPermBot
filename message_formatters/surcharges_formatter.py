import aiogram.utils.markdown as fmt


def surcharges_fmt(data):
    """
    Форматтер сообщения, выводящегося при функции «Доплаты»
    """
    row_fmt = lambda line: fmt.text(
        fmt.text('—'*30),
        fmt.text(fmt.hbold('Клиент:'), line['Клиент']),
        fmt.text(fmt.hbold('Сумма:'), line['Сумма доплаты']),
        fmt.text(fmt.hbold('Юристы:'), line['Юристы']),
        sep="\n"
    )
    d=[]
    if data['Данные']:
        d = [row_fmt(line) for line in data['Данные']]
    return fmt.text(
        fmt.text(f'Доплаты на',fmt.hbold(f'{data["Дата"]}:')),
        fmt.text(fmt.hbold('Количество:'),f'{data["Количество доплат"]};',\
            fmt.hbold('Сумма:'),f'{data["Сумма"]}'),
        *d,
        sep='\n'
    )