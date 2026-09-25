-- ==============================================================================
-- Student Record Management System - Seed Data
-- Realistic sample records for testing and demonstration
-- ==============================================================================

-- 1. Departments
INSERT INTO departments (id, code, name, description, status) VALUES
(1, 'CS', 'Computer Science & Engineering', 'Undergraduate department focusing on algorithms, software architecture, and artificial intelligence.', 'Active'),
(2, 'EE', 'Electrical & Electronics Engineering', 'Department dedicated to circuit design, power systems, and microelectronics.', 'Active'),
(3, 'ME', 'Mechanical Engineering', 'Programs covering thermodynamics, robotics, and CAD manufacturing engineering.', 'Active'),
(4, 'BA', 'Business Administration', 'School of management covering finance, marketing, and organizational leadership.', 'Active')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- 2. Students
INSERT INTO students (id, admission_number, first_name, last_name, gender, date_of_birth, phone_number, email, address, department_id, year, guardian_name, guardian_phone, admission_date, status) VALUES
(1, 'ADM-2023-001', 'Alexander', 'Wright', 'Male', '2004-03-15', '+1-555-0101', 'a.wright@example.com', '742 Evergreen Terrace, Springfield, OR', 1, 2, 'Robert Wright', '+1-555-9101', '2023-08-20', 'Active'),
(2, 'ADM-2023-002', 'Sophia', 'Chen', 'Female', '2004-07-22', '+1-555-0102', 's.chen@example.com', '124 Conch Street, Pacific Grove, CA', 1, 2, 'David Chen', '+1-555-9102', '2023-08-20', 'Active'),
(3, 'ADM-2022-045', 'Marcus', 'Johnson', 'Male', '2003-11-09', '+1-555-0103', 'm.johnson@example.com', '884 Elm Avenue, Seattle, WA', 2, 3, 'Patricia Johnson', '+1-555-9103', '2022-08-15', 'Active'),
(4, 'ADM-2024-101', 'Elena', 'Rodriguez', 'Female', '2005-01-30', '+1-555-0104', 'e.rodriguez@example.com', '312 Maple Drive, Austin, TX', 1, 1, 'Carlos Rodriguez', '+1-555-9104', '2024-08-22', 'Active'),
(5, 'ADM-2022-089', 'Liam', 'O''Connor', 'Male', '2003-05-18', '+1-555-0105', 'l.oconnor@example.com', '56 Pine Street, Boston, MA', 3, 3, 'Fiona O''Connor', '+1-555-9105', '2022-08-15', 'Active'),
(6, 'ADM-2024-118', 'Amina', 'Patel', 'Female', '2005-09-12', '+1-555-0106', 'a.patel@example.com', '901 Cedar Boulevard, Denver, CO', 4, 1, 'Suresh Patel', '+1-555-9106', '2024-08-22', 'Active'),
(7, 'ADM-2021-012', 'Ethan', 'Miller', 'Male', '2002-12-04', '+1-555-0107', 'e.miller@example.com', '440 Birch Lane, Minneapolis, MN', 3, 4, 'Sarah Miller', '+1-555-9107', '2021-08-18', 'Active'),
(8, 'ADM-2023-055', 'Chloe', 'Dubois', 'Female', '2004-04-28', '+1-555-0108', 'c.dubois@example.com', '710 Oak Ridge Road, Atlanta, GA', 4, 2, 'Henri Dubois', '+1-555-9108', '2023-08-20', 'Active'),
(9, 'ADM-2022-130', 'Lucas', 'Silva', 'Male', '2003-08-14', '+1-555-0109', 'l.silva@example.com', '225 Willow Way, Miami, FL', 2, 3, 'Isabella Silva', '+1-555-9109', '2022-08-15', 'Active'),
(10, 'ADM-2024-142', 'Zoe', 'Kowalski', 'Female', '2005-06-03', '+1-555-0110', 'z.kowalski@example.com', '180 Walnut Court, Chicago, IL', 1, 1, 'Jan Kowalski', '+1-555-9110', '2024-08-22', 'Active'),
(11, 'ADM-2021-098', 'Daniel', 'Kim', 'Male', '2002-02-19', '+1-555-0111', 'd.kim@example.com', '633 Highland Park, San Jose, CA', 1, 4, 'Grace Kim', '+1-555-9111', '2021-08-18', 'Active'),
(12, 'ADM-2023-088', 'Maya', 'Abebe', 'Female', '2004-10-10', '+1-555-0112', 'm.abebe@example.com', '502 River Street, Portland, OR', 2, 2, 'Dawit Abebe', '+1-555-9112', '2023-08-20', 'Inactive')
ON DUPLICATE KEY UPDATE admission_number=VALUES(admission_number);

-- 3. Attendance Records
INSERT INTO attendance (student_id, attendance_date, status, remarks) VALUES
(1, '2026-09-21', 'Present', 'On time'),
(2, '2026-09-21', 'Present', 'On time'),
(3, '2026-09-21', 'Present', 'On time'),
(4, '2026-09-21', 'Late', 'Late by 10 mins (traffic)'),
(5, '2026-09-21', 'Present', 'On time'),
(6, '2026-09-21', 'Absent', 'Medical leave'),
(7, '2026-09-21', 'Present', 'On time'),
(8, '2026-09-21', 'Present', 'On time'),
(9, '2026-09-21', 'Present', 'On time'),
(10, '2026-09-21', 'Present', 'On time'),
(11, '2026-09-21', 'Present', 'On time'),
(1, '2026-09-22', 'Present', 'On time'),
(2, '2026-09-22', 'Present', 'On time'),
(3, '2026-09-22', 'Late', 'Transit delay'),
(4, '2026-09-22', 'Present', 'On time'),
(5, '2026-09-22', 'Present', 'On time'),
(6, '2026-09-22', 'Present', 'On time'),
(7, '2026-09-22', 'Absent', 'Family emergency'),
(8, '2026-09-22', 'Present', 'On time'),
(9, '2026-09-22', 'Present', 'On time'),
(10, '2026-09-22', 'Present', 'On time'),
(11, '2026-09-22', 'Present', 'On time'),
(1, '2026-09-23', 'Present', 'On time'),
(2, '2026-09-23', 'Present', 'On time'),
(3, '2026-09-23', 'Present', 'On time'),
(4, '2026-09-23', 'Present', 'On time'),
(5, '2026-09-23', 'Present', 'On time'),
(6, '2026-09-23', 'Present', 'On time'),
(7, '2026-09-23', 'Present', 'On time'),
(8, '2026-09-23', 'Late', 'Late check-in'),
(9, '2026-09-23', 'Present', 'On time'),
(10, '2026-09-23', 'Present', 'On time'),
(11, '2026-09-23', 'Present', 'On time')
ON DUPLICATE KEY UPDATE status=VALUES(status);

-- 4. Marks / Exam Records
INSERT INTO marks (student_id, subject, exam_name, marks_obtained, max_marks, percentage, grade, remarks) VALUES
(1, 'Data Structures & Algorithms', 'Sem Exam', 92.50, 100.00, 92.50, 'A+', 'Outstanding code implementation'),
(1, 'Database Systems', 'Sem Exam', 88.00, 100.00, 88.00, 'A', 'Strong SQL knowledge'),
(2, 'Data Structures & Algorithms', 'Sem Exam', 95.00, 100.00, 95.00, 'A+', 'Top score in cohort'),
(2, 'Database Systems', 'Sem Exam', 91.00, 100.00, 91.00, 'A+', 'Clean normalization solution'),
(3, 'Digital Signal Processing', 'Sem Exam', 78.50, 100.00, 78.50, 'B', 'Good theoretical understanding'),
(3, 'Electromagnetic Fields', 'Sem Exam', 72.00, 100.00, 72.00, 'B', 'Satisfactory progress'),
(4, 'Introduction to Programming', 'Quiz 1', 94.00, 100.00, 94.00, 'A+', 'Excellent syntax and logic'),
(4, 'Calculus I', 'Sem Exam', 86.50, 100.00, 86.50, 'A', 'Strong problem solving'),
(5, 'Thermodynamics', 'Sem Exam', 82.00, 100.00, 82.00, 'A', 'Well structured formulas'),
(5, 'Fluid Mechanics', 'Sem Exam', 67.50, 100.00, 67.50, 'C', 'Needs practice with Navier-Stokes'),
(6, 'Principles of Management', 'Sem Exam', 89.00, 100.00, 89.00, 'A', 'Comprehensive essay answers'),
(6, 'Financial Accounting', 'Sem Exam', 93.00, 100.00, 93.00, 'A+', 'Accurate ledger balancing'),
(7, 'Robotics & Automation', 'Final Exam', 91.50, 100.00, 91.50, 'A+', 'Exceptional project demo'),
(8, 'Marketing Strategy', 'Sem Exam', 85.00, 100.00, 85.00, 'A', 'Creative campaign proposal'),
(9, 'Microcontrollers', 'Sem Exam', 79.00, 100.00, 79.00, 'B', 'Solid embedded C code'),
(10, 'Introduction to Programming', 'Quiz 1', 90.00, 100.00, 90.00, 'A+', 'Great coding habits'),
(11, 'Cloud Architecture', 'Final Project', 96.00, 100.00, 96.00, 'A+', 'Production-grade deployment')
ON DUPLICATE KEY UPDATE marks_obtained=VALUES(marks_obtained);
