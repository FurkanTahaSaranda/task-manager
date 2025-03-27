import json
import os
import webview

DATA_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding='utf-8') as file:
            return json.load(file)
    return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding='utf-8') as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


class Api:
    def __init__(self):
        self.tasks = load_tasks()

    def get_tasks(self):
        return self.tasks

    def add_task(self, task_name):
        if task_name:
            self.tasks.append({"task": task_name, "completed": False})
            save_tasks(self.tasks)
            return True
        return False

    def edit_task(self, index, new_name):
        if 0 <= index < len(self.tasks) and new_name:
            self.tasks[index]["task"] = new_name
            save_tasks(self.tasks)
            return True
        return False

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            save_tasks(self.tasks)
            return True
        return False

    def toggle_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            save_tasks(self.tasks)
            return True
        return False

    def sort_tasks(self):
        self.tasks = sorted(self.tasks, key=lambda x: x["task"].lower())
        save_tasks(self.tasks)
        return True


def create_app():
    api = Api()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📚 Görev Yöneticisi</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .task-list {
                background: white;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .task-item {
                display: flex;
                align-items: center;
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            .task-text {
                flex-grow: 1;
                margin: 0 10px;
                font-size: 18px;
            }
            .completed {
                text-decoration: line-through;
                color: #888;
            }
            .controls {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }
            button {
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                flex-grow: 1;
                min-width: 120px;
            }
            .add-btn { background-color: #4CAF50; color: white; }
            .edit-btn { background-color: #2196F3; color: white; }
            .delete-btn { background-color: #F44336; color: white; }
            .complete-btn { background-color: #8BC34A; color: white; }
            .sort-btn { background-color: #FFC107; color: black; }
        </style>
    </head>
    <body>
        <h1>📚 Görev Yöneticisi</h1>

        <div class="controls">
            <button class="add-btn" onclick="addTask()">➕ Ekle</button>
            <button class="edit-btn" onclick="editTask()">✏️ Düzenle</button>
            <button class="delete-btn" onclick="deleteTask()">🗑️ Sil</button>
        </div>

        <div class="controls">
            <button class="complete-btn" onclick="toggleComplete()">✅ Tamamla</button>
            <button class="sort-btn" onclick="sortTasks()">🔄 Sırala</button>
        </div>

        <div class="task-list" id="taskList">
            <!-- Görevler buraya eklenecek -->
        </div>

        <script>
            let selectedIndex = -1;

            function refreshTasks() {
                window.pywebview.api.get_tasks().then(tasks => {
                    const taskList = document.getElementById('taskList');
                    taskList.innerHTML = '';

                    tasks.forEach((task, index) => {
                        const taskItem = document.createElement('div');
                        taskItem.className = 'task-item';
                        taskItem.onclick = () => {
                            document.querySelectorAll('.task-item').forEach(item => {
                                item.style.backgroundColor = '';
                            });
                            taskItem.style.backgroundColor = '#e3f2fd';
                            selectedIndex = index;
                        };

                        taskItem.innerHTML = `
                            <span style="font-size:20px;">${task.completed ? '✅' : '❌'}</span>
                            <span class="task-text ${task.completed ? 'completed' : ''}">${task.task}</span>
                        `;

                        taskList.appendChild(taskItem);
                    });
                });
            }

            function addTask() {
                const taskName = prompt('Yeni görev adı girin:');
                if (taskName) {
                    window.pywebview.api.add_task(taskName).then(refreshTasks);
                }
            }

            function editTask() {
                if (selectedIndex >= 0) {
                    const newName = prompt('Yeni görev adı girin:');
                    if (newName) {
                        window.pywebview.api.edit_task(selectedIndex, newName).then(refreshTasks);
                    }
                } else {
                    alert('Lütfen bir görev seçin!');
                }
            }

            function deleteTask() {
                if (selectedIndex >= 0) {
                    if (confirm('Bu görevi silmek istediğinize emin misiniz?')) {
                        window.pywebview.api.delete_task(selectedIndex).then(refreshTasks);
                    }
                } else {
                    alert('Lütfen bir görev seçin!');
                }
            }

            function toggleComplete() {
                if (selectedIndex >= 0) {
                    window.pywebview.api.toggle_complete(selectedIndex).then(refreshTasks);
                } else {
                    alert('Lütfen bir görev seçin!');
                }
            }

            function sortTasks() {
                window.pywebview.api.sort_tasks().then(refreshTasks);
            }

            // Sayfa yüklendiğinde görevleri getir
            window.onload = refreshTasks;
        </script>
    </body>
    </html>
    """

    window = webview.create_window(
        "📚 Görev Yöneticisi",
        html=html,
        js_api=api,
        width=800,
        height=600,
        resizable=True,
        text_select=True
    )

    webview.start()


if __name__ == "__main__":
    create_app()

