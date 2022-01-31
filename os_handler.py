import os
import json

# Функция только забирает польльзовательнские данные из текстовых документом
def get_info(filename):
    if os.path.isdir(r'C:\\token_folder') == True and os.path.isfile(r'C:\\token_folder\\' + filename + '.txt') == True:
        with open(r'C:\\token_folder\\' + filename + '.txt', 'r') as log:
            return log.read()

# Функция только записывает токен
def write_token(filename, token_to_write):
    if os.path.isdir(r'C:\\token_folder') == True and os.path.isfile(r'C:\\token_folder\\' + filename + '.txt') == True:
        with open(r'C:\\token_folder\\' + filename + '.txt', 'w') as log:
            return log.write(token_to_write)

# Функция записывает результаты выполнения программы
def write_result(file_name, overall_result):
    with open(r'C:\\overall_result\\' + file_name + '.json', 'w') as f:
        json.dump(overall_result, f, ensure_ascii=False, indent=4)

# Функция забирает строку подключения к базе данных
def get_sql_string():
    if os.path.isdir(r'C:\\SQL-string') == True and os.path.isfile(r'C:\\SQL-string\\' + 'sql_string.txt') == True:
        with open(r'C:\\SQL-string\\' + 'sql_string.txt', 'r') as log:
            return str(log.read())