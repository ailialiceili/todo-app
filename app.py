import tkinter as tk
from tkinter import messagebox
import json
import os

TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


def load_tasks():
    """JSONファイルからタスクを読み込む"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    """タスクをJSONファイルへ保存する"""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todoアプリ")
        self.root.resizable(False, False)

        self.tasks = load_tasks()

        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        # --- 入力エリア ---
        frame_input = tk.Frame(self.root, padx=10, pady=10)
        frame_input.pack(fill=tk.X)

        self.entry = tk.Entry(frame_input, width=40)
        self.entry.pack(side=tk.LEFT, padx=(0, 5))
        self.entry.bind("<Return>", lambda e: self._add_task())

        btn_add = tk.Button(frame_input, text="追加", width=8, command=self._add_task)
        btn_add.pack(side=tk.LEFT)

        # --- リスト表示エリア ---
        frame_list = tk.Frame(self.root, padx=10)
        frame_list.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_list, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(
            frame_list,
            width=50,
            height=15,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
        )
        scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- 削除ボタン ---
        frame_btn = tk.Frame(self.root, padx=10, pady=10)
        frame_btn.pack(fill=tk.X)

        btn_delete = tk.Button(
            frame_btn, text="削除", width=8, command=self._delete_task
        )
        btn_delete.pack(side=tk.RIGHT)

    def _refresh_list(self):
        """リストボックスをタスクリストで更新する"""
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, task)

    def _add_task(self):
        """タスクを追加する"""
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("入力エラー", "タスクを入力してください。")
            return
        self.tasks.append(text)
        save_tasks(self.tasks)
        self._refresh_list()
        self.entry.delete(0, tk.END)

    def _delete_task(self):
        """選択中のタスクを削除する"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("選択エラー", "削除するタスクを選択してください。")
            return
        index = selection[0]
        self.tasks.pop(index)
        save_tasks(self.tasks)
        self._refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
