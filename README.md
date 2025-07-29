# Flask Grade Management System

A web application for managing student grades with teacher and student roles.

## Features
- User authentication (login/signup)
- Role-based access (Teacher/Student)
- Subject management
- Grade tracking and management
- Teacher can add, edit, delete grades
- Students can view their grades

### Prerequisites:
* Python 3.7+
* MySQL database
* XAMPP (for MySQL) - https://www.apachefriends.org/download.html

### Installation:

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd <project-folder>
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup MySQL database:**
- Start XAMPP
- Open phpMyAdmin: http://localhost/phpmyadmin
- Create a database named 'user'

5. **Run the application:**
```bash
python main.py
```

6. **Access the app:**
Open http://localhost:5000 in your browser

## Usage
1. Register as either Teacher or Student
2. Teachers can create subjects and manage grades
3. Students can view their grades and see which teacher assigned them

### Libraries Used
- Flask: A web framework for Python.
- Flask-Login: Provides user session management for Flask.
- Flask-SQLAlchemy: Adds SQLAlchemy support to Flask.
- Werkzeug: A WSGI utility library for Python.

### Additional Notes:
1. User passwords are hashed using Werkzeug for security.
2. SQLAlchemy is used to interact with the MySQL database.
3. User input is validated using Python validation processes.

#### Author

Gabriel Mokhele


Feel free to add any home page of your choice and implement backend python code to add functionality to its front end with additional features like CSS & JS static files etc.

