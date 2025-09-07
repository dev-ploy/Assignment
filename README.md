# Campus Event Management Platform

The Campus Event Management Platform is a web-based application designed to help educational institutions organize and manage campus events efficiently. It provides tools for creating and tracking events, handling student registrations, monitoring attendance, and collecting feedback.

## Documentation

You can find information about the code design and architecture in `/Documentation/Docs.MD`.

## Features

- Event creation and management
- Student registration system
- Attendance tracking
- Feedback collection
- Reporting and analytics
- Separate portals for administrators and students
- Responsive design for all devices

## Technology Stack

- Backend: Python Flask
- Database: MySQL
- Frontend: HTML5, CSS3, JavaScript, Bootstrap
- Icons: Font Awesome
- CORS: Flask-CORS

## Prerequisites

- Python 3.10 or newer
- pip (Python package manager)
- A modern web browser (Chrome, Firefox, Safari, Edge)

## Project Structure

```
campus-event-management/
├── app.py                       # Main Flask application
├── requirements.txt             # Python dependencies
├── database_schema_sqlite.sql   # Database schema (SQLite format)
├── templates/                   # HTML templates
│   ├── index.html
│   ├── admin.html
│   └── student.html
├── static/                      # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── admin.js
│       └── student.js
└── campus_events.db             # SQLite database
```

## Screenshots

Screenshots and logs of conversations (with Claude) are available in the `logs` folder.

## Installation

1. Install dependencies using pip:
    ```
    pip install -r requirements.txt
    ```

2. Run the application:
    ```
    cd backend
    python app.py
    ```

## Accessing the Application

- Main URL: http://localhost:5000
- Admin Portal: http://localhost:5000/admin
- Student Portal: http://localhost:5000/student

---

This platform helps make campus events more organized, interactive, and data-driven.
