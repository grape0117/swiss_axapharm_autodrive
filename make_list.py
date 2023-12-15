import os
from bs4 import BeautifulSoup
import json
import re

# with open('pi_key.json') as f:
#     keys = json.load(f)

folder_path = './fi_de_html'  # Specify the path to the folder containing HTML files

# Get a list of all HTML files in the folder
html_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]

data = []
key = []
result = {}
pattern = r"[^\n\s]+"

# french_text = soup.find('div', {'class': 'french-text'}).get_text()
# utf8_text = french_text.encode('utf-8')

# Iterate through each HTML file and read its contents
for file_name in html_files:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r',  encoding='utf-8-sig') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        section1_raw = soup.find('div', id='section1')
        # section_to_remove = soup.find('p', class_='footer')
        # section_to_remove.extract()
        section1 = re.search(pattern, str(section1_raw.text).replace("-", ""))
        # section1 = re.search(pattern, str(section1_raw.text))
        # section2 = soup.find('div', class_='ownerCompany')
        body = soup.find('body').prettify()

        # print("hello::::::::", section_to_remove)
        # print(section1_raw.text.strip().replace(" ", "_").lower().split(",")[0])
        # print(section1.group())
        # print(body)
        
        # Append the section1 and body content to the data list
        if section1.group() and body:
            data.append({section1_raw.text.strip().replace(" ", "_").lower().split(",")[0] : body})
            key.append(section1_raw.text.strip().replace(" ", "_").lower().split(",")[0])
            print(key)
            # print(len(data), 'hello')
            # print(data[len(data)-1])
            # data[len(data)-1].update()
            # print(keys[len(data)-1])
            result.update(dict(zip(data[len(data)-1].keys(), data[len(data)-1].values())))
            
            

# Write the data list to a JSON file
output_file = 'fi_de_output.json'  # Specify the name of the output file
with open(output_file, 'w') as file:
    json.dump(result, file)

output_pi_fr_data = 'fi_de_data.json'
with open(output_pi_fr_data, 'w') as file:
    json.dump(data, file)

output_key = 'fi_key.json'
with open(output_key, 'w') as file:
    json.dump(key, file)

print(f"Data written to {output_file}.")