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
# Creating function to m3u8 sniffer
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

# Use function to sniff channels links in mapping
data_list = []
m3u_links = []

for channel, source_link in channel_mapping.items():
    fetched_link = update_links(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
    if fetched_link:  # If link is fetched, we add it to the m3u_links list
        m3u_links.append(f"{channel}\n{fetched_link}")

channel_df = pd.DataFrame(data_list)

# Write the fetched m3u links into the sources.m3u file
file_path = 'C:\\Users\\a1bg537940\\Desktop\\sources.m3u'

# Clear the file before writing new links
with open(file_path, 'w') as file:  # 'w' mode will overwrite the file (clear it first)
    for link in m3u_links:
        file.write(link + '\n')

print(f"File {file_path} successfully updated with new links.")

# Ако има ново съдържание, записваме го във файла
if tv_m3u_content_updated:
    with open(file_path, 'w') as file:
        file.write(tv_m3u_content_updated)
        print(f"File {file_path} successfully updated.")
else:
    print("No valid m3u links found, nothing to update.")
