import requests
from bs4 import BeautifulSoup
import json
import re

def get_html_code(url):
    response = requests.get(url)
    return response.text

def html_to_soup(html_code):
    return BeautifulSoup(html_code, 'html.parser')

def enrich_cve(cve):
    try:
        mitre_url = "https://cve.mitre.org/cgi-bin/cvename.cgi?name="
        cve_url = mitre_url + cve

        html_code = get_html_code(cve_url)
        soup = html_to_soup(html_code)
        description = soup.find("th", string="Description")
        description = description.find_next("td", colspan="2").text
    except Exception as e:
        print(e)
        return "Description not found"
    return description

url = 'https://support.apple.com/en-us/HT201222'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')

data = []
for row in rows[1:]:
    cols = row.find_all('td')
    cols = [element.text.strip() for element in cols]
    product_info = cols[0]
    if any(product in product_info for product in ['macOS', 'Safari', 'Xcode']):
        link_element = row.find('a')
        if link_element is not None:
            link = link_element['href']
            product_response = requests.get(link)
            product_soup = BeautifulSoup(product_response.content, 'html.parser')
            
            cve_matches = re.findall(r'CVE-\d{4}-\d{2,7}', product_soup.text)
            cve_dict = {}
            release_date = cols[2]
            if '2023' in release_date:
                for cve_id in set(cve_matches):
                    cve_dict[cve_id] = enrich_cve(cve_id)
                
                product_data = {
                    'name': product_info,
                    'information_link': link,
                    'available_for': cols[1],
                    'release_date': release_date,
                    'cve': cve_dict
                }
                data.append(product_data)

# Записываем результаты в JSON файл
output_file = 'apple_cve_data.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f'Результаты работы программы сохранены в файле {output_file}')
