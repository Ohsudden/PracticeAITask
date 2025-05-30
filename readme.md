📝 ToDo Board - Flask Web Application
A modern, Trello-style ToDo board built with Flask, SQLite3, and Neomorphism UI design. This app allows users to register, log in, and manage tasks across multiple categories using a dynamic drag-and-drop interface.

✅ Features
1. User Authentication
Login page with registration support. (You may use the test account - test:admin)

2. Task Management
Add new tasks with a specific status: To Do, In Progress, or Done.

Mark tasks as completed or delete them permanently.

Tasks are user-specific and persist via an SQLite database.

3. Trello-style Board UI
Tasks are displayed in vertical columns grouped by status.

Columns automatically update when tasks change state.

Neomorphic design using subtle shadows and smooth UI transitions.

4. Drag-and-Drop Functionality
Drag tasks between columns to update their status.

Works even when a column is initially empty.

Automatically updates the backend on drop via AJAX.

5. Responsive Design
Works on desktop and tablets.

