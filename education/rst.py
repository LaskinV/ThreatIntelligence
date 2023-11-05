import requests
import json

# Ваш API ключ
api_key = 'teBcr6RJE36moDaSc6xB39GoNw4ZS7G1p6HCvi24'

def get_whois_info(domain):
    url = f'https://www.rstcloud.com/api/whois/{domain}'
    headers = {
        'apiKey': api_key
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        created_on = data.get('created_on', 'Unknown')
        registrar = data.get('registrar', 'Unknown')
    else:
        created_on = 'Unknown'
        registrar = 'Unknown'

    return created_on, registrar

def update_domain_info():
    # Считывание данных из domain_info.json
    with open('domain_info.json', 'r', encoding='utf-8') as f:
        domain_info_list = json.load(f)

    # Обновление информации для каждого домена
    for domain_info in domain_info_list:
        domain = domain_info['Domain']
        created_on, registrar = get_whois_info(domain)
        domain_info['Created On'] = created_on
        domain_info['Registrar'] = registrar

    # Сохранение обновленной информации обратно в domain_info.json
    with open('D:\education\domain_info.json', 'w', encoding='utf-8') as f:
        json.dump(domain_info_list, f, ensure_ascii=False, indent=4)

# Вызов функции для обновления информации
update_domain_info()
