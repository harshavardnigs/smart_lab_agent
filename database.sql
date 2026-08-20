-- =========================================================
-- SMARTLAB DATABASE
-- =========================================================

CREATE SCHEMA IF NOT EXISTS SMARTLAB;


-- =========================================================
-- 1. USERS
-- Students, Faculty and Lab Managers
-- =========================================================

CREATE TABLE SMARTLAB.USERS (

    user_id DECIMAL(10,0) IDENTITY PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(200) NOT NULL UNIQUE,

    role VARCHAR(20) NOT NULL

);


-- =========================================================
-- 2. EQUIPMENT
-- All laboratory equipment
-- =========================================================

CREATE TABLE SMARTLAB.EQUIPMENT (

    equipment_id DECIMAL(10,0) IDENTITY PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    equipment_type VARCHAR(100),

    availability VARCHAR(30) NOT NULL,

    health_score DECIMAL(5,2),

    maintenance_date DATE,

    status VARCHAR(30),

    CONSTRAINT chk_health_score
        CHECK (health_score >= 0 AND health_score <= 100)

);


-- =========================================================
-- 3. BOOKINGS
-- Equipment reservations made by users
-- =========================================================

CREATE TABLE SMARTLAB.BOOKINGS (

    booking_id DECIMAL(10,0) IDENTITY PRIMARY KEY,

    user_id DECIMAL(10,0) NOT NULL,

    equipment_id DECIMAL(10,0) NOT NULL,

    booking_date DATE NOT NULL,

    start_time VARCHAR(10) NOT NULL,

    end_time VARCHAR(10) NOT NULL,

    status VARCHAR(30) NOT NULL,

    CONSTRAINT fk_booking_user
        FOREIGN KEY (user_id)
        REFERENCES SMARTLAB.USERS(user_id),

    CONSTRAINT fk_booking_equipment
        FOREIGN KEY (equipment_id)
        REFERENCES SMARTLAB.EQUIPMENT(equipment_id)

);


-- =========================================================
-- 4. USAGE HISTORY
-- Records how equipment has been used
-- =========================================================

CREATE TABLE SMARTLAB.USAGE_HISTORY (

    usage_id DECIMAL(10,0) IDENTITY PRIMARY KEY,

    equipment_id DECIMAL(10,0) NOT NULL,

    user_id DECIMAL(10,0) NOT NULL,

    usage_date DATE NOT NULL,

    start_time VARCHAR(10),

    end_time VARCHAR(10),

    duration_minutes DECIMAL(10,0),

    CONSTRAINT fk_usage_equipment
        FOREIGN KEY (equipment_id)
        REFERENCES SMARTLAB.EQUIPMENT(equipment_id),

    CONSTRAINT fk_usage_user
        FOREIGN KEY (user_id)
        REFERENCES SMARTLAB.USERS(user_id)

);


-- =========================================================
-- 5. ISSUES
-- Problems reported with equipment
-- =========================================================

CREATE TABLE SMARTLAB.ISSUES (

    issue_id DECIMAL(10,0) IDENTITY PRIMARY KEY,

    equipment_id DECIMAL(10,0) NOT NULL,

    reported_by DECIMAL(10,0) NOT NULL,

    description VARCHAR(500) NOT NULL,

    priority VARCHAR(20) NOT NULL,

    status VARCHAR(30) NOT NULL,

    reported_date DATE NOT NULL,

    CONSTRAINT fk_issue_equipment
        FOREIGN KEY (equipment_id)
        REFERENCES SMARTLAB.EQUIPMENT(equipment_id),

    CONSTRAINT fk_issue_user
        FOREIGN KEY (reported_by)
        REFERENCES SMARTLAB.USERS(user_id)

);


-- =========================================================
-- 6. NOTIFICATIONS
-- Notifications sent to users
-- =========================================================

CREATE TABLE SMARTLAB.NOTIFICATIONS (

    notification_id DECIMAL(10,0) IDENTITY PRIMARY KEY,

    user_id DECIMAL(10,0) NOT NULL,

    message VARCHAR(500) NOT NULL,

    priority VARCHAR(20) NOT NULL,

    is_read BOOLEAN DEFAULT FALSE,

    created_date DATE,

    CONSTRAINT fk_notification_user
        FOREIGN KEY (user_id)
        REFERENCES SMARTLAB.USERS(user_id)

);


-- =========================================================
-- SAMPLE DATA
-- =========================================================


-- USERS

INSERT INTO SMARTLAB.USERS
    (name, email, role)
VALUES
    ('Arun Kumar', 'arun@student.com', 'Student'),
    ('Priya Sharma', 'priya@faculty.com', 'Faculty'),
    ('Rahul Manager', 'rahul@lab.com', 'Lab Manager');


-- EQUIPMENT

INSERT INTO SMARTLAB.EQUIPMENT
    (name, equipment_type, availability, health_score, maintenance_date, status)
VALUES
    ('Oscilloscope 01', 'Oscilloscope', 'Available', 94.00, '2026-09-15', 'Operational'),

    ('Oscilloscope 02', 'Oscilloscope', 'Booked', 91.00, '2026-10-10', 'Operational'),

    ('Power Supply 01', 'Power Supply', 'Unavailable', 63.00, '2026-08-25', 'Maintenance'),

    ('Function Generator 01', 'Function Generator', 'Available', 88.00, '2026-11-05', 'Operational'),

    ('Digital Multimeter 01', 'Multimeter', 'Available', 97.00, '2027-01-15', 'Operational');


-- BOOKINGS

INSERT INTO SMARTLAB.BOOKINGS
    (user_id, equipment_id, booking_date, start_time, end_time, status)
VALUES
    (1, 1, '2026-08-20', '10:00', '11:00', 'Confirmed'),

    (2, 2, '2026-08-20', '14:00', '15:00', 'Confirmed');


-- USAGE HISTORY

INSERT INTO SMARTLAB.USAGE_HISTORY
    (equipment_id, user_id, usage_date, start_time, end_time, duration_minutes)
VALUES
    (1, 1, '2026-08-18', '10:00', '11:30', 90),

    (2, 2, '2026-08-18', '14:00', '15:00', 60),

    (1, 1, '2026-08-17', '09:00', '10:00', 60);


-- ISSUES

INSERT INTO SMARTLAB.ISSUES
    (equipment_id, reported_by, description, priority, status, reported_date)
VALUES
    (3, 1, 'Power supply output is unstable', 'High', 'Open', '2026-08-19');


-- NOTIFICATIONS

INSERT INTO SMARTLAB.NOTIFICATIONS
    (user_id, message, priority, is_read, created_date)
VALUES
    (3, 'Power Supply 01 requires maintenance', 'High', FALSE, '2026-08-19'),

    (1, 'Your Oscilloscope 01 booking is confirmed', 'Medium', FALSE, '2026-08-19');