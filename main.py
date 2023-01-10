import requests
import json
import os
import datetime

API_BASE = "https://json.medrating.org"
BASE_TEXT = """...
# Отчёт для {company}.
{name} <{email}> {date}\n
Всего задач: {tasks}

## Актуальные задачи ({actual}):
{list_actual}

## Завершённые задачи ({done}):
{list_done}
...
"""

todos = json.loads(requests.get(f"{API_BASE}/todos").text)
users = json.loads(requests.get(f"{API_BASE}/users").text)
reports = {}

time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")


# Стандартизация названия todos
def crop_text(text):
    if len(text) > 46:
        return text[:46] + '...'
    else:
        return text


for user in users:
    todos_for_user = []
    actual_todos = []
    done_todos = []
    #
    # Сортировка и подсчет задач
    try:
        for todo in todos:
            if todo['userId'] == user['id']:
                todos_for_user.append(todo)
    except KeyError as e:
        print(f"Что-то с данными не так(((")
        print(e)

    for todo in todos_for_user:
        if todo['completed']:
            done_todos.append(todo)
        else:
            actual_todos.append(todo)


    # Создание листинга по ТЗ
    list_actual = "- " + "\n - ".join(
        [crop_text(todo['title']) for todo in actual_todos]
    )
    list_done = "- " + "\n - ".join(
        [crop_text(todo['title']) for todo in done_todos]
    )

    report = BASE_TEXT.format(
        company=user['company']['name'],
        name=user['name'],
        email=user['email'],
        date=time,
        tasks=len(todos_for_user),
        actual=len(actual_todos),
        done=len(done_todos),
        list_actual=list_actual,
        list_done=list_done
    )

    # Создание файла и переименование старого в формате
    # Использовала формат %Y-%m-%dT%H-%M т.к. блокнот не разрешает спец. символы
    if not os.path.exists('tasks'):
        os.mkdir('tasks')

    filename = os.path.join("./tasks", f"{user['username']}.txt")
    if os.path.exists(filename):
        dt_c = datetime.datetime.fromtimestamp(os.path.getctime(filename))
        dt = dt_c.strftime("%Y-%m-%dT%H-%M")
        os.rename(filename, os.path.join("./tasks", f"old_{user['username']}_{dt}.txt"))
    reports[filename] = report

for name, content in reports.items():
    file = open(name, "w+")
    file.write(content)

















