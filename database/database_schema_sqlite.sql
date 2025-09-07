-- Campus Event Management Platform Database Schema (SQLite)
-- Designed for ~50 colleges, ~500 students each, ~20 events per semester

-- Colleges table
CREATE TABLE IF NOT EXISTS colleges (
    college_id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_name TEXT NOT NULL,
    college_code TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    student_id_number TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges(college_id),
    UNIQUE (college_id, student_id_number)
);

-- Event types for flexible filtering
CREATE TABLE IF NOT EXISTS event_types (
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL UNIQUE
);

-- Events table
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_id INTEGER NOT NULL,
    event_name TEXT NOT NULL,
    event_description TEXT,
    event_type_id INTEGER NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    location TEXT,
    max_capacity INTEGER DEFAULT NULL,
    created_by TEXT NOT NULL, -- Admin who created the event
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges(college_id),
    FOREIGN KEY (event_type_id) REFERENCES event_types(type_id)
);

-- Event registrations
CREATE TABLE IF NOT EXISTS event_registrations (
    registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'registered' CHECK (status IN ('registered', 'cancelled')),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    UNIQUE (event_id, student_id)
);

-- Attendance tracking
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'present' CHECK (status IN ('present', 'absent')),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    UNIQUE (event_id, student_id)
);

-- Feedback system
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    UNIQUE (event_id, student_id)
);

-- Insert sample event types
INSERT OR IGNORE INTO event_types (type_name) VALUES 
('Workshop'),
('Hackathon'),
('Tech Talk'),
('Fest'),
('Seminar'),
('Conference'),
('Competition');

-- Insert sample college
INSERT OR IGNORE INTO colleges (college_name, college_code) VALUES 
('Sample University', 'SU001');

-- Insert sample students
INSERT OR IGNORE INTO students (college_id, student_name, email, student_id_number) VALUES 
(1, 'John Doe', 'john.doe@sample.edu', 'SU001001'),
(1, 'Jane Smith', 'jane.smith@sample.edu', 'SU001002'),
(1, 'Mike Johnson', 'mike.johnson@sample.edu', 'SU001003'),
(1, 'Sarah Wilson', 'sarah.wilson@sample.edu', 'SU001004'),
(1, 'David Brown', 'david.brown@sample.edu', 'SU001005');

-- Insert sample events
INSERT OR IGNORE INTO events (college_id, event_name, event_description, event_type_id, event_date, event_time, location, max_capacity, created_by) VALUES 
(1, 'Python Workshop', 'Learn Python programming basics', 1, '2024-02-15', '10:00:00', 'Computer Lab 1', 30, 'Admin'),
(1, 'Tech Fest 2024', 'Annual technology festival', 4, '2024-02-20', '09:00:00', 'Main Auditorium', 200, 'Admin'),
(1, 'AI Seminar', 'Introduction to Artificial Intelligence', 5, '2024-02-25', '14:00:00', 'Lecture Hall 2', 50, 'Admin'),
(1, 'Hackathon 2024', '24-hour coding competition', 2, '2024-03-01', '08:00:00', 'Innovation Center', 100, 'Admin');
