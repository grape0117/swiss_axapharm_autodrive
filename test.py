import os
from bs4 import BeautifulSoup
import json
import re

folder_path = './fi_fr_html'

html_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]

with open('fi_de_data.json') as f:
    data = json.load(f)

with open('fi_key.json') as f:
    keys = json.load(f)

# print(len(data))
# print(data[0])

key = []
result = {}
pattern = r"[^\n\s]+"

i = 0

for file_name in html_files:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        section1_raw = soup.find('div', id='section1')
        section1 = re.search(pattern, str(section1_raw.text).replace("-", ""))
        # section_to_remove = soup.find('p', class_='footer')
        # section_to_remove.extract()
        # section1 = re.search(pattern, str(section1_raw.text))
        body = soup.find('body')

        # print(section1_raw.text.strip().replace(" ", "_").lower().split(",")[0])

        if section1.group() and body:
            data[i][keys[i]] = str(body)
            # data.append({section1_raw.text.strip().replace(" ", "_").lower().split(",")[0] : str(body)})
            # key.append(section1_raw.text.strip().replace(" ", "_").lower().split(",")[0])
            # print(key)
            # print(len(data), 'hello')
            # print(data[len(data)-1])
            # data[len(data)-1].update()
            # print(keys[len(data)-1])
            # result.update(dict(zip(data[len(data)-1].keys(), data[len(data)-1].values())))
            result.update(dict(zip(data[i].keys(), data[i].values())))
    i = i + 1
    print("i == ", i)

output_file = 'fi_fr_output.json'  # Specify the name of the output file
with open(output_file, 'w') as file:
    json.dump(result, file)