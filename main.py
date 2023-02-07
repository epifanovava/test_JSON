import shutil
from os.path import getctime
import requests
import datetime as dt
import os


def create_directory(destination: str):
    if not os.path.exists(destination):
        os.mkdir(destination)


def validation_data(data):
    if ('username' in data) and ('company' in data) and ('name' in data) and ('email' in data) and ('id' in data):
        return 1


def text_tasks(content: str):
    if len(content) > 46:
        return f"- {content[:46]}... \n"
    else:
        return f"- {content} \n"


create_directory('tasks')

todos = requests.get('https://json.medrocket.ru/todos').json()
users = requests.get('https://json.medrocket.ru/users').json()


for user in users:
    if validation_data(user):
        dir_ = 'tasks'
        time_now = dt.datetime.now(dt.timezone.utc).astimezone()
        time_format = '%d.%m.%Y %H:%M'
        # rename_format = '%Y-%m-%dT%H_%M' - for Windows
        rename_format = '%Y-%m-%dT%H:%M'
        all_tasks = 0
        actual_tasks = 0
        completed_tasks = 0
        text_actual_tasks = ''
        text_completed_tasks = ''

        for task in todos:
            if ('userId' in task) and ('completed' in task) and ('title' in task):
                if user['id'] == task['userId']:
                    all_tasks += 1
                    if task['completed'] is True:
                        completed_tasks += 1
                        text_completed_tasks += text_tasks(task['title'])
                    else:
                        actual_tasks += 1
                        text_actual_tasks += text_tasks(task['title'])

        if os.path.exists(os.path.join(dir_, f"{user['username']}.txt")):

            time_create = dt.datetime.fromtimestamp(getctime(os.path.join(dir_, f"{user['username']}.txt")))\
                .strftime(rename_format)

            old_file = os.path.join(dir_, f"{user['username']}.txt")
            new_file = os.path.join(dir_, f"old_{user['username']}_{time_create}.txt")
            shutil.copy(old_file, new_file)

        with open(os.path.join(dir_, f"{user['username']}.txt"), "w", encoding='UTF-8') as file:
            file.write(f"# Отчёт для {user['company']['name']}.\n"
                       f"{user['name']} <{user['email']}> {time_now:{time_format}}\n"
                       f"Всего задач: {all_tasks}\n\n"
                       f"## Актуальные задачи ({actual_tasks}): \n"
                       f"{text_actual_tasks} \n"
                       f"## Завершённые задачи ({completed_tasks}): \n"
                       f"{text_completed_tasks}")
