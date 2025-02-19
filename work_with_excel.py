import os

import openpyxl
import pandas as pd

from other import create_folder


def auto_size_excel_file(path_to_file: str) -> None:
    """Автоширина ячеек в Excel"""

    wb = openpyxl.load_workbook(path_to_file)
    ws = wb.active
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[openpyxl.utils.get_column_letter(column[0].column)].width = adjusted_width
    wb.save(path_to_file)


def write_data_to_excel_wireBank(data: list) -> None:
    """
    Создание Excel файла

    :param data: данные
    :return:
    """

    number_phone = data[0]
    user_email = data[1]

    path_to_excel = os.path.join(os.getcwd(), 'result')
    create_folder(path_to_folder=path_to_excel)

    all_data = {
        'Номер телефона': [number_phone],
        'Почта': [user_email]
    }
    path_to_file = os.path.join(path_to_excel, 'result.xlsx')
    new_df = pd.DataFrame(all_data)
    try:
        df = pd.read_excel(path_to_file)
        df = pd.concat([df, new_df], ignore_index=True)
    except FileNotFoundError:
        df = new_df
    df.to_excel(path_to_file, index=False)
    auto_size_excel_file(path_to_file=path_to_file)

