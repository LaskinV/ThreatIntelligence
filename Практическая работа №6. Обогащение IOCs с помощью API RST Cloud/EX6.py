import requests
import re
import json

# URL страницы, которую вы хотите получить
url = "https://thedfirreport.com/2023/06/12/a-truly-graceful-wipe-out"

# Устанавливаем заголовки, чтобы сделать запрос более "подобным браузеру"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Отправляем GET-запрос с заголовками
response = requests.get(url, headers=headers)

# Функция для преобразования экранированных IOC в обычный формат
def decode_ioc(ioc):
    return ioc.replace('[.]', '.').replace('hxxps', 'https').replace('[:]', ':')

# Функция для проверки, является ли хеш частью URL
def is_part_of_url(hash, text):
    pattern = re.compile(r'https://[0-9a-f]*/' + re.escape(hash) + r'/')
    return bool(re.search(pattern, text))

# Проверяем успешность запроса
if response.status_code == 200:
    # Выводим HTML-код страницы
    html_content = response.text
    
    # Регулярные выражения для поиска экранированных IOC
    ip_regex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\[\.\]\d{1,3}\b")
    hash_regex = re.compile(r"\b[0-9a-f]{32}\b|\b[0-9a-f]{40}\b|\b[0-9a-f]{64}\b")
    domain_regex = re.compile(r"(hxxps\[:\]//[\w-]+\[\.\][\w-]+(/[^\s<]*)?)|([\w-]+\[\.\][\w-]+)")
    
    # Поиск всех совпадений
    ip_addresses = re.findall(ip_regex, html_content)
    domains = re.findall(domain_regex, html_content)
    # Поиск и фильтрация хешей
    hashes = []
    for match in re.finditer(hash_regex, html_content):
        start, end = match.span()
        surrounding_text = html_content[max(0, start - 20):end + 20]
        if 'https://' not in surrounding_text and '/' not in surrounding_text:
            hashes.append(match.group())
    
    # Декодирование экранированных IOC
    ip_addresses = [decode_ioc(ip) for ip in ip_addresses]
    domains = [decode_ioc(domain[0]) for domain in domains if domain[0]]
    
    # Создаем словарь с результатами
    results = {
        "IP Addresses": ip_addresses,
        "Hashes": hashes,
        "Domains": domains
    }

    # Записываем результаты в JSON-файл в текущей директории
    with open("ioc_data.json", "w") as json_file:
        json.dump(results, json_file, indent=4)

    # Выводим все найденные IOC
    print("IP Addresses:", ip_addresses)
    print("Hashes:", hashes)
    print("Domains:", domains)
else:
    print(f"Ошибка {response.status_code}: Не удалось получить страницу.")
