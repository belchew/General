from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

# Структура за каналите
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash=',
}

# Функция за търсене на линкове с Selenium
def update_links_selenium(channel, source_link):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Стартира браузъра в "headless" режим (без графичен интерфейс)
    
    # Създаване на WebDriver с автоматично конфигуриран ChromeDriver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get(source_link)
    time.sleep(5)  # Изчакване за зареждане на страницата

    try:
        # Търсене на m3u8 линк
        m3u_link_element = driver.find_element_by_xpath('//*[contains(text(), "index.m3u8")]')
        m3u_link = m3u_link_element.get_attribute("href")
        print(f"Fetched m3u link for {channel}: {m3u_link}")
        return m3u_link
    except Exception as e:
        print(f"Error finding m3u link for {channel}: {e}")
        return None
    finally:
        driver.quit()

# Използваме функцията за извличане на линкове
data_list = []
m3u_links = []

for channel, source_link in channel_mapping.items():
    fetched_link = update_links_selenium(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
    if fetched_link:  # Ако линкът е намерен, го добавяме в списъка
        m3u_links.append(f"{channel}\n{fetched_link}")

# Записваме новите линкове в .m3u файл
file_path = 'sources.m3u'
with open(file_path, 'w') as file:
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')  # Добавяме на първия ред #EXTM3U
    for link in m3u_links:
        file.write(link + '\n')

print(f"File {file_path} successfully updated with new links.")
