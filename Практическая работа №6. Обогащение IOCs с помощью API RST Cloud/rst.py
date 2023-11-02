import requests
import json

# Открываем и читаем файл ioc_data.json
with open('D:\education\ioc_data.json', 'r') as file:
    ioc_data = json.load(file)

# URL и заголовки для API
url = "https://api.rstcloud.net/v1/ioc"
api_key = "api-key"  # Замените на свой API-ключ

headers = {
    "x-api-key": api_key,
    "Accept": "application/json"
}

# Функция для выполнения запроса к API и форматирования данных
def query_and_format(ioc_value):
    params = {"value": ioc_value}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        formatted_data = {
            "ioc": data.get("ioc_value", ""),
            "tag": ", ".join(data.get("tags", {}).get("str", [])),
            "related_threat": ", ".join(data.get("threat", [])),
            "report_source": data.get("src", {}).get("report", ""),
            "ioc_type": data.get("ioc_type", "")
        }
        return formatted_data
    else:
        print(f"Failed to query {ioc_value}, status code: {response.status_code}")
        return None

# Список для хранения отформатированных данных
formatted_data_list = []

# Итерация по каждому типу IOC и каждому значению
for ioc_type, ioc_values in ioc_data.items():
    for ioc_value in ioc_values:
        formatted_data = query_and_format(ioc_value)
        if formatted_data:
            formatted_data_list.append(formatted_data)

# Запись отформатированных данных в новый файл JSON
with open('formatted_ioc_data.json', 'w') as file:
    json.dump(formatted_data_list, file, indent=4)