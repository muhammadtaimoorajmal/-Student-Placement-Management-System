-- Connect as placement_admin user in SQL Developer

-- ======================================================
-- 1. CREATE TABLES (DDL)
-- ======================================================
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE PLACEMENT CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE APPLICATION CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE JOB CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE COMPANY CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE STUDENT CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE TPO CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

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
INSERT INTO COMPANY VALUES ('C004', 'NetSol', 'IT Services', 'hr@netsol.com', '042-1234567', 'Lahore', 'Y');
INSERT INTO COMPANY VALUES ('C005', 'Devsinc', 'Software', 'careers@devsinc.com', '042-7654321', 'Lahore', 'Y');
INSERT INTO COMPANY VALUES ('C006', 'Arbisoft', 'IT Services', 'hiring@arbisoft.com', '042-99887766', 'Lahore', 'Y');
INSERT INTO COMPANY VALUES ('C007', 'Motive', 'AI/Software', 'hr@motive.com', '051-2233445', 'Islamabad', 'Y');
INSERT INTO COMPANY VALUES ('C008', 'Teradata', 'Data Analytics', 'jobs@teradata.com', '051-9988776', 'Islamabad', 'Y');
INSERT INTO COMPANY VALUES ('C009', 'Jazz', 'Telecommunications', 'hr@jazz.com.pk', '051-111300300', 'Islamabad', 'Y');
INSERT INTO COMPANY VALUES ('C010', 'Zameen', 'Real Estate Tech', 'careers@zameen.com', '042-111333444', 'Lahore', 'Y');
INSERT INTO COMPANY VALUES ('C011', 'Careem', 'Transport Tech', 'hr.pk@careem.com', '021-111222333', 'Karachi', 'Y');
INSERT INTO COMPANY VALUES ('C012', 'S&P Global', 'FinTech', 'jobs@spglobal.com', '051-4455667', 'Islamabad', 'Y');
INSERT INTO COMPANY VALUES ('C013', '10Pearls', 'Software', 'careers@10pearls.com', '021-9988776', 'Karachi', 'N');
INSERT INTO COMPANY VALUES ('C014', 'Ibex', 'BPO', 'hr@ibex.co', '042-111222444', 'Lahore', 'N');
INSERT INTO COMPANY VALUES ('C015', 'Ovex Technologies', 'IT Services', 'hr@ovextech.com', '051-111222555', 'Islamabad', 'Y');

-- Insert Students
INSERT INTO STUDENT VALUES ('S001', 'Muhammad Taimoor Ajmal', '63461@students.riphah.edu.pk', '03302612613', 'CS', 3.75, 2025, 'Python, SQL, Machine Learning');
INSERT INTO STUDENT VALUES ('S002', 'Fatima Khan', 'fatima.khan2@riphah.edu.pk', '03275108603', 'SE', 2.71, 2024, 'AWS, Docker, Kubernetes');
INSERT INTO STUDENT VALUES ('S003', 'Nida Ahmed', 'nida.ahmed3@riphah.edu.pk', '03478078673', 'CS', 2.54, 2024, 'Data Analysis, SQL, Power BI');
INSERT INTO STUDENT VALUES ('S004', 'Tariq Iqbal', 'tariq.iqbal4@riphah.edu.pk', '03114335942', 'IT', 3.13, 2025, 'Flutter, Dart, Firebase');
INSERT INTO STUDENT VALUES ('S005', 'Ayesha Baig', 'ayesha.baig5@riphah.edu.pk', '03103678638', 'DS', 3.01, 2024, 'Data Analysis, SQL, Power BI');
INSERT INTO STUDENT VALUES ('S006', 'Hamza Ahmed', 'hamza.ahmed6@riphah.edu.pk', '03157374122', 'CS', 3.04, 2025, 'Flutter, Dart, Firebase');
INSERT INTO STUDENT VALUES ('S007', 'Ayesha Baig', 'ayesha.baig7@riphah.edu.pk', '03128707870', 'IT', 2.69, 2025, 'Java, Spring Boot, Oracle');
INSERT INTO STUDENT VALUES ('S008', 'Nida Tariq', 'nida.tariq8@riphah.edu.pk', '03497067228', 'IT', 2.79, 2024, 'Python, SQL, Machine Learning');
INSERT INTO STUDENT VALUES ('S009', 'Zainab Baig', 'zainab.baig9@riphah.edu.pk', '03282338687', 'SE', 3.8, 2025, 'R, Python, Statistics');
INSERT INTO STUDENT VALUES ('S010', 'Ahmad Qureshi', 'ahmad.qureshi10@riphah.edu.pk', '03333728882', 'AI', 3.03, 2025, 'HTML, CSS, JavaScript, Vue.js');
INSERT INTO STUDENT VALUES ('S011', 'Sara Iqbal', 'sara.iqbal11@riphah.edu.pk', '03209961380', 'SE', 2.75, 2025, 'R, Python, Statistics');
INSERT INTO STUDENT VALUES ('S012', 'Nida Zafar', 'nida.zafar12@riphah.edu.pk', '03301938483', 'SE', 3.73, 2025, 'Angular, Express, JavaScript');
INSERT INTO STUDENT VALUES ('S013', 'Ayesha Ahmed', 'ayesha.ahmed13@riphah.edu.pk', '03236279418', 'SE', 3.48, 2025, 'Machine Learning, NLP, PyTorch');
INSERT INTO STUDENT VALUES ('S014', 'Ahmad Ali', 'ahmad.ali14@riphah.edu.pk', '03263342608', 'SE', 3.62, 2025, 'HTML, CSS, JavaScript, Vue.js');
INSERT INTO STUDENT VALUES ('S015', 'Sana Raza', 'sana.raza15@riphah.edu.pk', '03477700828', 'AI', 2.83, 2024, 'Django, Python, PostgreSQL');
INSERT INTO STUDENT VALUES ('S016', 'Saad Ahmed', 'saad.ahmed16@riphah.edu.pk', '03132839607', 'SE', 3.44, 2025, 'Flutter, Dart, Firebase');
INSERT INTO STUDENT VALUES ('S017', 'Sara Raza', 'sara.raza17@riphah.edu.pk', '03348852574', 'IT', 2.88, 2024, 'AWS, Docker, Kubernetes');
INSERT INTO STUDENT VALUES ('S018', 'Fatima Qureshi', 'fatima.qureshi18@riphah.edu.pk', '03445476583', 'AI', 2.67, 2025, 'C++, TensorFlow, Python');
INSERT INTO STUDENT VALUES ('S019', 'Ahmad Khan', 'ahmad.khan19@riphah.edu.pk', '03269398441', 'SE', 3.26, 2024, 'Cloud Computing, Azure');
INSERT INTO STUDENT VALUES ('S020', 'Usman Chaudhry', 'usman.chaudhry20@riphah.edu.pk', '03424337174', 'SE', 3.06, 2024, 'Django, Python, PostgreSQL');
INSERT INTO STUDENT VALUES ('S021', 'Tariq Sheikh', 'tariq.sheikh21@riphah.edu.pk', '03106438436', 'DS', 2.53, 2025, 'Machine Learning, NLP, PyTorch');
INSERT INTO STUDENT VALUES ('S022', 'Usman Zafar', 'usman.zafar22@riphah.edu.pk', '03135041154', 'IT', 3.92, 2024, 'HTML, CSS, JavaScript, Vue.js');
INSERT INTO STUDENT VALUES ('S023', 'Saad Chaudhry', 'saad.chaudhry23@riphah.edu.pk', '03149937326', 'SE', 2.69, 2025, 'Django, Python, PostgreSQL');
INSERT INTO STUDENT VALUES ('S024', 'Bilal Tariq', 'bilal.tariq24@riphah.edu.pk', '03438099076', 'SE', 3.89, 2024, 'HTML, CSS, JavaScript, Vue.js');
INSERT INTO STUDENT VALUES ('S025', 'Usman Raza', 'usman.raza25@riphah.edu.pk', '03338350099', 'IT', 3.18, 2024, 'Data Analysis, SQL, Power BI');
INSERT INTO STUDENT VALUES ('S026', 'Sara Hussain', 'sara.hussain26@riphah.edu.pk', '03114860684', 'IT', 2.83, 2024, 'HTML, CSS, JavaScript, Vue.js');
INSERT INTO STUDENT VALUES ('S027', 'Ali Zafar', 'ali.zafar27@riphah.edu.pk', '03141527021', 'AI', 2.61, 2024, 'R, Python, Statistics');
INSERT INTO STUDENT VALUES ('S028', 'Saad Zafar', 'saad.zafar28@riphah.edu.pk', '03443219824', 'IT', 3.36, 2024, 'Cybersecurity, Ethical Hacking');
INSERT INTO STUDENT VALUES ('S029', 'Saad Baig', 'saad.baig29@riphah.edu.pk', '03364194548', 'CS', 2.65, 2025, 'React, Node.js, MongoDB');
INSERT INTO STUDENT VALUES ('S030', 'Abdullah Raza', 'abdullah.raza30@riphah.edu.pk', '03391908841', 'CS', 2.59, 2025, 'Cybersecurity, Ethical Hacking');
INSERT INTO STUDENT VALUES ('S031', 'Fatima Zafar', 'fatima.zafar31@riphah.edu.pk', '03224191175', 'IT', 3.17, 2025, 'C++, TensorFlow, Python');
INSERT INTO STUDENT VALUES ('S032', 'Ayesha Shah', 'ayesha.shah32@riphah.edu.pk', '03252264748', 'DS', 3.71, 2024, 'Python, SQL, Machine Learning');
INSERT INTO STUDENT VALUES ('S033', 'Nida Chaudhry', 'nida.chaudhry33@riphah.edu.pk', '03102564689', 'SE', 2.75, 2025, 'C#, .NET, SQL Server');
INSERT INTO STUDENT VALUES ('S034', 'Hassan Chaudhry', 'hassan.chaudhry34@riphah.edu.pk', '03351983738', 'SE', 3.07, 2025, 'R, Python, Statistics');
INSERT INTO STUDENT VALUES ('S035', 'Ahmad Tariq', 'ahmad.tariq35@riphah.edu.pk', '03379164991', 'SE', 2.78, 2024, 'Python, SQL, Machine Learning');
INSERT INTO STUDENT VALUES ('S036', 'Sana Nawaz', 'sana.nawaz36@riphah.edu.pk', '03442022698', 'AI', 2.59, 2025, 'Django, Python, PostgreSQL');
INSERT INTO STUDENT VALUES ('S037', 'Tariq Ali', 'tariq.ali37@riphah.edu.pk', '03139519948', 'CS', 3.78, 2024, 'Flutter, Dart, Firebase');
INSERT INTO STUDENT VALUES ('S038', 'Sara Qureshi', 'sara.qureshi38@riphah.edu.pk', '03257774229', 'CS', 3.91, 2024, 'Flutter, Dart, Firebase');
INSERT INTO STUDENT VALUES ('S039', 'Hira Khan', 'hira.khan39@riphah.edu.pk', '03492375453', 'DS', 3.49, 2025, 'Machine Learning, NLP, PyTorch');
INSERT INTO STUDENT VALUES ('S040', 'Ayesha Zafar', 'ayesha.zafar40@riphah.edu.pk', '03305004485', 'AI', 3.09, 2025, 'C#, .NET, SQL Server');

-- Insert Jobs
INSERT INTO JOB VALUES ('J001', 'C006', 'Database Administrator', 'Looking for an experienced Database Administrator.', 3.44, 'Lahore', TO_DATE('2025-08-20', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J002', 'C002', 'Quality Assurance', 'Looking for an experienced Quality Assurance.', 2.71, 'Karachi', TO_DATE('2025-03-12', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J003', 'C015', 'Network Engineer', 'Looking for an experienced Network Engineer.', 2.87, 'Islamabad', TO_DATE('2025-08-27', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J004', 'C010', 'Database Administrator', 'Looking for an experienced Database Administrator.', 3.15, 'Lahore', TO_DATE('2025-11-27', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J005', 'C015', 'Product Manager', 'Looking for an experienced Product Manager.', 2.6, 'Islamabad', TO_DATE('2025-05-04', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J006', 'C012', 'Quality Assurance', 'Looking for an experienced Quality Assurance.', 2.66, 'Karachi', TO_DATE('2025-10-07', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J007', 'C004', 'Product Manager', 'Looking for an experienced Product Manager.', 3.13, 'Karachi', TO_DATE('2025-09-16', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J008', 'C015', 'Cloud Architect', 'Looking for an experienced Cloud Architect.', 2.55, 'Remote', TO_DATE('2025-05-02', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J009', 'C006', 'Database Administrator', 'Looking for an experienced Database Administrator.', 2.63, 'Karachi', TO_DATE('2025-03-24', 'YYYY-MM-DD'), 'N');
INSERT INTO JOB VALUES ('J010', 'C009', 'UX/UI Designer', 'Looking for an experienced UX/UI Designer.', 2.93, 'Lahore', TO_DATE('2025-02-03', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J011', 'C009', 'Software Engineer', 'Looking for an experienced Software Engineer.', 3.33, 'Islamabad', TO_DATE('2025-07-05', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J012', 'C005', 'Frontend Developer', 'Looking for an experienced Frontend Developer.', 3.4, 'Lahore', TO_DATE('2025-06-07', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J013', 'C011', 'Data Analyst', 'Looking for an experienced Data Analyst.', 2.85, 'Remote', TO_DATE('2025-10-24', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J014', 'C015', 'Network Engineer', 'Looking for an experienced Network Engineer.', 3.36, 'Islamabad', TO_DATE('2025-07-01', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J015', 'C012', 'Frontend Developer', 'Looking for an experienced Frontend Developer.', 3.28, 'Remote', TO_DATE('2025-11-28', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J016', 'C005', 'AI Specialist', 'Looking for an experienced AI Specialist.', 3.29, 'Lahore', TO_DATE('2025-07-28', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J017', 'C014', 'DevOps Engineer', 'Looking for an experienced DevOps Engineer.', 2.72, 'Remote', TO_DATE('2025-06-10', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J018', 'C004', 'Software Engineer', 'Looking for an experienced Software Engineer.', 3.16, 'Remote', TO_DATE('2025-06-09', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J019', 'C013', 'Full Stack Developer', 'Looking for an experienced Full Stack Developer.', 2.85, 'Remote', TO_DATE('2025-11-27', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J020', 'C001', 'Data Analyst', 'Looking for an experienced Data Analyst.', 3.38, 'Karachi', TO_DATE('2025-03-19', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J021', 'C001', 'Data Analyst', 'Looking for an experienced Data Analyst.', 3.1, 'Karachi', TO_DATE('2025-12-26', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J022', 'C007', 'Cybersecurity Analyst', 'Looking for an experienced Cybersecurity Analyst.', 3.48, 'Lahore', TO_DATE('2025-07-19', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J023', 'C005', 'Software Engineer', 'Looking for an experienced Software Engineer.', 3.21, 'Lahore', TO_DATE('2025-09-26', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J024', 'C006', 'Backend Developer', 'Looking for an experienced Backend Developer.', 2.57, 'Karachi', TO_DATE('2025-10-11', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J025', 'C012', 'Full Stack Developer', 'Looking for an experienced Full Stack Developer.', 3.01, 'Remote', TO_DATE('2025-06-13', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J026', 'C009', 'AI Specialist', 'Looking for an experienced AI Specialist.', 2.69, 'Remote', TO_DATE('2025-11-24', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J027', 'C010', 'Cybersecurity Analyst', 'Looking for an experienced Cybersecurity Analyst.', 2.8, 'Lahore', TO_DATE('2025-05-10', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J028', 'C007', 'Database Administrator', 'Looking for an experienced Database Administrator.', 3.08, 'Karachi', TO_DATE('2025-08-15', 'YYYY-MM-DD'), 'N');
INSERT INTO JOB VALUES ('J029', 'C011', 'Network Engineer', 'Looking for an experienced Network Engineer.', 3.01, 'Islamabad', TO_DATE('2025-11-03', 'YYYY-MM-DD'), 'Y');
INSERT INTO JOB VALUES ('J030', 'C009', 'Product Manager', 'Looking for an experienced Product Manager.', 3.13, 'Karachi', TO_DATE('2025-02-27', 'YYYY-MM-DD'), 'Y');

-- Insert Applications
INSERT INTO APPLICATION VALUES ('A001', 'S001', 'J008', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A002', 'S001', 'J005', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A003', 'S004', 'J028', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A004', 'S004', 'J029', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A005', 'S005', 'J013', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A006', 'S005', 'J005', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A007', 'S007', 'J008', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A008', 'S007', 'J026', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A009', 'S008', 'J008', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A010', 'S008', 'J005', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A011', 'S009', 'J018', SYSDATE, 'Rejected');
INSERT INTO APPLICATION VALUES ('A012', 'S009', 'J025', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A013', 'S009', 'J020', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A014', 'S009', 'J027', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A015', 'S010', 'J024', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A016', 'S011', 'J009', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A017', 'S012', 'J025', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A018', 'S012', 'J021', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A019', 'S013', 'J015', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A020', 'S013', 'J023', SYSDATE, 'Rejected');
INSERT INTO APPLICATION VALUES ('A021', 'S014', 'J009', SYSDATE, 'Rejected');
INSERT INTO APPLICATION VALUES ('A022', 'S017', 'J005', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A023', 'S018', 'J005', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A024', 'S019', 'J018', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A025', 'S020', 'J002', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A026', 'S020', 'J027', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A027', 'S020', 'J013', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A028', 'S022', 'J025', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A029', 'S022', 'J028', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A030', 'S023', 'J024', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A031', 'S023', 'J008', SYSDATE, 'Rejected');
INSERT INTO APPLICATION VALUES ('A032', 'S024', 'J001', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A033', 'S024', 'J011', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A034', 'S024', 'J024', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A035', 'S025', 'J030', SYSDATE, 'Shortlisted');
INSERT INTO APPLICATION VALUES ('A036', 'S025', 'J018', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A037', 'S029', 'J005', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A038', 'S032', 'J011', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A039', 'S032', 'J009', SYSDATE, 'Selected');
INSERT INTO APPLICATION VALUES ('A040', 'S034', 'J024', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A041', 'S039', 'J007', SYSDATE, 'Pending');
INSERT INTO APPLICATION VALUES ('A042', 'S040', 'J005', SYSDATE, 'Shortlisted');

-- Insert Placements (for selected applications)
INSERT INTO PLACEMENT VALUES ('P001', 'S007', 'J026', SYSDATE, 6.4, TO_DATE('2025-07-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P002', 'S008', 'J005', SYSDATE, 13.77, TO_DATE('2025-08-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P003', 'S009', 'J025', SYSDATE, 20.1, TO_DATE('2025-07-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P004', 'S009', 'J020', SYSDATE, 16.72, TO_DATE('2025-06-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P005', 'S009', 'J027', SYSDATE, 20.33, TO_DATE('2025-07-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P006', 'S010', 'J024', SYSDATE, 24.26, TO_DATE('2025-06-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P007', 'S012', 'J025', SYSDATE, 16.15, TO_DATE('2025-08-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P008', 'S019', 'J018', SYSDATE, 16.09, TO_DATE('2025-09-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P009', 'S020', 'J027', SYSDATE, 12.33, TO_DATE('2025-07-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P010', 'S022', 'J025', SYSDATE, 5.6, TO_DATE('2025-07-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P011', 'S022', 'J028', SYSDATE, 6.14, TO_DATE('2025-08-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P012', 'S024', 'J001', SYSDATE, 21.86, TO_DATE('2025-06-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P013', 'S024', 'J011', SYSDATE, 20.72, TO_DATE('2025-06-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P014', 'S029', 'J005', SYSDATE, 11.29, TO_DATE('2025-09-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P015', 'S032', 'J011', SYSDATE, 17.89, TO_DATE('2025-06-01', 'YYYY-MM-DD'));
INSERT INTO PLACEMENT VALUES ('P016', 'S032', 'J009', SYSDATE, 14.63, TO_DATE('2025-08-01', 'YYYY-MM-DD'));

-- Commit the transactions
COMMIT;
