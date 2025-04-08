import os
import base64
import re
import pandas as pd
import requests

# Channel mapping
channel_mapping = {
    '#EXTINF:-1, Nat Geo Wild': 'https://www.seir-sanduk.com/?player=1&id=hd-nat-geo-wild-hd&pass=',
    '#EXTINF:-1, Kitchen 24': 'https://www.seir-sanduk.com/?player=1&id=hd-24-kitchen-hd&pass=',
    '#EXTINF:-1, BNT 1': 'https://www.seir-sanduk.com/?player=1&id=hd-bnt-1-hd&pass=',
    # Добавете още канали по необходимост
}

# Creating function to fetch m3u8 links
def update_links(channel, source_link):
    with requests.Session() as session:
        response = session.get(source_link)
        match = re.search(r'https://[^\s"]+\.m3u8(?:\?[^\s"]*)?', response.text)
        if match:
            m3u_link = match.group(0)
            return m3u_link
        else:
            return None

# Use function to fetch channel links in the mapping
data_list = []
for channel, source_link in channel_mapping.items():
    fetched_link = update_links(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})

channel_df = pd.DataFrame(data_list)

# Reading the existing m3u file
file_path = 'sources.m3u'

if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        tv_m3u_content = file.read()
else:
    tv_m3u_content = ""

# Clear the file before writing new content
tv_m3u_content_updated = ""

# Updating m3u content with the new links
for index, row in channel_df.iterrows():
    channel_name = row['Channel']
    link_to_update = row['LinkToUpdate']
    if link_to_update is not None:
        tv_m3u_content_updated += f"{channel_name}\n{link_to_update}\n"

# Write the updated content back to the file
with open(file_path, 'w') as file:
    file.write(tv_m3u_content_updated)

print(f"File {file_path} successfully updated.")
