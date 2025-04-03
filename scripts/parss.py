import requests
from xml.etree import ElementTree as ET
import time
import os
repo_path = os.getcwd()  
M3U_FILE_PATH = "output.m3u"  # Път на новия m3u файл, който ще генерираме
local_file_path = os.path.join(repo_path, M3U_FILE_PATH)

# Функция за изтегляне на EPG XML файл
def download_epg_xml(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("EPG XML файлът е изтеглен успешно.")
        return response.text
    else:
        print(f"Грешка при изтегляне на EPG файла: {response.status_code}")
        return None

# Функция за създаване на m3u файл от EPG данни
def create_m3u_file(epg_data):
    if epg_data is None:
        print("EPG данните не са налични.")
        return

    root = ET.fromstring(epg_data)
    programmes = root.findall(".//programme")

    if not programmes:
        print("Няма намерени програми в EPG XML файла.")
        return

    with open(M3U_FILE_PATH, "w") as m3u_file:
        m3u_file.write("#EXTM3U\n")  # Започваме m3u файла

        for programme in programmes:
            start = programme.get("start")
            stop = programme.get("stop")
            title = programme.find("title").text if programme.find("title") is not None else "Без заглавие"
            video_url = "your_video_link.m3u8"  # Примерен m3u8 линк, може да бъде различен

            # Преобразуваме времето от формат ISO в timestamp
            start_timestamp = int(time.mktime(time.strptime(start, "%Y%m%dT%H%M%S000Z")))
            stop_timestamp = int(time.mktime(time.strptime(stop, "%Y%m%dT%H%M%S000Z")))

            # Записваме информацията във m3u файл
            m3u_file.write(f"#EXTINF:{stop_timestamp - start_timestamp},{title}\n")
            m3u_file.write(f"{video_url}\n")

    print(f"m3u файлът беше успешно създаден и записан в {M3U_FILE_PATH}")

# Проверка дали m3u файлът е записан
def check_file_created(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        print(f"Файлът {file_path} е създаден успешно.")
    else:
        print(f"Файлът {file_path} не е създаден или е празен.")

# Основна функция
def main():
    try:
        # Стъпка 1: Изтегляне на EPG XML файла
        epg_data = download_epg_xml("https://raw.githubusercontent.com/harrygg/EPG/refs/heads/master/all-2days.basic.epg.xml")

        # Стъпка 2: Създаване на m3u файл от EPG данни
        create_m3u_file(epg_data)

        # Стъпка 3: Проверка на резултата
        check_file_created(M3U_FILE_PATH)

    except Exception as e:
        print(f"Грешка: {e}")

if __name__ == "__main__":
    main()
