import os
import requests

def download_file_from_repo(url, file_path):
    """
    Изтегля файл от външно репозитори и го записва локално.
    """
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Файлът е изтеглен и записан на {file_path}")
    else:
        print(f"Грешка при изтегляне на файла: {response.status_code}")

def replace_phrases_in_file(file_path, replacements):
    """
    Променя фрази и думи в локален файл.
    replacements е речник с ключове за замяна и стойности за новите думи.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Замяна на фразите
        for old_phrase, new_phrase in replacements.items():
            content = content.replace(old_phrase, new_phrase)

        # Записване на променения файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Файлът е успешно променен и записан на {file_path}")
    
    except FileNotFoundError:
        print(f"Файлът {file_path} не беше намерен!")

def copy_and_modify_file(source_url, destination_path, replacements):
    """
    Изтегля файл от даден URL, променя фрази и го записва в локално репозитори.
    """
    download_file_from_repo(source_url, destination_path)
    replace_phrases_in_file(destination_path, replacements)

# Примерни данни
source_url = 'https://raw.githubusercontent.com/belchew/connectdirect/refs/heads/main/sources.m3u'  # URL на файла от друго репозитори
destination_path = 'basic.m3u'  # Локалният път, където да запишеш файла
replacements = {
     "https://cdn2.glebul.com/hls/": 'https://cdn11.glebul.com/dvr/',
            "https://cdn3.glebul.com/hls/": 'https://cdn11.glebul.com/dvr/',
            "https://cdn4.glebul.com/hls/": 'https://cdn11.glebul.com/dvr/',
            "https://cdn5.glebul.com/hls/": 'https://cdn11.glebul.com/dvr/',
            "https://cdn6.glebul.com/hls/": 'https://cdn11.glebul.com/dvr/',
            "https://cdn7.glebul.com/hls/": 'https://cdn11.glebul.com/dvr/',
            "https://cdn8.glebul.com/hls/": 'https://cdn11.glebul.com/dvr/',
            "https://cdn9.glebul.com/hls/": 'https://cdn11.glebul.com/dvr/',
            #"index.m3u8?": 'tracks-v1a1/rewind-86940.m3u8?'
            "index.m3u8?": 'tracks-v1a1/index.m3u8?'
}

# Стартирай процеса
copy_and_modify_file(source_url, destination_path, replacements)
