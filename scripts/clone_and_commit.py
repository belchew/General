import os
import requests
import git
# Път до твоето репозиторио, това ще бъде автоматично във всяка стъпка на GitHub Actions
repo_path = os.getcwd()  # Това ще даде директорията на текущото репозиторио в GitHub Actions

# URL на файла, който искаш да клонираш
file_url = 'https://raw.githubusercontent.com/rosendonchev/linkove/refs/heads/main/video_stream.m3u'  # Замени с твоя URL

# Локален път, където ще запишеш файла
local_filename = 'basic.m3u'  # Промененото име на файла
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
        
# Функция за преместване на редове в basic.txt
def rearrange_file_lines(file_path):
    # Четене на съдържанието на файла
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Пример за преместване на редове: тук просто сменяме местата на първия и втория ред
    if len(lines) >= 2:
        lines[12], lines[13] = lines[4], lines[5]
        lines[10], lines[11] = lines[6], lines[7]
    # Записване на промененото съдържание обратно в файла
    with open(file_path, 'w') as file:
        file.writelines(lines)
    print("Редовете са преместени успешно!")

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
    # Изтегли файла и го преименувай на basic.txt
    download_file(file_url, local_file_path)
    
    # Извърши комитване и качване на промените
    commit_and_push_changes()
