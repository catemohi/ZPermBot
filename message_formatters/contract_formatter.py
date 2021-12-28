import aiogram.utils.markdown as fmt


def contract_fmt(data,day):
    """
    Форматтер сообщения, выводящегося при функции «Договоры»
    """
    row_fmt = lambda line: fmt.text(
        fmt.text('—'*30),
        fmt.text(fmt.hbold('Клиент:'), line['Клиент']),
        fmt.text(fmt.hbold('Юристы:'), line['Юристы']),
        sep="\n"
    )
    d = [fmt.text(
            fmt.text('—'*30),
            fmt.text(fmt.hitalic('Договоров нет.')),
            )]
    if data['Данные']:
        d = [row_fmt(line) for line in data['Данные']]
    return fmt.text(
        fmt.text(f'{day} день у договоров на дату',fmt.hbold(f'{data["Дата"]}:')),
        *d,
        sep='\n'
    )