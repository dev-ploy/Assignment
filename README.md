CAMPUS EVENT MANAGEMENT PLATFORM 

The Campus Event Management Platform is a web-based application designed to streamline event management for educational institutions. It provides a comprehensive solution for creating, managing, and tracking campus events with features for student registration, attendance tracking, and feedback collection.

For The Code Design: /Documentation/Docs.MD


FEATURES
Event creation and management
Student registration system
Attendance tracking
Feedback collection
Reporting and analytics
Admin and Student portals
Responsive design

TECHNOLOGY STACK 
Backend: Python Flask
Database: MySQL 
Frontend: HTML5, CSS3, JavaScript, Bootstrap 
Icons: Font Awesome
CORS: Flask-CORS 

PREREQUISITES
Python 3.10+
pip (Python package manager)
Web browser (Chrome, Firefox, Safari, Edge)

PROJECT STRUCTURE
campus-event-management/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── database_schema_sqlite.sql  # Database schema
├── templates/            # HTML templates
│   ├── index.html
│   ├── admin.html
│   └── student.html
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── admin.js
│       └── student.js
└── campus_events.db     # SQLite database

SCREENSHOTS
check the logs folder for conversation with LLM tool (Claude being used in this case)

DEPENDENCIES INSTALLATION
pip install -r requirements.txt

RUN THE APPLICATION
cd backend
python app.py 

ACCESS THE APPLICATION
MAIN URL:http://localhost:5000
ADMIN PORTAL: http://localhost:5000/admin
STUDENT PORTAL: http://localhost:5000/student

