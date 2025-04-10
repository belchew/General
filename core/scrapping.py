import os
import base64
import re
import requests
import time
import pandas as pd

# Channel mapping
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash=',
}

# Creating function to m3u8 sniffer
def update_links(channel, source_link, retries=3, delay=5):
    with requests.Session() as session:
        # Add headers to simulate browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        for attempt in range(retries):
            try:
                print(f"Making request to {source_link} (Attempt {attempt + 1})")
                response = session.get(source_link, headers=headers, timeout=30)  # Increased timeout
                print(f"Response status code: {response.status_code}")
                # Search for m3u8 link in the response text
                match = re.search(r'https://cdn[^\s"]+index.m3u8\?[^"]*', response.text)
                if match:
                    m3u_link = match.group(0)
                    print(f"Fetched m3u link for {channel}: {m3u_link}")
                    return m3u_link
                else:
                    print(f"No m3u link found for {channel}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(delay)  # Wait before retrying
        return None  # Return None if all attempts fail

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
file_path = 'sources.m3u'

# Clear the file before writing new links
with open(file_path, 'w') as file:  # 'w' mode will overwrite the file (clear it first)
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')  # Добавяме на първия ред #EXTM3U
    for link in m3u_links:
        file.write(link + '\n')

print(f"File {file_path} successfully updated with new links.")
