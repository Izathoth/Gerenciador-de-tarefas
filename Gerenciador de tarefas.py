import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime

class Task:
    def __init__(self, title, description, priority, category, due_date, status='pending'):
        self.title = title
        self.description = description
        self.priority = priority
        self.category = category
        self.due_date = due_date
        self.status = status

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'category': self.category,
            'due_date': self.due_date,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            task_dict['title'],
            task_dict['description'],
            task_dict['priority'],
            task_dict['category'],
            task_dict['due_date'],
            task_dict['status']
        )

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task.from_dict(task) for task in tasks_data]

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def add_task(self, title, description, priority, category, due_date):
        task = Task(title, description, priority, category, due_date)
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]
        self.save_tasks()

    def update_task_status(self, title, status):
        for task in self.tasks:
            if task.title == title:
                task.status = status
                self.save_tasks()
                break

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.task_manager = TaskManager()

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_widgets()
        self.populate_task_list()

    def create_widgets(self):
        self.task_list = tk.Listbox(self.frame, width=50, height=15)
        self.task_list.grid(row=0, column=0, columnspan=3)

        ttk.Button(self.frame, text="Adicionar Tarefa", command=self.add_task).grid(row=1, column=0)
        ttk.Button(self.frame, text="Remover Tarefa", command=self.remove_task).grid(row=1, column=1)
        ttk.Button(self.frame, text="Atualizar Status", command=self.update_status).grid(row=1, column=2)

    def populate_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.task_manager.tasks:
            self.task_list.insert(tk.END, f"{task.title} - {task.status} (Prioridade: {task.priority}, Categoria: {task.category})")

    def add_task(self):
        title = simpledialog.askstring("Título", "Título da Tarefa:")
        description = simpledialog.askstring("Descrição", "Descrição da Tarefa:")
        priority = simpledialog.askstring("Prioridade", "Prioridade (Alta, Média, Baixa):")
        category = simpledialog.askstring("Categoria", "Categoria da Tarefa:")
        due_date = simpledialog.askstring("Data de Vencimento", "Data de Vencimento (YYYY-MM-DD):")

        if title:
            self.task_manager.add_task(title, description, priority, category, due_date)
            self.populate_task_list()

    def remove_task(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            selected_task_title = self.task_list.get(selected_task_index).split(' - ')[0]
            self.task_manager.remove_task(selected_task_title)
            self.populate_task_list()
        else:
            messagebox.showwarning("Seleção Inválida", "Selecione uma tarefa para remover.")

    def update_status(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            selected_task_title = self.task_list.get(selected_task_index).split(' - ')[0]
            new_status = simpledialog.askstring("Status", "Novo Status (pending, in progress, completed):")
            if new_status:
                self.task_manager.update_task_status(selected_task_title, new_status)
                self.populate_task_list()
        else:
            messagebox.showwarning("Seleção Inválida", "Selecione uma tarefa para atualizar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()