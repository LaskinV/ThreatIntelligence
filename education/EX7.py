import pandas as pd
import re
import requests
import json
from socket import gethostbyname

def analyze_file(file_name):
    data = pd.read_csv(file_name, encoding='latin-1', sep=';')
    domains = data.iloc[:, 1].str.lower()
    results = []  # Создайте пустой список для хранения результатов
    for domain in domains:
        if re.match(r".*sber.*", domain) or re.match(r".*avito.*", domain):
            info = get_domain_info(domain)
            results.append(info)  # Добавьте информацию о домене в список результатов
    return results  # Верните список результатов

def get_domain_info(domain):
    info = {
        "Domain": domain,
        "IP": None,
        "Response Code": None,
        "Title": None,
        "Redirect": None
    }
    try:
        info["IP"] = gethostbyname(domain)
    except:
        pass  # Failed to get IP

    try:
        response = requests.get(f'http://{domain}', timeout=5)
        info["Response Code"] = response.status_code
        if response.history:
            info["Redirect"] = [resp.url for resp in response.history]
        else:
            info["Redirect"] = []
        if response.status_code == 200:
            # Only parse the title if the status code is 200 OK
            info["Title"] = re.search('<title>(.*?)</title>', response.text).group(1)
    except:
        pass  # Failed to get HTTP response

    return info

# Список файлов для анализа
files = ["D:\education\education\ihead_domains_1698930578_9283.csv", "D:\education\education\ihead_domains_1698930619_6834.csv", "D:\education\education\ihead_domains_1698930652_2377.csv"]

all_results = []  # Создайте пустой список для хранения всех результатов

# Примените функцию analyze_file к каждому файлу в списке
for file in files:
    results = analyze_file(file)
    all_results.extend(results)  # Добавьте результаты из этого файла в общий список результатов

# Сохраните все результаты в JSON-файл
with open('domain_info.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_results, json_file, ensure_ascii=False, indent=4)
