-- ======================================================
-- STUDENT PLACEMENT MANAGEMENT SYSTEM - COMPLETE SCHEMA
-- ======================================================
-- This file contains all DDL statements including Tables, 
-- Constraints, Views, Triggers, Sequences, and Procedures.
-- Database: Oracle
-- ======================================================

-- 1. CLEANUP (Drop existing objects)
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE PLACEMENT CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE APPLICATION CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE JOB CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE COMPANY CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE STUDENT CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE TPO CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP TABLE AUDIT_LOG CASCADE CONSTRAINTS';
   EXECUTE IMMEDIATE 'DROP SEQUENCE log_seq';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- 2. TABLE CREATION (DDL)

-- Student Table
CREATE TABLE STUDENT (
    student_id VARCHAR2(20) PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL,
    phone VARCHAR2(15) NOT NULL,
    department VARCHAR2(50) NOT NULL,
    cgpa NUMBER(3,2) CHECK (cgpa >= 0 AND cgpa <= 4),
    graduation_year NUMBER(4) CHECK (graduation_year >= 2024),
    skills VARCHAR2(200),
    CONSTRAINT valid_email CHECK (email LIKE '%@%.%')
);

-- Company Table
CREATE TABLE COMPANY (
    company_id VARCHAR2(20) PRIMARY KEY,
    company_name VARCHAR2(100) NOT NULL,
    industry VARCHAR2(50),
    email VARCHAR2(100) NOT NULL,
    phone VARCHAR2(15),
    address VARCHAR2(200),
    tpo_verified CHAR(1) DEFAULT 'N' CHECK (tpo_verified IN ('Y', 'N'))
);

-- Job Table
CREATE TABLE JOB (
    job_id VARCHAR2(20) PRIMARY KEY,
    company_id VARCHAR2(20) NOT NULL,
    job_title VARCHAR2(100) NOT NULL,
    description VARCHAR2(500),
    required_cgpa NUMBER(3,2) CHECK (required_cgpa >= 0 AND required_cgpa <= 4),
    location VARCHAR2(50),
    deadline_date DATE,
    is_active CHAR(1) DEFAULT 'Y' CHECK (is_active IN ('Y', 'N')),
    FOREIGN KEY (company_id) REFERENCES COMPANY(company_id) ON DELETE CASCADE
);

-- Application Table
CREATE TABLE APPLICATION (
    application_id VARCHAR2(20) PRIMARY KEY,
    student_id VARCHAR2(20) NOT NULL,
    job_id VARCHAR2(20) NOT NULL,
    application_date DATE DEFAULT SYSDATE,
    status VARCHAR2(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Shortlisted', 'Rejected', 'Selected')),
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES JOB(job_id) ON DELETE CASCADE,
    CONSTRAINT unique_application UNIQUE (student_id, job_id)
);

-- Placement Table
CREATE TABLE PLACEMENT (
    placement_id VARCHAR2(20) PRIMARY KEY,
    student_id VARCHAR2(20) NOT NULL,
    job_id VARCHAR2(20) NOT NULL,
    offer_date DATE DEFAULT SYSDATE,
    package_lpa NUMBER(5,2),
    joining_date DATE,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
    FOREIGN KEY (job_id) REFERENCES JOB(job_id)
);

-- TPO Table
CREATE TABLE TPO (
    tpo_id VARCHAR2(20) PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL,
    phone VARCHAR2(15),
    password VARCHAR2(50) NOT NULL
);

-- Audit Log Table
CREATE TABLE AUDIT_LOG (
    log_id NUMBER PRIMARY KEY,
    table_name VARCHAR2(30),
    action VARCHAR2(10),
    record_id VARCHAR2(20),
    changed_by VARCHAR2(20),
    change_date DATE
);

-- 3. SEQUENCES
CREATE SEQUENCE log_seq START WITH 1;

-- 4. VIEWS

-- Job application summary with company details
CREATE OR REPLACE VIEW vw_job_applications AS
SELECT j.job_id, j.job_title, c.company_name, COUNT(a.application_id) AS total_apps,
       AVG(s.cgpa) AS avg_cgpa
FROM JOB j
JOIN COMPANY c ON j.company_id = c.company_id
LEFT JOIN APPLICATION a ON j.job_id = a.job_id
LEFT JOIN STUDENT s ON a.student_id = s.student_id
GROUP BY j.job_id, j.job_title, c.company_name;

-- Student placement statistics by department
CREATE OR REPLACE VIEW vw_dept_placement_stats AS
SELECT department, COUNT(student_id) AS total_students,
       SUM(CASE WHEN student_id IN (SELECT student_id FROM PLACEMENT) THEN 1 ELSE 0 END) AS placed,
       ROUND(AVG(CASE WHEN student_id IN (SELECT student_id FROM PLACEMENT) THEN cgpa END), 2) AS avg_placed_cgpa
FROM STUDENT
GROUP BY department;

-- 5. TRIGGERS

-- Log job applications to AUDIT_LOG table
CREATE OR REPLACE TRIGGER trg_application_audit
AFTER INSERT ON APPLICATION
FOR EACH ROW
BEGIN
    INSERT INTO AUDIT_LOG (log_id, table_name, action, record_id, changed_by, change_date)
    VALUES (log_seq.NEXTVAL, 'APPLICATION', 'INSERT', :NEW.application_id, USER, SYSDATE);
END;
/

-- 6. STORED PROCEDURES

-- Apply for job with validation
CREATE OR REPLACE PROCEDURE sp_apply_job(
    p_student_id VARCHAR2,
    p_job_id VARCHAR2,
    p_status OUT VARCHAR2
) AS
    v_cgpa NUMBER;
    v_req_cgpa NUMBER;
    v_deadline DATE;
    v_exists NUMBER;
BEGIN
    -- Check if already applied
    SELECT COUNT(*) INTO v_exists FROM APPLICATION WHERE student_id = p_student_id AND job_id = p_job_id;
    IF v_exists > 0 THEN
        p_status := 'ALREADY_APPLIED';
        RETURN;
    END IF;
    
    -- Get student CGPA and job requirements
    SELECT cgpa INTO v_cgpa FROM STUDENT WHERE student_id = p_student_id;
    SELECT required_cgpa, deadline_date INTO v_req_cgpa, v_deadline FROM JOB WHERE job_id = p_job_id;
    
    IF v_cgpa < v_req_cgpa THEN
        p_status := 'CGPA_TOO_LOW';
        RETURN;
    END IF;
    
    IF v_deadline < SYSDATE THEN
        p_status := 'DEADLINE_PASSED';
        RETURN;
    END IF;
    
    -- Insert application
    INSERT INTO APPLICATION (application_id, student_id, job_id, status)
    VALUES ('A'||p_student_id||p_job_id, p_student_id, p_job_id, 'Pending');
    COMMIT;
    p_status := 'SUCCESS';
EXCEPTION
    WHEN OTHERS THEN
        p_status := 'ERROR';
END;
/

-- Final Commit
COMMIT;
