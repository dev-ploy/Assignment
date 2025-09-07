from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime, date, timedelta
import json

# Custom JSON encoder to handle datetime and timedelta objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            return str(obj)
        return super().default(obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
CORS(app)

# Database configuration
DB_PATH = 'campus_events.db'

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row  # This enables column access by name
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def init_database():
    """Initialize the database with tables and sample data"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Read and execute the SQL schema
        with open('database_schema_sqlite.sql', 'r') as f:
            sql_script = f.read()
        
        # Split the script into individual statements and execute them
        statements = sql_script.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        connection.commit()
        print("Database initialized successfully!")
        return True
        
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        if connection:
            connection.close()

# Routes for Admin Portal

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/admin')
def admin_portal():
    """Admin portal for creating events"""
    return render_template('admin.html')

@app.route('/student')
def student_portal():
    """Student portal for browsing and registering events"""
    return render_template('student.html')

# API Routes

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events with optional filtering"""
    college_id = request.args.get('college_id', 1)
    event_type = request.args.get('event_type')
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT e.*, et.type_name, c.college_name,
               COUNT(er.registration_id) as registration_count,
               COUNT(a.attendance_id) as attendance_count
        FROM events e
        JOIN event_types et ON e.event_type_id = et.type_id
        JOIN colleges c ON e.college_id = c.college_id
        LEFT JOIN event_registrations er ON e.event_id = er.event_id AND er.status = 'registered'
        LEFT JOIN attendance a ON e.event_id = a.event_id AND a.status = 'present'
        WHERE e.college_id = ?
        """
        params = [college_id]
        
        if event_type:
            query += " AND et.type_name = ?"
            params.append(event_type)
        
        query += " GROUP BY e.event_id ORDER BY e.event_date DESC"
        
        cursor.execute(query, params)
        events = cursor.fetchall()
        
        # Convert Row objects to dictionaries
        events_list = []
        for event in events:
            events_list.append(dict(event))
        
        return jsonify(events_list)
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/events', methods=['POST'])
def create_event():
    """Create a new event"""
    data = request.json
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        query = """
        INSERT INTO events (college_id, event_name, event_description, event_type_id, 
                           event_date, event_time, location, max_capacity, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            data['college_id'],
            data['event_name'],
            data['event_description'],
            data['event_type_id'],
            data['event_date'],
            data['event_time'],
            data['location'],
            data.get('max_capacity'),
            data['created_by']
        )
        
        cursor.execute(query, values)
        connection.commit()
        
        return jsonify({'message': 'Event created successfully', 'event_id': cursor.lastrowid})
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students"""
    college_id = request.args.get('college_id', 1)
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM students WHERE college_id = ? ORDER BY student_name"
        cursor.execute(query, [college_id])
        students = cursor.fetchall()
        
        # Convert Row objects to dictionaries
        students_list = []
        for student in students:
            students_list.append(dict(student))
        
        return jsonify(students_list)
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/register', methods=['POST'])
def register_student():
    """Register a student for an event"""
    data = request.json
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Check if already registered
        check_query = "SELECT registration_id FROM event_registrations WHERE event_id = ? AND student_id = ?"
        cursor.execute(check_query, (data['event_id'], data['student_id']))
        
        if cursor.fetchone():
            return jsonify({'error': 'Student already registered for this event'}), 400
        
        # Register student
        insert_query = """
        INSERT INTO event_registrations (event_id, student_id)
        VALUES (?, ?)
        """
        cursor.execute(insert_query, (data['event_id'], data['student_id']))
        connection.commit()
        
        return jsonify({'message': 'Registration successful'})
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    """Mark attendance for an event"""
    data = request.json
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Check if already marked
        check_query = "SELECT attendance_id FROM attendance WHERE event_id = ? AND student_id = ?"
        cursor.execute(check_query, (data['event_id'], data['student_id']))
        
        if cursor.fetchone():
            return jsonify({'error': 'Attendance already marked for this event'}), 400
        
        # Mark attendance
        insert_query = """
        INSERT INTO attendance (event_id, student_id, status)
        VALUES (?, ?, ?)
        """
        cursor.execute(insert_query, (data['event_id'], data['student_id'], data['status']))
        connection.commit()
        
        return jsonify({'message': 'Attendance marked succescsfully'})
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback for an event"""
    data = request.json
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        # Check if feedback already submitted
        check_query = "SELECT feedback_id FROM feedback WHERE event_id = ? AND student_id = ?"
        cursor.execute(check_query, (data['event_id'], data['student_id']))
        
        if cursor.fetchone():
            return jsonify({'error': 'Feedback already submitted for this event'}), 400
        
        # Submit feedback
        insert_query = """
        INSERT INTO feedback (event_id, student_id, rating, comments)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(insert_query, (data['event_id'], data['student_id'], data['rating'], data.get('comments', '')))
        connection.commit()
        
        return jsonify({'message': 'Feedback submitted successfully'})
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

# Report Routes

@app.route('/api/reports/event-popularity')
def event_popularity_report():
    """Generate event popularity report (sorted by registrations)"""
    college_id = request.args.get('college_id', 1)
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        query = """
        SELECT e.event_name, et.type_name, e.event_date,
               COUNT(er.registration_id) as total_registrations,
               COUNT(a.attendance_id) as attendance_count,
               ROUND((COUNT(a.attendance_id) * 100.0 / COUNT(er.registration_id)), 2) as attendance_percentage,
               ROUND(AVG(f.rating), 2) as average_rating
        FROM events e
        JOIN event_types et ON e.event_type_id = et.type_id
        LEFT JOIN event_registrations er ON e.event_id = er.event_id AND er.status = 'registered'
        LEFT JOIN attendance a ON e.event_id = a.event_id AND a.status = 'present'
        LEFT JOIN feedback f ON e.event_id = f.event_id
        WHERE e.college_id = ?
        GROUP BY e.event_id
        ORDER BY total_registrations DESC
        """
        cursor.execute(query, [college_id])
        report = cursor.fetchall()
        
        # Convert Row objects to dictionaries
        report_list = []
        for row in report:
            report_list.append(dict(row))
        
        return jsonify(report_list)
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/reports/student-participation')
def student_participation_report():
    """Generate student participation report"""
    college_id = request.args.get('college_id', 1)
    student_id = request.args.get('student_id')
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        
        if student_id:
            # Specific student report
            query = """
            SELECT s.student_name, s.email,
                   COUNT(er.registration_id) as events_registered,
                   COUNT(a.attendance_id) as events_attended,
                   ROUND((COUNT(a.attendance_id) * 100.0 / COUNT(er.registration_id)), 2) as attendance_rate
            FROM students s
            LEFT JOIN event_registrations er ON s.student_id = er.student_id AND er.status = 'registered'
            LEFT JOIN attendance a ON s.student_id = a.student_id AND a.status = 'present'
            WHERE s.student_id = ? AND s.college_id = ?
            GROUP BY s.student_id
            """
            cursor.execute(query, (student_id, college_id))
        else:
            # All students report
            query = """
            SELECT s.student_name, s.email,
                   COUNT(er.registration_id) as events_registered,
                   COUNT(a.attendance_id) as events_attended,
                   ROUND((COUNT(a.attendance_id) * 100.0 / COUNT(er.registration_id)), 2) as attendance_rate
            FROM students s
            LEFT JOIN event_registrations er ON s.student_id = er.student_id AND er.status = 'registered'
            LEFT JOIN attendance a ON s.student_id = a.student_id AND a.status = 'present'
            WHERE s.college_id = ?
            GROUP BY s.student_id
            ORDER BY events_attended DESC
            """
            cursor.execute(query, [college_id])
        
        report = cursor.fetchall()
        
        # Convert Row objects to dictionaries
        report_list = []
        for row in report:
            report_list.append(dict(row))
        
        return jsonify(report_list)
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/reports/top-active-students')
def top_active_students_report():
    """Generate top 3 most active students report"""
    college_id = request.args.get('college_id', 1)
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        query = """
        SELECT s.student_name, s.email,
               COUNT(er.registration_id) as events_registered,
               COUNT(a.attendance_id) as events_attended,
               ROUND((COUNT(a.attendance_id) * 100.0 / COUNT(er.registration_id)), 2) as attendance_rate
        FROM students s
        LEFT JOIN event_registrations er ON s.student_id = er.student_id AND er.status = 'registered'
        LEFT JOIN attendance a ON s.student_id = a.student_id AND a.status = 'present'
        WHERE s.college_id = ?
        GROUP BY s.student_id
        HAVING events_registered > 0
        ORDER BY events_attended DESC, events_registered DESC
        LIMIT 3
        """
        cursor.execute(query, [college_id])
        report = cursor.fetchall()
        
        # Convert Row objects to dictionaries
        report_list = []
        for row in report:
            report_list.append(dict(row))
        
        return jsonify(report_list)
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/event-types')
def get_event_types():
    """Get all event types"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM event_types ORDER BY type_name"
        cursor.execute(query)
        event_types = cursor.fetchall()
        
        # Convert Row objects to dictionaries
        event_types_list = []
        for event_type in event_types:
            event_types_list.append(dict(event_type))
        
        return jsonify(event_types_list)
    
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    # Initialize database on startup
    if not os.path.exists(DB_PATH):
        print("Initializing database...")
        init_database()
    
    app.run(debug=True, host='0.0.0.0', port=5000)