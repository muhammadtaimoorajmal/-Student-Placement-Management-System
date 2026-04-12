-- Connect as placement_admin user in SQL Developer

-- ======================================================
-- 1. CREATE TABLES (DDL)
-- ======================================================

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

CREATE TABLE COMPANY (
    company_id VARCHAR2(20) PRIMARY KEY,
    company_name VARCHAR2(100) NOT NULL,
    industry VARCHAR2(50),
    email VARCHAR2(100) NOT NULL,
    phone VARCHAR2(15),
    address VARCHAR2(200),
    tpo_verified CHAR(1) DEFAULT 'N' CHECK (tpo_verified IN ('Y', 'N'))
);

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

CREATE TABLE TPO (
    tpo_id VARCHAR2(20) PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) UNIQUE NOT NULL,
    phone VARCHAR2(15),
    password VARCHAR2(50) NOT NULL
);

-- ======================================================
-- 2. INSERT SAMPLE DATA (DML)
-- ======================================================

-- Insert TPO
INSERT INTO TPO (tpo_id, name, email, phone, password) VALUES ('TPO001', 'Dr. Ahmed Raza', 'ahmed.raza@riphah.edu.pk', '03001234567', 'tpo123');

-- Insert Companies
INSERT INTO COMPANY VALUES ('C001', 'Systems Limited', 'IT Services', 'hr@systemsltd.com', '042-35712345', 'Lahore', 'Y');
INSERT INTO COMPANY VALUES ('C002', 'Nayatel', 'Telecommunications', 'careers@nayatel.com', '051-111123456', 'Islamabad', 'Y');
INSERT INTO COMPANY VALUES ('C003', 'Afiniti', 'AI/Software', 'jobs@afiniti.com', '021-35671234', 'Karachi', 'N');

-- Insert Students
INSERT INTO STUDENT VALUES ('S001', 'Ali Khan', 'ali.khan@riphah.edu.pk', '03123456789', 'CS', 3.75, 2025, 'Python, SQL, Machine Learning');
INSERT INTO STUDENT VALUES ('S002', 'Sara Ahmed', 'sara.ahmed@riphah.edu.pk', '03128765432', 'CS', 3.90, 2025, 'Java, Spring Boot, Oracle');
INSERT INTO STUDENT VALUES ('S003', 'Bilal Hussain', 'bilal.h@riphah.edu.pk', '03224567890', 'AI', 3.60, 2025, 'C++, TensorFlow, Python');
INSERT INTO STUDENT VALUES ('S004', 'Fatima Zafar', 'fatima.z@riphah.edu.pk', '03337654321', 'CS', 3.85, 2024, 'Data Analysis, SQL, Power BI');
INSERT INTO STUDENT VALUES ('S005', 'Omar Tariq', 'omar.t@riphah.edu.pk', '03455678901', 'DS', 3.50, 2025, 'R, Python, Statistics');

-- Insert Jobs
INSERT INTO JOB VALUES ('J001', 'C001', 'Software Engineer', 'Develop web applications.', 3.20, 'Lahore', TO_DATE('2025-06-30', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J002', 'C002', 'Network Engineer', 'Manage network infrastructure.', 3.00, 'Islamabad', TO_DATE('2025-05-15', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J003', 'C001', 'Data Analyst', 'Analyze business data.', 3.50, 'Remote', TO_DATE('2025-07-10', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J004', 'C003', 'AI Specialist', 'Develop AI models.', 3.70, 'Karachi', TO_DATE('2025-04-20', 'YYYY-MM-DD'), 'N');

-- Insert Applications
INSERT INTO APPLICATION VALUES ('A001', 'S001', 'J001', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A002', 'S002', 'J001', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A003', 'S004', 'J002', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A004', 'S003', 'J004', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A005', 'S001', 'J003', SYSDATE, 'Shortlisted');

-- Insert Placements (for selected applications)
INSERT INTO PLACEMENT VALUES ('P001', 'S004', 'J002', SYSDATE, 12.50, TO_DATE('2025-08-15', 'YYYY-MM-DD'));
-- Commit the transactions
COMMIT;

-- ======================================================
-- 3. ADVANCED SQL QUERIES FOR REPORTS
-- ======================================================

-- Report 1: Companies and their active job postings (INNER JOIN)
SELECT c.company_name, j.job_title, j.location, j.deadline_date
FROM COMPANY c
INNER JOIN JOB j ON c.company_id = j.company_id
WHERE j.is_active = 'Y';

-- Report 2: Students who applied for a specific company's job (Nested Query)
SELECT s.name, s.email, s.cgpa
FROM STUDENT s
WHERE s.student_id IN (
    SELECT a.student_id
    FROM APPLICATION a
    JOIN JOB j ON a.job_id = j.job_id
    WHERE j.company_id = 'C001'
);

-- Report 3: Number of applications per job with average CGPA of applicants (Aggregation, GROUP BY)
SELECT j.job_title, COUNT(a.application_id) AS total_applications, AVG(s.cgpa) AS avg_applicant_cgpa
FROM JOB j
JOIN APPLICATION a ON j.job_id = a.job_id
JOIN STUDENT s ON a.student_id = s.student_id
WHERE j.is_active = 'Y'
GROUP BY j.job_title
ORDER BY total_applications DESC;

-- Report 4: Department-wise placement statistics (Aggregation, LEFT JOIN)
SELECT s.department, COUNT(p.placement_id) AS total_placed, ROUND(AVG(p.package_lpa), 2) AS avg_package
FROM STUDENT s
LEFT JOIN PLACEMENT p ON s.student_id = p.student_id
GROUP BY s.department
ORDER BY total_placed DESC;

-- Report 5: Students with no applications yet (NOT EXISTS / NOT IN)
SELECT name, email
FROM STUDENT s
WHERE NOT EXISTS (
    SELECT 1 FROM APPLICATION a WHERE a.student_id = s.student_id
);