import oracledb as cx_Oracle
from database.db_config import get_connection

def authenticate_tpo(tpo_id, password):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TPO WHERE tpo_id = :id AND password = :pwd", {"id": tpo_id, "pwd": password})
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return False

def get_all_students():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, name, email, department, cgpa FROM STUDENT ORDER BY student_id")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []

def get_all_companies():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT company_id, company_name, industry, email, tpo_verified FROM COMPANY ORDER BY company_name")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []

def get_all_jobs():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT j.job_id, j.job_title, c.company_name, j.location, j.is_active FROM JOB j JOIN COMPANY c ON j.company_id = c.company_id ORDER BY j.job_id")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []

def get_all_applications():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT a.application_id, s.name AS student_name, j.job_title, a.status FROM APPLICATION a JOIN STUDENT s ON a.student_id = s.student_id JOIN JOB j ON a.job_id = j.job_id ORDER BY a.application_id")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []

def verify_company(company_id):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE COMPANY SET tpo_verified = 'Y' WHERE company_id = :id", {"id": company_id})
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return False