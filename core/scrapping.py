from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import pandas as pd

# Настройки на Selenium с добавен User-Agent
options = Options()
options.add_argument("--headless")  # стартиране в безглав режим (без да се отваря прозорец)
options.add_argument("--disable-gpu")  # отключване на GPU, ако се стартира на виртуални машини
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Инициализиране на Selenium WebDriver (за Chrome)
driver = webdriver.Chrome(options=options)

# Канали за които да търсим линкове
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash=',
}

# Функция за извличане на m3u8 линкове
def update_links(channel, source_link):
    driver.get(source_link)
    # Изчакване за зареждане на динамично съдържание
    time.sleep(10)  # Изчакайте 10 секунди, за да се заредят всички елементи
    html_content = driver.page_source

    # Търсене на линкове, започващи с "https://cdn" и съдържащи "index.m3u8?"
    match = re.search(r'https://cdn[^\s"]+index\.m3u8\?[^\s"]*', html_content)
    if match:
        m3u_link = match.group(0)
        print(f"Found m3u link for {channel}: {m3u_link}")
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

# Затваряне на браузъра
driver.quit()
