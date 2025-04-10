import requests
import re
import pandas as pd

# Channel mapping
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash=',
}

# Добавяме User-Agent, за да изглеждаме като нормален браузър
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Функция за търсене на m3u8 линкове
def update_links(channel, source_link):
    with requests.Session() as session:
        # Изпращаме GET заявка с User-Agent
        response = session.get(source_link, headers=headers)
        
        # Търсим m3u8 линк, който започва с https://cdn и съдържа "index.m3u8?"
        match = re.search(r'https://cdn[^\s"]+index\.m3u8\?[^\s"]*', response.text)
        if match:
            m3u_link = match.group(0)
            print(f"Fetched m3u link for {channel}: {m3u_link}")
            return m3u_link
        else:
            print(f"No m3u link found for {channel}")
            return None

# Използваме функцията за да търсим линковете
data_list = []
m3u_links = []

for channel, source_link in channel_mapping.items():
    fetched_link = update_links(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
    if fetched_link:  # Ако линкът е открит, добавяме го в списъка с m3u линкове
        m3u_links.append(f"{channel}\n{fetched_link}")

# Записваме резултатите в .m3u файл
file_path = 'sources.m3u'

# Изчистваме файла преди да запишем новите линкове
with open(file_path, 'w') as file:  # 'w' режим ще презапише файла
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')  # Добавяме на първия ред #EXTM3U
    for link in m3u_links:
        file.write(link + '\n')

print(f"File {file_path} successfully updated with new links.")
