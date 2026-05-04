import random
import datetime

# Setup random seed for consistency
random.seed(42)

def generate_sql():
    sql = """-- Connect as placement_admin user in SQL Developer

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
"""

    companies = [
        ('C001', 'Systems Limited', 'IT Services', 'hr@systemsltd.com', '042-35712345', 'Lahore', 'Y'),
        ('C002', 'Nayatel', 'Telecommunications', 'careers@nayatel.com', '051-111123456', 'Islamabad', 'Y'),
        ('C003', 'Afiniti', 'AI/Software', 'jobs@afiniti.com', '021-35671234', 'Karachi', 'N'),
        ('C004', 'NetSol', 'IT Services', 'hr@netsol.com', '042-1234567', 'Lahore', 'Y'),
        ('C005', 'Devsinc', 'Software', 'careers@devsinc.com', '042-7654321', 'Lahore', 'Y'),
        ('C006', 'Arbisoft', 'IT Services', 'hiring@arbisoft.com', '042-99887766', 'Lahore', 'Y'),
        ('C007', 'Motive', 'AI/Software', 'hr@motive.com', '051-2233445', 'Islamabad', 'Y'),
        ('C008', 'Teradata', 'Data Analytics', 'jobs@teradata.com', '051-9988776', 'Islamabad', 'Y'),
        ('C009', 'Jazz', 'Telecommunications', 'hr@jazz.com.pk', '051-111300300', 'Islamabad', 'Y'),
        ('C010', 'Zameen', 'Real Estate Tech', 'careers@zameen.com', '042-111333444', 'Lahore', 'Y'),
        ('C011', 'Careem', 'Transport Tech', 'hr.pk@careem.com', '021-111222333', 'Karachi', 'Y'),
        ('C012', 'S&P Global', 'FinTech', 'jobs@spglobal.com', '051-4455667', 'Islamabad', 'Y'),
        ('C013', '10Pearls', 'Software', 'careers@10pearls.com', '021-9988776', 'Karachi', 'N'),
        ('C014', 'Ibex', 'BPO', 'hr@ibex.co', '042-111222444', 'Lahore', 'N'),
        ('C015', 'Ovex Technologies', 'IT Services', 'hr@ovextech.com', '051-111222555', 'Islamabad', 'Y'),
    ]

    for c in companies:
        sql += f"INSERT INTO COMPANY VALUES ('{c[0]}', '{c[1]}', '{c[2]}', '{c[3]}', '{c[4]}', '{c[5]}', '{c[6]}');\n"

    sql += "\n-- Insert Students\n"
    
    departments = ['CS', 'SE', 'AI', 'DS', 'IT']
    skills_pool = [
        'Python, SQL, Machine Learning',
        'Java, Spring Boot, Oracle',
        'C++, TensorFlow, Python',
        'Data Analysis, SQL, Power BI',
        'R, Python, Statistics',
        'React, Node.js, MongoDB',
        'Angular, Express, JavaScript',
        'C#, .NET, SQL Server',
        'Django, Python, PostgreSQL',
        'Flutter, Dart, Firebase',
        'AWS, Docker, Kubernetes',
        'HTML, CSS, JavaScript, Vue.js',
        'Cybersecurity, Ethical Hacking',
        'Cloud Computing, Azure',
        'Machine Learning, NLP, PyTorch'
    ]
    
    first_names = ['Muhammad', 'Ali', 'Sara', 'Fatima', 'Omar', 'Bilal', 'Hassan', 'Zainab', 'Ayesha', 'Usman', 'Hamza', 'Khadija', 'Maryam', 'Abdullah', 'Ahmad', 'Saad', 'Tariq', 'Nida', 'Sana', 'Hira']
    last_names = ['Khan', 'Ahmed', 'Ali', 'Zafar', 'Tariq', 'Hussain', 'Raza', 'Shah', 'Malik', 'Iqbal', 'Qureshi', 'Nawaz', 'Baig', 'Chaudhry', 'Sheikh']
    
    students = [
        ('S001', 'Muhammad Taimoor Ajmal', '63461@students.riphah.edu.pk', '03302612613', 'CS', 3.75, 2025, 'Python, SQL, Machine Learning'),
    ]
    
    for i in range(2, 41):
        s_id = f"S{i:03d}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{name.split()[0].lower()}.{name.split()[1].lower()}{i}@riphah.edu.pk"
        phone = f"03{random.randint(10, 49)}{random.randint(1000000, 9999999)}"
        dept = random.choice(departments)
        cgpa = round(random.uniform(2.5, 4.0), 2)
        grad_year = random.choice([2024, 2025])
        skills = random.choice(skills_pool)
        students.append((s_id, name, email, phone, dept, cgpa, grad_year, skills))
        
    for s in students:
        sql += f"INSERT INTO STUDENT VALUES ('{s[0]}', '{s[1]}', '{s[2]}', '{s[3]}', '{s[4]}', {s[5]}, {s[6]}, '{s[7]}');\n"

    sql += "\n-- Insert Jobs\n"
    jobs = []
    job_titles = ['Software Engineer', 'Data Analyst', 'AI Specialist', 'Network Engineer', 'Full Stack Developer', 'Frontend Developer', 'Backend Developer', 'DevOps Engineer', 'Quality Assurance', 'Cybersecurity Analyst', 'Product Manager', 'UX/UI Designer', 'Database Administrator', 'Cloud Architect']
    locations = ['Lahore', 'Islamabad', 'Karachi', 'Remote']
    
    for i in range(1, 31):
        j_id = f"J{i:03d}"
        c_id = f"C{random.randint(1, 15):03d}"
        title = random.choice(job_titles)
        desc = f"Looking for an experienced {title}."
        req_cgpa = round(random.uniform(2.5, 3.5), 2)
        loc = random.choice(locations)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        year = 2025
        deadline = f"{year}-{month:02d}-{day:02d}"
        is_active = random.choice(['Y', 'Y', 'Y', 'N'])
        jobs.append((j_id, c_id, title, desc, req_cgpa, loc, deadline, is_active))
        
    for j in jobs:
        sql += f"INSERT INTO JOB VALUES ('{j[0]}', '{j[1]}', '{j[2]}', '{j[3]}', {j[4]}, '{j[5]}', TO_DATE('{j[6]}', 'YYYY-MM-DD'), '{j[7]}');\n"

    sql += "\n-- Insert Applications\n"
    applications = []
    app_id_counter = 1
    
    for s in students:
        num_apps = random.randint(0, 4)
        applied_jobs = set()
        for _ in range(num_apps):
            job = random.choice(jobs)
            j_id = job[0]
            if j_id not in applied_jobs and s[5] >= job[4]: # Check CGPA requirement
                applied_jobs.add(j_id)
                status = random.choice(['Pending', 'Shortlisted', 'Rejected', 'Selected'])
                applications.append((f"A{app_id_counter:03d}", s[0], j_id, status))
                app_id_counter += 1
                
    for a in applications:
        sql += f"INSERT INTO APPLICATION VALUES ('{a[0]}', '{a[1]}', '{a[2]}', SYSDATE, '{a[3]}');\n"

    sql += "\n-- Insert Placements (for selected applications)\n"
    placements = []
    p_id_counter = 1
    for a in applications:
        if a[3] == 'Selected':
            package = round(random.uniform(4.0, 25.0), 2)
            joining_month = random.randint(6, 9)
            joining_date = f"2025-{joining_month:02d}-01"
            placements.append((f"P{p_id_counter:03d}", a[1], a[2], package, joining_date))
            p_id_counter += 1
            
    for p in placements:
        sql += f"INSERT INTO PLACEMENT VALUES ('{p[0]}', '{p[1]}', '{p[2]}', SYSDATE, {p[3]}, TO_DATE('{p[4]}', 'YYYY-MM-DD'));\n"

    sql += "\n-- Commit the transactions\nCOMMIT;\n"
    return sql

with open("d:\\BACHELORS-OF-COMPUTER-SCIENCE\\4th-Semester\\Subjects\\Database Systems\\DATA\\PROJECT\\Implementation\\placement_system\\database\\placement_setup.sql", "w") as f:
    f.write(generate_sql())

print("placement_setup.sql generated successfully!")
