import oracledb as cx_Oracle
from database.db_config import get_connection

def authenticate_student(student_id, password):
    # For demo, password is student_id. In real world, store hashed passwords.
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM STUDENT WHERE student_id = :id", {"id": student_id})
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        # For demo, password is student_id
        return result is not None and password == student_id
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return False

def get_student_details(student_id):
    conn = get_connection()
    if not conn: return {}
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM STUDENT WHERE student_id = :id", {"id": student_id})
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(zip(columns, data)) if data else {}
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return {}

def get_available_jobs():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT j.job_id, j.job_title, c.company_name, j.required_cgpa, j.location FROM JOB j JOIN COMPANY c ON j.company_id = c.company_id WHERE j.is_active = 'Y' AND j.deadline_date >= SYSDATE")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []

def apply_for_job(student_id, job_id):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        app_id = f"A{student_id}{job_id}"  # Simple ID generation
        cursor.execute("INSERT INTO APPLICATION (application_id, student_id, job_id, status) VALUES (:app_id, :sid, :jid, 'Pending')", {"app_id": app_id, "sid": student_id, "jid": job_id})
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return False

def get_my_applications(student_id):
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT a.application_id, j.job_title, c.company_name, a.status FROM APPLICATION a JOIN JOB j ON a.job_id = j.job_id JOIN COMPANY c ON j.company_id = c.company_id WHERE a.student_id = :sid ORDER BY a.application_date", {"sid": student_id})
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []