import os
import base64
import re
import pandas as pd
import requests
import subprocess

# Channel mapping
channel_mapping = {
    '#EXTINF:-1, Nat Geo Wild': 'https://www.seir-sanduk.com/?player=1&id=hd-nat-geo-wild-hd&pass=',
    '#EXTINF:-1, Kitchen 24': 'https://www.seir-sanduk.com/?player=1&id=hd-24-kitchen-hd&pass=',
    '#EXTINF:-1, BNT 1': 'https://www.seir-sanduk.com/?player=1&id=hd-bnt-1-hd&pass=',
    '#EXTINF:-1, BNT 3': 'https://www.seir-sanduk.com/?player=1&id=hd-bnt-3-hd&pass=',
    '#EXTINF:-1, Max Sport 4': 'https://www.seir-sanduk.com/?player=3&id=hd-max-sport-4-hd&pass=',
    '#EXTINF:-1, Max Sport 3': 'https://www.seir-sanduk.com/?player=3&id=hd-max-sport-3-hd&pass=',
    '#EXTINF:-1, Diema Sport': 'https://seir-sanduk.com/diema-sport-hd-online',
    '#EXTINF:-1, Food Network BG': 'https://www.seir-sanduk.com/?player=1&id=hd-food-network-hd&pass=',
    '#EXTINF:-1, Epic Drama': 'https://www.seir-sanduk.com/?player=1&id=hd-epic-drama-hd&pass=',
    '#EXTINF:-1, Discovery Channel': 'https://www.seir-sanduk.com/?player=1&id=hd-discovery-channel-hd&pass=',
    '#EXTINF:-1, Star Crime': 'https://www.seir-sanduk.com/?player=1&id=hd-star-crime-hd&pass=',
    '#EXTINF:-1,Travel TV': 'https://www.seir-sanduk.com/?player=1&id=hd-travel-channel-hd&pass=',
    '#EXTINF:-1, Nova News': 'https://www.seir-sanduk.com/?player=1&id=hd-nova-news-hd&pass=',
    '#EXTINF:-1, Nova TV': 'https://www.seir-sanduk.com/?player=1&id=hd-nova-tv-hd&pass=',
    '#EXTINF:-1, BTV': 'https://www.seir-sanduk.com/?player=1&id=hd-btv-hd&pass=',
    '#EXTINF:-1, Max Sport 1': 'https://www.seir-sanduk.com/?player=3&id=hd-max-sport-1-hd&pass=',
    '#EXTINF:-1, Max Sport 2': 'https://www.seir-sanduk.com/?player=3&id=hd-max-sport-2-hd&pass=',
    '#EXTINF:-1, Nova Sports': 'https://www.seir-sanduk.com/?player=3&id=hd-nova-sport-hd&pass='

    # Add more channels as needed
}

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
file_path = 'C:\\Users\\a1bg537940\\Downloads\\General\\sources.m3u'

# Clear the file before writing new links
with open(file_path, 'w') as file:  # 'w' mode will overwrite the file (clear it first)
    file.write('#EXTM3U\n')  # Добавяме на първия ред #EXTM3U
    for link in m3u_links:
        file.write(link + '\n')

print(f"File {file_path} successfully updated with new links.")

def git_commit_and_push():
    repo_path = 'C:\\Users\\a1bg537940\\Downloads\\General'  # Път до вашия локален репозитори
    os.chdir(repo_path)  # Променяме текущата директория на репозитория

    try:
        # Изпълняваме git команди
        subprocess.run(['git', 'add', 'sources.m3u'], check=True)  # Добавяме новия файл
        subprocess.run(['git', 'commit', '-m', 'Обновен m3u файл с нови линкове'], check=True)  # Комитираме
        subprocess.run(['git', 'push'], check=True)  # Пушваме промените в репозитория
    except subprocess.CalledProcessError as e:
        print(f"Грешка при изпълнение на git команда: {e}")
        print(f"Изходът от командата е: {e.output}")
        print(f"Грешката е: {e.stderr}")

# Извикваме функцията за качване в GitHub
git_commit_and_push()