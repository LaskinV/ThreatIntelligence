import pandas as pd
import json

# Считывание данных из domain_info.json
with open('D:\education\domain_info.json', 'r', encoding='utf-8') as f:
    domain_info_list = json.load(f)

# Создание DataFrame с нужными полями
df = pd.DataFrame(domain_info_list)

# Переименование полей
df = df.rename(columns={'Domain': 'domain_name', 'Response Code': 'response_code', 'IP': 'ip', 'Title': 'title', 'Redirect': 'redirect', 'Created On': 'created_on', 'Registrar': 'registrar'})

# Сохранение DataFrame в CSV
df.to_csv('domain_info.csv', index=False, sep=',')

print("CSV файл 'domain_info.csv' успешно создан.")
