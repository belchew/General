import os
import requests
import re
import pandas as pd

# Проверка дали файлът sources.m3u съществува, ако не го създаваме
file_path = 'sources.m3u'

# Проверка на директорията
print(f"Current working directory: {os.getcwd()}")

if not os.path.exists(file_path):
    print(f"{file_path} does not exist. Creating a new one.")
    with open(file_path, 'w') as file:
        file.write("")  # Създава празен файл
else:
    print(f"{file_path} already exists.")

# Канали и линкове
channel_mapping = {
    '#EXTINF:-1, Nat Geo Wild': 'https://www.seir-sanduk.com/?player=1&id=hd-nat-geo-wild-hd&pass=',
    '#EXTINF:-1, Kitchen 24': 'https://www.seir-sanduk.com/?player=1&id=hd-24-kitchen-hd&pass=',
    '#EXTINF:-1, BNT 1': 'https://www.seir-sanduk.com/?player=1&id=hd-bnt-1-hd&pass=',
    # Добавете още канали по необходимост
}

# Функция за извличане на линкове
def update_links(channel, source_link):
    with requests.Session() as session:
        response = session.get(source_link)
        match = re.search(r'https://[^\s"]+\.m3u8(?:\?[^\s"]*)?', response.text)
        if match:
            m3u_link = match.group(0)
            print(f"Fetched m3u link for {channel}: {m3u_link}")
            return m3u_link
        else:
            print(f"No m3u link found for {channel}")
            return None

# Събиране на данни
data_list = []
for channel, source_link in channel_mapping.items():
    fetched_link = update_links(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})

channel_df = pd.DataFrame(data_list)

# Проверка на съдържанието на файла преди запис
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        tv_m3u_content = file.read()
        print(f"Existing content of {file_path}:\n{tv_m3u_content}")
else:
    print(f"{file_path} does not exist.")

# Изчистване на съдържанието на файла преди запис
tv_m3u_content_updated = ""

# Обновяване на съдържанието
for index, row in channel_df.iterrows():
    channel_name = row['Channel']
    link_to_update = row['LinkToUpdate']
    if link_to_update is not None:
        tv_m3u_content_updated += f"{channel_name}\n{link_to_update}\n"
        print(f"Updating channel: {channel_name} with link: {link_to_update}")

# Записване на обновеното съдържание обратно във файла
with open(file_path, 'w') as file:
    file.write(tv_m3u_content_updated)
    print(f"File {file_path} successfully updated.")
