from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

class ToDoApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'secret_key'
        self.init_db()
        self.setup_routes()

    def init_db(self):
        with sqlite3.connect("todo.db") as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    status TEXT NOT NULL DEFAULT 'To Do',
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)

    def setup_routes(self):
        app = self.app

        @app.route('/')
        def home():
            return render_template('login.html')

        @app.route('/login', methods=['POST'])
        def login():
            username = request.form['username']
            password = request.form['password']
            with sqlite3.connect("todo.db") as con:
                cur = con.cursor()
                cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
                user = cur.fetchone()
                if user:
                    session['user_id'] = user[0]
                    session['username'] = username
                    return redirect('/todo')
            return redirect('/')

        @app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                with sqlite3.connect("todo.db") as con:
                    cur = con.cursor()
                    try:
                        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                        con.commit()
                        return redirect('/')
                    except sqlite3.IntegrityError:
                        return "Username already exists."
            return render_template('register.html')

        @app.route('/todo')
        def todo():
            if 'user_id' not in session:
                return redirect('/')
            with sqlite3.connect("todo.db") as con:
                cur = con.cursor()
                cur.execute("SELECT id, description, completed, status FROM tasks WHERE user_id=?", (session['user_id'],))
                tasks = cur.fetchall()

            columns = {"To Do": [], "In Progress": [], "Done": []}
            for task in tasks:
                columns[task[3]].append(task)

            return render_template('todo.html', columns=columns, username=session['username'])

        @app.route('/add_task', methods=['POST'])
        def add_task():
            task = request.form['task']
            status = request.form['status']
            with sqlite3.connect("todo.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO tasks (description, status, user_id) VALUES (?, ?, ?)", (task, status, session['user_id']))
            return redirect('/todo')

        @app.route('/toggle_task/<int:task_id>', methods=['POST'])
        def toggle_task(task_id):
            with sqlite3.connect("todo.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE tasks SET completed = NOT completed WHERE id=? AND user_id=?", (task_id, session['user_id']))
            return redirect('/todo')

        @app.route('/delete_task/<int:task_id>', methods=['POST'])
        def delete_task(task_id):
            with sqlite3.connect("todo.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM tasks WHERE id=? AND user_id=?", (task_id, session['user_id']))
            return redirect('/todo')

        @app.route('/logout')
        def logout():
            session.clear()
            return redirect('/')

        @app.route('/update_task_status/<int:task_id>', methods=['POST'])
        def update_task_status(task_id):
            if 'user_id' not in session:
                return redirect('/')

            new_status = request.get_json()['status']
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute('UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?',
                      (new_status, task_id, session['user_id']))
            conn.commit()
            conn.close()
            return '', 204

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app = ToDoApp()
    app.run()