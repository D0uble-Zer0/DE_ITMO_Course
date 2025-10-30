def population_table(table):
    """
    Выделяет из найденой таблицы заголовки с html teh <span> и данные.
    Формирует таблицу из выделенных значений.
    """

    head_table = []
    for th in table.find("thead").find_all("th"):
        sp = th.find("span")
        if sp:
            head_table.append(sp.text.strip())
        else:
            head_table.append(th.text.strip())

    data = []
    for row in table.find("tbody").find_all("tr"):
        row_data = []
        for cell in row.find_all("td"):
            if cell.has_attr("data-order"):
                row_data.append(cell["data-order"])
            else:
                row_data.append(cell.text.strip())
        data.append(row_data)

    return head_table, data
