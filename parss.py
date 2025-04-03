import requests
from xml.etree import ElementTree as ET
import time
import os
from git import Repo

# URL на EPG XML файл в GitHub (заменете с вашия URL)
EPG_URL = "https://raw.githubusercontent.com/harrygg/EPG/refs/heads/master/all-2days.basic.epg.xml"
M3U_FILE_PATH = "output.m3u"  # Път на новия m3u файл, който ще генерираме

# Функция за изтегляне на EPG XML файл
def download_epg_xml(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Не може да се изтегли XML файл")

# Функция за създаване на m3u файл от EPG данни
def create_m3u_file(epg_data):
    # Извличаме всички програми от EPG
    root = ET.fromstring(epg_data)
    programmes = root.findall(".//programme")

    with open(M3U_FILE_PATH, "w") as m3u_file:
        m3u_file.write("#EXTM3U\n")  # Започваме m3u файла

        for programme in programmes:
            start = programme.get("start")
            stop = programme.get("stop")
            title = programme.find("title").text
            video_url = "your_video_link.m3u8"  # Примерен m3u8 линк, може да бъде различен

            # Преобразуваме времето от формат ISO в timestamp
            start_timestamp = int(time.mktime(time.strptime(start, "%Y%m%dT%H%M%S000Z")))
            stop_timestamp = int(time.mktime(time.strptime(stop, "%Y%m%dT%H%M%S000Z")))

            # Записваме информацията във m3u файл
            m3u_file.write(f"#EXTINF:{stop_timestamp - start_timestamp},{title}\n")
            m3u_file.write(f"{video_url}\n")

# Функция за добавяне на файла в Git репозиторио и качване в GitHub
def commit_and_push_to_github():
    # Път към текущото репозиторио
    repo_path = os.getcwd()  # Това е пътят до текущото работно директория
    repo = Repo(repo_path)

    # Добавяне на новия файл към репозиториото
    repo.git.add(M3U_FILE_PATH)

    # Комитване на промените
    repo.index.commit("Добавен нов m3u плейлист")

    # Пушване на промените в GitHub
    origin = repo.remote(name='origin')
    origin.push()

# Основна функция за стартиране на процеса
def main():
    try:
        # Стъпка 1: Изтегляне на EPG XML файла
        epg_data = download_epg_xml(EPG_URL)

        # Стъпка 2: Създаване на m3u файл от EPG данни
        create_m3u_file(epg_data)

        # Стъпка 3: Добавяне и качване на m3u файла в GitHub
        commit_and_push_to_github()

        print("m3u файл успешно създаден и качен в репозиториото!")

    except Exception as e:
        print(f"Грешка: {e}")

if __name__ == "__main__":
    main()
