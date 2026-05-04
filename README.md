# Student Placement Management System

## 1. Introduction

The **Student Placement Management System** is a centralized platform designed to automate university placement processes. It allows students to apply for jobs, companies to manage recruitment, and Training & Placement Officers (TPOs) to oversee the entire ecosystem.

This project is built as a **Full-Stack Web Application**. It uses a modern web frontend (HTML/CSS/JS) and a robust Python backend (Flask) that interfaces with an **Oracle 11g XE Database**.

## 2. Technology Stack

| Layer | Technology | Description |
| --- | --- | --- |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) | Modern UI with Glassmorphism, Animations, and Responsive Dashboards. |
| **Backend** | Python 3 + Flask | RESTful API that handles business logic and database communication. |
| **Database** | Oracle 11g XE | Relational database storing all persistent records (Students, Jobs, Applications, etc.). |
| **Connectivity** | `oracledb` (Thick Mode) | Python driver used to connect the Flask backend to the Oracle Database. |

## 3. Database Implementation (SQL)

The core of this project is the **Oracle Database**. All data is stored in the Oracle 11g XE instance.

### 3.1 Where is the Data Stored?

All information is stored in relational tables within your **Oracle 11g Express Edition (XE)** installation on your local machine (localhost). When you perform actions in the web interface (like logging in or applying for a job), the Flask backend executes SQL queries to fetch or update records in these tables.

### 3.2 How to View Database Tables?

You can view the tables and data directly using Oracle tools:

1. **SQL*Plus**: Open your terminal and run `sqlplus your_username/your_password`.
2. **Oracle SQL Developer**: A graphical tool to browse tables, run queries, and see data.
3. **Table Names**: The main tables are `STUDENT`, `COMPANY`, `JOB`, `APPLICATION`, `PLACEMENT`, `TPO`, and `AUDIT_LOG`.

### 3.3 Database Features

- **Normalization**: The schema is designed in **3rd Normal Form (3NF)** to avoid redundancy.
- **Stored Procedures**: `sp_apply_job` handles application logic (checks CGPA and deadlines).
- **Triggers**: `trg_application_audit` automatically logs every new application into the `AUDIT_LOG` table.
- **Views**: `vw_job_applications` and `vw_dept_placement_stats` are used for generating reports.

## 4. System Setup & Running Instructions

### Step 1: Database Configuration

1. Ensure **Oracle 11g XE** is installed and running.
2. Open `database/db_config.py` and update the `DB_USER` and `DB_PASSWORD` with your actual Oracle credentials.
3. Ensure you have the **Oracle Instant Client** installed (required for `oracledb` thick mode).

### Step 2: Install Python Dependencies

Open your terminal in the project root directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

Start the Flask web server:

```bash
python main.py
```

### Step 4: Access the Portal

Open your browser and go to:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## 5. User Roles & Login

- **Student**: Login using `student_id` (e.g., S001) as both ID and Password.
- **Company**: Login using `company_id` (e.g., C001) as both ID and Password.
- **TPO**: Login using TPO credentials (e.g., TPO001 / tpo123).

---
**GitHub Link**: [https://github.com/muhammadtaimoorajmal/-Student-Placement-Management-System.git](https://github.com/muhammadtaimoorajmal/-Student-Placement-Management-System.git)
