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

def check_git_status():
    repo = git.Repo(repo_path)
    status = repo.git.status()
    print(status)

check_git_status()  # Това ще покаже състоянието на репозиториото

# Функция за изтегляне на файл от URL
def download_file(url, dest_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest_path, 'wb') as file:
            file.write(response.content)
        print(f"Файлът е изтеглен успешно и преименуван на {dest_path}")
    else:
        print(f"Грешка при изтегляне на файла: {response.status_code}")
        
def rearrange_file_lines(file_path):
    # Четене на съдържанието на файла
    with open(file_path, 'r') as file:
    
      lines = content.splitlines()
            if len(lines) > 18:
                content = '\n'.join(lines[:-18])
            file.seek(0)
            file.truncate()
            file.write(content)
        print(f"File edited successfully")
    except Exception as e:
        print(f"Error editing the file")
        
def commit_and_push_changes():
    # Отвори локалното репозиторио с gitpython
    repo = git.Repo(repo_path)
    
    # Добави новия файл в staging area (преди commit)
    repo.git.add(local_filename)
    
    # Извърши commit, ако има промени
    try:
        repo.git.commit('-m', 'Добавен нов файл basic.m3u от URL')
        print("Промените са комитнати успешно.")
    except git.exc.GitCommandError as e:
        print("Няма промени за комитване:", e)
    
    # Изпрати промените към origin (можеш да промениш името на remote, ако е различно)
    repo.git.push('origin', 'main')
    print(f"Промените са качени успешно в репозиториото: {repo_path}")

if __name__ == "__main__":
    # Изтегли файла и го преименувай на basic.txt
    download_file(file_url, local_file_path)
    
    # Извърши комитване и качване на промените
    commit_and_push_changes()
