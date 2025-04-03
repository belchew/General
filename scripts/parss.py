import xml.etree.ElementTree as ET
import requests
from datetime import datetime

# Функция за конвертиране на време в секунди
def time_to_seconds(time_str):
    time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
    return int(time_obj.timestamp())

# Изтегляне на EPG XML файл
tree = ET.parse('epg.xml')
root = tree.getroot()

# Четене на данни от EPG
programs = []
for program in root.findall('.//programme'):
    title = program.find('title').text
    start_time = program.find('start').text
    end_time = program.find('stop').text
    programs.append({'title': title, 'start_time': start_time, 'end_time': end_time})

# Отваряне на m3u файла за добавяне на нови записи
with open('output.m3u', 'a') as m3u_file:
    for program in programs:
        start_seconds = time_to_seconds(program['start_time'])
        end_seconds = time_to_seconds(program['end_time'])
        
        # Форматиране на нови сегменти
        m3u_segment = f"#EXTINF:{end_seconds - start_seconds},{program['title']}\n"
        m3u_segment += f"http://example.com/video/index-{start_seconds}-{end_seconds}.ts\n"
        
        # Записване на новия сегмент в m3u файла
        m3u_file.write(m3u_segment)

print("m3u файлът е актуализиран успешно!")
