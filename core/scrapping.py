import os
import base64
import re
import pandas as pd
import requests
import subprocess

# Channel mapping
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/hd-diema-sport-hd-online?player=3&id=hd-diema-sport-hd&pass='
        
            

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
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')  # Добавяме на първия ред #EXTM3U
    for link in m3u_links:
        file.write(link + '\n')

print(f"File {file_path} successfully updated with new links.")

#def git_commit_and_push():
 #   repo_path = '/Users/admin/Downloads/General'  # Път до вашия локален репозитори
  #  os.chdir(repo_path)  # Променяме текущата директория на репозитория

#   try:
        #Изпълняваме git команди
    # subprocess.run(['git', 'add', 'sources.m3u'], check=True)  # Добавяме новия файл
     #  subprocess.run(['git', 'commit', '-m', 'Обновен m3u файл с нови линкове'], check=True)  # Комитираме
     #  subprocess.run(['git', 'push'], check=True)  # Пушваме промените в репозитория
    # except subprocess.CalledProcessError as e:
     #  print(f"Грешка при изпълнение на git команда: {e}")
     #  print(f"Изходът от командата е: {e.output}")
     #  print(f"Грешката е: {e.stderr}")

# Извикваме функцията за качване в GitHub
#git_commit_and_push()
