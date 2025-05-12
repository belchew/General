import os
import requests
import git

# Път до твоето репозиторио, това ще бъде автоматично във всяка стъпка на GitHub Actions
repo_path = os.getcwd()  

file_url = 'https://raw.githubusercontent.com/belchew/connectdirect/refs/heads/main/sources.m3u'  

# Локален път, където ще запишеш файла
local_filename = 'basic.m3u' 
local_file_path = os.path.join(repo_path, local_filename)

# Функция за изтегляне на файл от URL
def download_file(url, dest_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest_path, 'wb') as file:
            file.write(response.content)
        print(f"Файлът е изтеглен успешно и преименуван на {dest_path}")
    else:
        print(f"Грешка при изтегляне на файла: {response.status_code}")
        
# Функция за замяна на съдържание във файла
def replace_multiple_content(file_path, replacements):
    try:
        # Отваряме файла за четене
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Извършваме замените
        for old_content, new_content in replacements.items():
            content = content.replace(old_content, new_content)

        # Записваме обратно промененото съдържание
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Съдържанието е успешно заменено в {file_path}.")
    
    except Exception as e:
        print(f"Грешка при замяна на съдържание във файла: {e}")

# Функция за изтриване на последните 18 реда от файла
def delete_last_n_lines(file_path, n=1):
    try:
        # Отваряме файла за четене
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Премахваме последните n реда
        lines = lines[:-n]

        # Записваме обратно промененото съдържание в същия файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        print(f"Последните {n} реда са изтрити успешно от файла {file_path}.")
    
    except Exception as e:
        print(f"Грешка при изтриване на последните {n} реда от файла: {e}")
        
# Функция за клониране на репозиторио и качване на промените
def commit_and_push_changes():
    # Отвори локалното репозиторио с gitpython
    repo = git.Repo(repo_path)
    
    # Добави новия файл
    repo.git.add(local_filename)
    
    # Извърши commit
    repo.git.commit('-m', 'Добавен нов файл basic.m3u от URL')
    
    # Изпрати промените към origin (можеш да промениш името на remote, ако е различно)
    repo.git.push('origin', 'main')
    print(f"Промените са качени успешно в репозиториото: {repo_path}")

if __name__ == "__main__":
    # Изтегли файла и го преименувай на basic.m3u
    download_file(file_url, local_file_path)
    
    # Изтриване на последните 18 реда от файла
    delete_last_n_lines(local_file_path, 1)

        # Замяна на множество редове съдържание във файла
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
    replace_multiple_content(local_file_path, replacements)
    # Извърши комитване и качване на промените
    commit_and_push_changes()
