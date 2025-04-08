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
    print(f"Fetching link for channel: {channel} from {source_link}")
    with requests.Session() as session:
        try:
            response = session.get(source_link)
            response.raise_for_status()  # Вдига грешка ако статусът не е 200
            print(f"Received response with status code {response.status_code} for {channel}")
            
            # Извличане на линк към m3u
            match = re.search(r'https://[^\s"]+\.m3u8(?:\?[^\s"]*)?', response.text)
            if match:
                m3u_link = match.group(0)
                print(f"Fetched m3u link for {channel}: {m3u_link}")
                return m3u_link
            else:
                print(f"No m3u link found for {channel}")
                return None
        except requests.RequestException as e:
            print(f"Error fetching link for {channel}: {e}")
            return None

# Use function to sniff channels links in mapping
data_list = []
m3u_links = []

# Обработка на каналите
for channel, source_link in channel_mapping.items():
    fetched_link = update_links(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
    
    if fetched_link:  # Ако линкът е извлечен, добавяме го в списъка m3u_links
        m3u_links.append(f"{channel}\n{fetched_link}")
    else:
        print(f"Skipping channel {channel} because no link was fetched.")

# Преобразуваме данните в DataFrame
channel_df = pd.DataFrame(data_list)

# Проверка дали има намерени линкове
if not m3u_links:
    print("No valid m3u links were found. The file will not be updated.")
else:
    # Записваме линковете в sources.m3u
    print(f"Writing {len(m3u_links)} m3u links to the file {file_path}")
    
    # Изчистваме съдържанието на файла и записваме новите линкове
    with open(file_path, 'w') as file:  # 'w' режим за презапис на файла
        for link in m3u_links:
            file.write(link + '\n')

    print(f"File {file_path} successfully updated with new links.")
