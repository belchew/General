import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# Channel mapping
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash='
    # Добави още канали, ако е необходимо
}

# Функция за извличане на .m3u8 линкове
def update_links(channel, source_link):
    response = requests.get(source_link)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')  # Парсваме HTML съдържанието
        # Намираме всички линкове, които съдържат .m3u8
        m3u8_links = re.findall(r'https://[^\s"]+\.m3u8(?:\?[^\s"]*)?', soup.prettify())
        
        if m3u8_links:
            print(f"Fetched m3u link for {channel}: {m3u8_links[0]}")  # Показваме първия линк
            return m3u8_links[0]  # Връщаме първия линк, ако има такива
        else:
            print(f"No m3u link found for {channel}")
            return None
    else:
        print(f"Failed to fetch the page for {channel}. Status code: {response.status_code}")
        return None

# Събиране на линковете
data_list = []
m3u_links = []

for channel, source_link in channel_mapping.items():
    fetched_link = update_links(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
    if fetched_link:  # Ако е намерен линк
        m3u_links.append(f"{channel}\n{fetched_link}")

channel_df = pd.DataFrame(data_list)

# Записваме линковете в m3u файл
file_path = 'sources.m3u'

with open(file_path, 'w') as file:
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')  # Първи ред
    for link in m3u_links:
        file.write(link + '\n')

print(f"File {file_path} successfully updated with new links.")
