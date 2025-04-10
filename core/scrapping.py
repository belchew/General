from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import pandas as pd

# Channel mapping
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash=',
}

# Function to get m3u8 link using Selenium
def update_links_selenium(channel, source_link):
    # Initialize the browser driver (you may need to install the proper webdriver for your browser)
    driver = webdriver.Chrome()  # Ensure that you have installed the appropriate ChromeDriver
    driver.get(source_link)
    
    time.sleep(5)  # Wait for the page to load (you may need to adjust this)
    
    try:
        # Try to find the m3u8 link on the page
        m3u_link_element = driver.find_element(By.XPATH, '//*[contains(text(), "index.m3u8")]')
        m3u_link = m3u_link_element.get_attribute("href")
        print(f"Fetched m3u link for {channel}: {m3u_link}")
        return m3u_link
    except Exception as e:
        print(f"Error finding m3u link for {channel}: {e}")
        return None
    finally:
        driver.quit()

# Use function to sniff channels links in mapping
data_list = []
m3u_links = []

for channel, source_link in channel_mapping.items():
    fetched_link = update_links_selenium(channel, source_link)
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
