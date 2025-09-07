Purpose of this Project:
The Campus Event Management Platform is a web-based application designed to streamline event management for educational institutions. It provides a comprehensive solution for creating, managing, and tracking campus events with features for student registration, attendance tracking, and feedback collection.

This project follows:
CRUD operations -> Create,view,update and delete campus events
Registration of users (students)->allows students to register for events
Tracking->to track the attendance of student
Report analysis->to generate the comprehensive reports
Multi User Support->can login as A student and an admin 

Target Audience is Event organizers,faculty,stuff,campus,community memebers and educational organizations

Tech Stack:
Backend- Flask (Microweb framework)
Frontend - Html-5 , Css-3, JS(ES6+)
Database- Mysql
UI- Bootstrap 5
Icons- Font Awesome
Cors- Flask-CORS 4

Database Design:

Entity Relationship Diagram

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Colleges   │    │  Students   │    │Event Types  │
│             │    │             │    │             │
│ college_id  │◄───┤ college_id  │    │ type_id     │
│ college_name│    │ student_id  │    │ type_name   │
│ college_code│    │ student_name│    └─────────────┘
└─────────────┘    │ email       │           │
                   │ student_id_#│           │
                   └─────────────┘           │
                          │                  │
                          │                  │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Events    │    │Registrations│    │ Attendance  │
│             │    │             │    │             │
│ event_id    │◄───┤ event_id    │    │ event_id    │
│ college_id  │    │ student_id  │    │ student_id  │
│ event_name  │    │ status      │    │ status      │
│ event_type_id│   │ reg_date    │    │ check_in    │
│ event_date  │    └─────────────┘    └─────────────┘
│ event_time  │
│ location    │
│ max_capacity│
└─────────────┘
       │
       │
┌─────────────┐
│  Feedback   │
│             │
│ event_id    │
│ student_id  │
│ rating      │
│ comments    │
└─────────────┘
```
Database Schema Details
1.Colleges Table
2.Students Table
3.Event Types
4.Events
5.Registrations
6.Attendance
7.Feedback

API Design

Event Management

GET    /api/events              # Get all events (with optional filtering)
POST   /api/events              # Create new event
GET    /api/events/{id}         # Get specific event
PUT    /api/events/{id}         # Update event
DELETE /api/events/{id}         # Delete event

Student Management

GET    /api/students            # Get all students
POST   /api/students            # Create new student
GET    /api/students/{id}       # Get specific student
PUT    /api/students/{id}       # Update student
DELETE /api/students/{id}       # Delete student

Registration System

POST   /api/register            # Register student for event
DELETE /api/register/{id}       # Cancel registration
GET    /api/registrations       # Get all registrations

Attendance System

OST   /api/attendance          # Mark attendance
GET    /api/attendance          # Get attendance records
PUT    /api/attendance/{id}     # Update attendance

Feedback System

POST   /api/feedback            # Submit feedback
GET    /api/feedback            # Get feedback records
PUT    /api/feedback/{id}       # Update feedback

Reporting & Analytics

GET    /api/reports/event-popularity        # Event popularity report
GET    /api/reports/student-participation   # Student participation report
GET    /api/reports/top-active-students     # Top active students
GET    /api/reports/attendance-summary      # Attendance summary

Utility Endpoints

ET    /api/event-types         # Get all event types
GET    /api/colleges            # Get all colleges

API respone format -> JSON

Additional:
Deployement- using netlify or render
Containerzation - Docker
Orchestration - Kubernetes 
CI/CD pipeline - GitLab

Improvements:
Django can be used to scale the platform 
Postgres SQL or MongoDB to store multiple student records 
React OR Angular or Next-JS to improve the UI design
FastApi to create modular and secure API endpoints

