import subprocess
import os
from bs4 import BeautifulSoup
import json
import re

java_file_path = "aips2sqlite.jar"

commands = [
    ['java', '-jar', '-Xmx8000m', 'aips2sqlite.jar', '--owner=Axapharm', '–plain', '--xml', '--lang=de', '--pinfo'],
    ['java', '-jar', '-Xmx8000m', 'aips2sqlite.jar', '--nodown', '--owner=Axapharm', '--plain', '--xml', '--lang=fr', '--pinfo'],
    ['java', '-jar', '-Xmx8000m', 'aips2sqlite.jar', '--nodown', '--owner=Axapharm', '--plain', '--xml', '--lang=it', '--pinfo'],
    ['java', '-jar', '-Xmx8000m', 'aips2sqlite.jar', '--owner=Axapharm', '–plain', '--xml', '--lang=de'],
    ['java', '-jar', '-Xmx8000m', 'aips2sqlite.jar', '--nodown', '--owner=Axapharm', '--plain', '--xml', '--lang=fr'],
    ['java', '-jar', '-Xmx8000m', 'aips2sqlite.jar', '--nodown', '--owner=Axapharm', '--plain', '--xml', '--lang=it']
]

languages = ['fr', 'it']
folders = ['pi', 'fi']

missing_files = ['25930', '29934', '56917', '58454', '58694', '58768', '58981', 
                 '59063', '62104', '62257', '62574', '63094', '65836', '66220', 
                 '66261', '66428', '66553', '66681', '67060', '67123', '67152',
                 '67250', '68814']

    
def download_files():
    for command in commands:
        subprocess.run(command)  
        print("command \"", command, "\" is successfully executed!")
        
def handle_missing_files():

    for missing_file_name in missing_files:

        with open("./output/fis/fi_it_html/" + missing_file_name + ".html", "w") as f:
            # Write the HTML code to the file
            f.write("""
        <!DOCTYPE html>
        <html>
        <head>
        <title>Hello World!</title>
        </head>
        <body>
        <div id="section1">Keine Daten zu diesem Produkt vorhanden!</div>
        </body>
        </html>
        """)

        # Save the file
        f.close()
    print("Missing files are successfully handled!")


def make_de_version():
  for folder_prefix in folders:
    folder_path = './output/' + folder_prefix + 's/' + folder_prefix + '_de_html'  # Specify the path to the folder containing HTML files
    # Get a list of all HTML files in the folder
    html_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]

    data = []
    key = []
    result = {}
    pattern = r"[^\n\s]+"

    # Iterate through each HTML file and read its contents
    for file_name in html_files:
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'r',  encoding='utf-8-sig') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            
            title_raw = soup.find('div', id='section1')
            title = re.search(pattern, str(title_raw.text).replace("-", ""))
            
            section_to_remove = soup.find('p', class_='footer')
            section_to_remove.extract() if section_to_remove else ""
            
            body = soup.find('body').prettify()

            # Append the title and body content to the data list
            if title.group() and body:
                data.append({title_raw.text.strip().replace(" ", "_").lower().split(",")[0] : body})
                key.append(title_raw.text.strip().replace(" ", "_").lower().split(",")[0])
                # print(key)
                result.update(dict(zip(data[len(data)-1].keys(), data[len(data)-1].values())))
                
                

    # Write the data list to a JSON file
    if os.path.isdir("./database_json"):
        pass
    else:
        os.makedirs("./database_json")
        
    output_file = './database_json/' + folder_prefix + '_de_output.json'  # Specify the name of the output file
    with open(output_file, 'w') as file:
        json.dump(result, file)

    # data directory
    if os.path.isdir("./data"):
        pass
    else:
        os.makedirs("./data")
    
    output_pi_de_data = './data/' + folder_prefix + '_de_data.json'
    with open(output_pi_de_data, 'w') as file:
        json.dump(data, file)

    # keys directory 
    if os.path.isdir("./keys"):
        pass
    else:
        os.makedirs("./keys")
    output_key = './keys/' + folder_prefix + '_key.json'
    with open(output_key, 'w') as file:
        json.dump(key, file)

    print(f"Data written to {output_file}.")
                
def convert_other_versions():
    for folder_prefix in folders:
        for lang in languages:
            folder_path = './output/' + folder_prefix + 's/' + folder_prefix + '_' + lang + '_html'

            html_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]

            with open('./keys/' + folder_prefix + '_key.json') as f:
                keys = json.load(f)
                
            with open('./data/' + folder_prefix + '_de_data.json') as f:
                data = json.load(f)

            result = {}
            pattern = r"[^\n\s]+"

            i = 0

            for file_name in html_files:
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8-sig') as file:
                    html_content = file.read()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    title_raw = soup.find('div', id='section1')
                    title = re.search(pattern, str(title_raw.text).replace("-", "")) if title_raw else ""
                    
                    section_to_remove = soup.find('p', class_='footer')
                    section_to_remove.extract() if section_to_remove else ""
            
                    body = soup.find('body')

                    if title.group() and body:
                        
                        data[i][keys[i]] = str(body)
                        result.update(dict(zip(data[i].keys(), data[i].values())))
                        
                i = i + 1
                # print("i == ", i)
                
            output_file = './database_json/' + folder_prefix + '_' + lang + '_output.json'  # Specify the name of the output file
            with open(output_file, 'w') as file:
                json.dump(result, file)
                
            print(f"Data written to {output_file}.")
                
if __name__ == "__main__":
    download_files()
    handle_missing_files()
    make_de_version()
    convert_other_versions()