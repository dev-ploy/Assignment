<<<<<<< HEAD
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(id),
    user_id INT REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
=======
-- Campus Event Management Platform Database Schema
-- Designed for ~50 colleges, ~500 students each, ~20 events per semester

-- Colleges table
CREATE TABLE colleges (
    college_id INT PRIMARY KEY AUTO_INCREMENT,
    college_name VARCHAR(255) NOT NULL,
    college_code VARCHAR(10) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    college_id INT NOT NULL,
    student_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    student_id_number VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges(college_id),
    UNIQUE KEY unique_student_per_college (college_id, student_id_number)
);

-- Event types for flexible filtering
CREATE TABLE event_types (
    type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(100) NOT NULL UNIQUE
);

-- Events table
CREATE TABLE events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    college_id INT NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    event_description TEXT,
    event_type_id INT NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    location VARCHAR(255),
    max_capacity INT DEFAULT NULL,
    created_by VARCHAR(255) NOT NULL, -- Admin who created the event
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges(college_id),
    FOREIGN KEY (event_type_id) REFERENCES event_types(type_id)
);

-- Event registrations
CREATE TABLE event_registrations (
    registration_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    student_id INT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('registered', 'cancelled') DEFAULT 'registered',
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    UNIQUE KEY unique_registration (event_id, student_id)
);

-- Attendance tracking
CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    student_id INT NOT NULL,
    check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('present', 'absent') DEFAULT 'present',
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    UNIQUE KEY unique_attendance (event_id, student_id)
);

-- Feedback system
CREATE TABLE feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    student_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comments TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    UNIQUE KEY unique_feedback (event_id, student_id)
);

-- Insert sample event types
INSERT INTO event_types (type_name) VALUES 
('Workshop'),
('Hackathon'),
('Tech Talk'),
('Fest'),
('Seminar'),
('Conference'),
('Competition');

-- Insert sample college
INSERT INTO colleges (college_name, college_code) VALUES 
('Sample University', 'SU001');

-- Insert sample students
INSERT INTO students (college_id, student_name, email, student_id_number) VALUES 
(1, 'John Doe', 'john.doe@sample.edu', 'SU001001'),
(1, 'Jane Smith', 'jane.smith@sample.edu', 'SU001002'),
(1, 'Mike Johnson', 'mike.johnson@sample.edu', 'SU001003'),
(1, 'Sarah Wilson', 'sarah.wilson@sample.edu', 'SU001004'),
(1, 'David Brown', 'david.brown@sample.edu', 'SU001005');

-- Insert sample events
INSERT INTO events (college_id, event_name, event_description, event_type_id, event_date, event_time, location, max_capacity, created_by) VALUES 
(1, 'Python Workshop', 'Learn Python programming basics', 1, '2024-02-15', '10:00:00', 'Computer Lab 1', 30, 'Admin'),
(1, 'Tech Fest 2024', 'Annual technology festival', 4, '2024-02-20', '09:00:00', 'Main Auditorium', 200, 'Admin'),
(1, 'AI Seminar', 'Introduction to Artificial Intelligence', 5, '2024-02-25', '14:00:00', 'Lecture Hall 2', 50, 'Admin'),
(1, 'Hackathon 2024', '24-hour coding competition', 2, '2024-03-01', '08:00:00', 'Innovation Center', 100, 'Admin');
>>>>>>> ad9e91c (Added the Code files)
