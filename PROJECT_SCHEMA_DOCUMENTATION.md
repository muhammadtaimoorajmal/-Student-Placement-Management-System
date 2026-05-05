# Student Placement Management System - Database Schema Documentation

This document provides a comprehensive overview of the database schema designed for the Student Placement Management System.

## 1. Entity-Relationship (ER) Diagram

The following diagram illustrates the tables and their relationships within the system.

```mermaid
erDiagram
    STUDENT ||--o{ APPLICATION : "submits"
    JOB ||--o{ APPLICATION : "receives"
    COMPANY ||--o{ JOB : "posts"
    STUDENT ||--o{ PLACEMENT : "is placed in"
    JOB ||--o{ PLACEMENT : "results in"
    TPO ||--o{ COMPANY : "verifies"
    
    STUDENT {
        varchar2 student_id PK
        varchar2 name
        varchar2 email UK
        varchar2 phone
        varchar2 department
        number cgpa
        number graduation_year
        varchar2 skills
    }
    
    COMPANY {
        varchar2 company_id PK
        varchar2 company_name
        varchar2 industry
        varchar2 email
        varchar2 phone
        varchar2 address
        char tpo_verified
    }
    
    JOB {
        varchar2 job_id PK
        varchar2 company_id FK
        varchar2 job_title
        varchar2 description
        number required_cgpa
        varchar2 location
        date deadline_date
        char is_active
    }
    
    APPLICATION {
        varchar2 application_id PK
        varchar2 student_id FK
        varchar2 job_id FK
        date application_date
        varchar2 status
    }
    
    PLACEMENT {
        varchar2 placement_id PK
        varchar2 student_id FK
        varchar2 job_id FK
        date offer_date
        number package_lpa
        date joining_date
    }
    
    TPO {
        varchar2 tpo_id PK
        varchar2 name
        varchar2 email UK
        varchar2 phone
        varchar2 password
    }
    
    AUDIT_LOG {
        number log_id PK
        varchar2 table_name
        varchar2 action
        varchar2 record_id
        varchar2 changed_by
        date change_date
    }
```

---

## 2. Data Dictionary

### Table: `STUDENT`
Stores personal and academic details of students.
- `student_id`: Unique identifier for each student (Primary Key).
- `name`: Full name of the student.
- `email`: University email address (Unique).
- `cgpa`: Cumulative Grade Point Average (0.0 to 4.0).
- `skills`: Comma-separated list of technical skills.

### Table: `COMPANY`
Stores information about recruiting companies.
- `company_id`: Unique identifier for the company (Primary Key).
- `tpo_verified`: Boolean flag ('Y'/'N') indicating if the company is verified by the TPO.

### Table: `JOB`
Stores details of job openings posted by companies.
- `job_id`: Unique identifier for the job (Primary Key).
- `required_cgpa`: Minimum CGPA required to apply for the job.
- `is_active`: Status of the job posting ('Y' for active, 'N' for closed).

### Table: `APPLICATION`
Tracks applications submitted by students for specific jobs.
- `status`: Current stage of the application (Pending, Shortlisted, Selected, Rejected).

### Table: `PLACEMENT`
Stores final placement/offer details for successful candidates.
- `package_lpa`: Salary package offered in Lakhs Per Annum.

---

## 3. Advanced SQL Features

### Views
1. **`vw_job_applications`**: Summarizes the total number of applications and the average applicant CGPA for each job.
2. **`vw_dept_placement_stats`**: Provides placement percentages and average CGPA of placed students per department.

### Triggers
- **`trg_application_audit`**: Automatically logs every new application into the `AUDIT_LOG` table for tracking and security purposes.

### Stored Procedures
- **`sp_apply_job`**: A robust procedure that validates a student's eligibility (CGPA check, deadline check) before allowing them to apply for a job.
