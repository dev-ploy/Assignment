import sqlite3

def add_sample_registrations():
    """Add sample event registrations and attendance to make students active"""
    DB_PATH = 'campus_events.db'
    
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    
    try:
        cursor = connection.cursor()
        
        # Add sample event registrations
        registrations = [
            # Student 1 (John Doe) - registers for 3 events
            (1, 1),  # Python Workshop
            (1, 2),  # Tech Fest 2024
            (1, 3),  # AI Seminar
            
            # Student 2 (Jane Smith) - registers for 2 events
            (2, 1),  # Python Workshop
            (2, 4),  # Hackathon 2024
            
            # Student 3 (Mike Johnson) - registers for 4 events
            (3, 1),  # Python Workshop
            (3, 2),  # Tech Fest 2024
            (3, 3),  # AI Seminar
            (3, 4),  # Hackathon 2024
            
            # Student 4 (Sarah Wilson) - registers for 2 events
            (4, 2),  # Tech Fest 2024
            (4, 3),  # AI Seminar
            
            # Student 5 (David Brown) - registers for 1 event
            (5, 1),  # Python Workshop
        ]
        
        print("Adding sample event registrations...")
        for student_id, event_id in registrations:
            cursor.execute("""
                INSERT OR IGNORE INTO event_registrations (event_id, student_id)
                VALUES (?, ?)
            """, (event_id, student_id))
        
        # Add sample attendance (some students attend the events they registered for)
        attendance = [
            # John Doe attends 2 out of 3 events
            (1, 1, 'present'),  # Python Workshop
            (1, 2, 'present'),  # Tech Fest 2024
            
            # Jane Smith attends 1 out of 2 events
            (2, 1, 'present'),  # Python Workshop
            
            # Mike Johnson attends 3 out of 4 events
            (3, 1, 'present'),  # Python Workshop
            (3, 2, 'present'),  # Tech Fest 2024
            (3, 3, 'present'),  # AI Seminar
            
            # Sarah Wilson attends 2 out of 2 events
            (4, 2, 'present'),  # Tech Fest 2024
            (4, 3, 'present'),  # AI Seminar
            
            # David Brown attends 1 out of 1 event
            (5, 1, 'present'),  # Python Workshop
        ]
        
        print("Adding sample attendance...")
        for student_id, event_id, status in attendance:
            cursor.execute("""
                INSERT OR IGNORE INTO attendance (event_id, student_id, status)
                VALUES (?, ?, ?)
            """, (event_id, student_id, status))
        
        # Add sample feedback
        feedback = [
            (1, 1, 5, "Great workshop! Learned a lot about Python."),
            (1, 2, 4, "Tech Fest was amazing!"),
            (2, 1, 5, "Excellent Python workshop!"),
            (3, 1, 4, "Good introduction to Python."),
            (3, 2, 5, "Fantastic tech fest!"),
            (3, 3, 4, "AI seminar was very informative."),
            (4, 2, 5, "Tech Fest exceeded expectations!"),
            (4, 3, 4, "AI seminar was good."),
            (5, 1, 5, "Perfect Python workshop!"),
        ]
        
        print("Adding sample feedback...")
        for student_id, event_id, rating, comments in feedback:
            cursor.execute("""
                INSERT OR IGNORE INTO feedback (event_id, student_id, rating, comments)
                VALUES (?, ?, ?, ?)
            """, (event_id, student_id, rating, comments))
        
        connection.commit()
        print("Sample data added successfully!")
        
        # Show the results
        print("\n=== Current Statistics ===")
        
        # Show registrations
        cursor.execute("""
            SELECT s.student_name, COUNT(er.registration_id) as registrations
            FROM students s
            LEFT JOIN event_registrations er ON s.student_id = er.student_id
            GROUP BY s.student_id
            ORDER BY registrations DESC
        """)
        registrations = cursor.fetchall()
        print("\nStudent Registrations:")
        for row in registrations:
            print(f"  {row['student_name']}: {row['registrations']} events")
        
        # Show attendance
        cursor.execute("""
            SELECT s.student_name, COUNT(a.attendance_id) as attendance
            FROM students s
            LEFT JOIN attendance a ON s.student_id = a.student_id
            GROUP BY s.student_id
            ORDER BY attendance DESC
        """)
        attendance = cursor.fetchall()
        print("\nStudent Attendance:")
        for row in attendance:
            print(f"  {row['student_name']}: {row['attendance']} events")
        
        return True
        
    except sqlite3.Error as e:
        print(f"Error adding sample data: {e}")
        return False
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    add_sample_registrations()
