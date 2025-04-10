import os
import re
import pandas as pd
import requests

# Channel mapping
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash=',
}

# Creating function to m3u8 sniffer
def update_links(channel, source_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    with requests.Session() as session:
        try:
            response = session.get(source_link, headers=headers)
            response.raise_for_status()  # To ensure we don't miss HTTP errors like 404
            print(f"Fetched content from {source_link}")
            
            # Print first 500 characters of the HTML content for debugging
            print(response.text[:500])  # Show only the first 500 chars
            
            match = re.search(r'https://[^\s"]+\.m3u8(?:\?[^\s"]*)?', response.text)
            if match:
                m3u_link = match.group(0)
                print(f"Fetched m3u link for {channel}: {m3u_link}")
                return m3u_link
            else:
                print(f"No m3u link found for {channel} at {source_link}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {source_link}: {e}")
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
file_path = 'sources.m3u'

# Clear the file before writing new links
with open(file_path, 'w') as file:  # 'w' mode will overwrite the file (clear it first)
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')  # Adding #EXTM3U header
    for link in m3u_links:
        file.write(link + '\n')

print(f"File {file_path} successfully updated with new links.")
