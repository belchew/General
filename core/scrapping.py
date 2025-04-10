import os
import re
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By

# Channel mapping
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash=',
    # Добави тук и други канали с техните URL адреси, ако има нужда
}

def update_links_with_selenium(channel, source_link):
    """
    Използва Selenium, за да зареди динамично съдържание и да извлече m3u8 линкове.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Стартиране на браузър без GUI
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(source_link)
        driver.implicitly_wait(10)  # Изчаква 10 секунди, за да се заредят JavaScript елементите

        # Търсене на m3u8 линковете
        page_source = driver.page_source
        match = re.search(r'https:\/\/[^\s"]+\.m3u8(?:\?[^\s"]*)?', page_source)

        if match:
            m3u_link = match.group(0)
            print(f"Fetched m3u link for {channel}: {m3u_link}")
            return m3u_link
        else:
            print(f"No m3u link found for {channel}")
            return None
    finally:
        driver.quit()  # Затваря браузъра

def update_links(channel, source_link):
    """
    Използва requests, за да зареди съдържанието на страницата и да извлече m3u8 линковете.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        with requests.Session() as session:
            response = session.get(source_link, headers=headers, timeout=60)
            print(f"Status code for {source_link}: {response.status_code}")
            # Логване на първите 500 символа от съдържанието на HTML
            print(f"HTML preview: {response.text[:500]}")  # Показва първите 500 символа от HTML

            if response.status_code != 200:
                print(f"Failed to fetch {source_link} - Status code: {response.status_code}")
                return None

            # Проверка дали можем да намерим m3u8 линк
            match = re.search(r'https:\/\/[^\s"]+\.m3u8(?:\?[^\s"]*)?', response.text)
            if match:
                m3u_link = match.group(0)
                print(f"Fetched m3u link for {channel}: {m3u_link}")
                return m3u_link
            else:
                print(f"No m3u link found for {channel}")
                return None
    except requests.RequestException as e:
        print(f"Error fetching {source_link}: {e}")
        return None

def git_commit_and_push():
    """
    Комитва и пушва промените в GitHub репозитория.
    """
    repo_path = '/path/to/your/repo'  # Път до локалния репозитори
    os.chdir(repo_path)  # Променяме текущата директория на репозитория

    try:
        # Изпълняваме git команди
        subprocess.run(['git', 'add', 'sources.m3u'], check=True)  # Добавяме новия файл
        subprocess.run(['git', 'commit', '-m', 'Core engine links'], check=True)  # Комитираме
        subprocess.run(['git', 'push'], check=True)  # Пушваме промените в репозитория
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")

# Основна логика за извличане на линкове и актуализиране на файла
def main():
    data_list = []
    m3u_links = []

    for channel, source_link in channel_mapping.items():
        # Изпълняваме с requests, ако не работи - пробваме със Selenium
        print(f"Processing {channel}...")
        fetched_link = update_links(channel, source_link)
        
        if not fetched_link:
            print(f"Trying with Selenium for {channel}...")
            fetched_link = update_links_with_selenium(channel, source_link)
        
        data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
        if fetched_link:  # Ако линкът е намерен, го добавяме към списъка
            m3u_links.append(f"{channel}\n{fetched_link}")

    # Записваме линковете в sources.m3u файл
    file_path = 'sources.m3u'
    
    with open(file_path, 'w') as file:  # 'w' режим ще презапише файла
        file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')
        for link in m3u_links:
            file.write(link + '\n')

    print(f"File {file_path} successfully updated with new links.")

    # Извикваме Git командите за комит и пуш
    git_commit_and_push()

# Стартиране на основната логика
if __name__ == "__main__":
    main()
