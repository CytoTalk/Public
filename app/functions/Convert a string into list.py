import os
import uuid

from flask import current_app

def string_to_list(phrase, pattern_to_remove):
    new_list = []
    temp = ''

    clock = 0
    for i in range(0, len(phrase)):
        if clock > i:
            continue
        elif phrase[i:i + len(pattern_to_remove)] == pattern_to_remove:
            new_list.append(temp)
            temp = ''
            clock = i + len(pattern_to_remove)
        elif i == len(phrase) - 1:
            temp += phrase[i]
            new_list.append(temp)
            break
        else:
            temp += phrase[i]
    return new_list

def file_to_network(excelfilepath: str, key_column: int = 0, target_column: int = 0, pattern_to_remove: str = ',') -> str:
    wb = openpyxl.load_workbook(excelfilepath, data_only=True)
    sheet = wb.active
    c = sheet.cell

    new_dict = {}
    key_col_name = c(row=1, column=key_column).value
    target_col_name = c(row=1, column=target_column).value

    for i in range(2,1000000):
        key = c(row=i, column=key_column).value
        if key == None:
            break
        phrase = c(row=i,column=target_column).value
        splitted_list = string_to_list(phrase, pattern_to_remove)
        new_dict[key]=splitted_list

    wb = openpyxl.Workbook()
    sheet = wb.active
    c = sheet.cell

    c(row=1, column=1).value = key_col_name
    c(row=1, column=2).value = target_col_name
    r = 2
    for key in new_dict:
        for item in new_dict[key]:
            c(row=r, column=1).value = key
            c(row=r, column=2).value = item
            r+=1
    file_name = str(uuid.uuid4())[0:8] + '.xlsx'
    wb.save(os.path.join(current_app.config['OUTPUT_PATH'], file_name))
    return file_name


