import oracledb as cx_Oracle
from database.db_config import get_connection

def authenticate_company(company_id, password):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM COMPANY WHERE company_id = :id", {"id": company_id})
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        # For demo, password is company_id
        return result is not None and password == company_id
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return False

def get_company_details(company_id):
    conn = get_connection()
    if not conn: return {}
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM COMPANY WHERE company_id = :id", {"id": company_id})
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(zip(columns, data)) if data else {}
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return {}

def get_company_jobs(company_id):
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT job_id, job_title, required_cgpa, location, deadline_date, is_active FROM JOB WHERE company_id = :cid", {"cid": company_id})
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []

def post_new_job(company_id, title, description, req_cgpa, location, deadline):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        # Simple ID generation: J + timestamp
        job_id = f"J{company_id}{cursor.callfunc('sys_guid', str)}"[:20]
        cursor.execute("""
            INSERT INTO JOB (job_id, company_id, job_title, description, required_cgpa, location, deadline_date) 
            VALUES (:jid, :cid, :title, :job_desc, :cgpa, :loc, TO_DATE(:deadline, 'YYYY-MM-DD'))
        """, {"jid": job_id, "cid": company_id, "title": title, "job_desc": description, "cgpa": req_cgpa, "loc": location, "deadline": deadline})
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return False

def get_applicants_for_company(company_id):
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT a.application_id, s.name, s.email, s.cgpa, j.job_title, a.status FROM APPLICATION a JOIN STUDENT s ON a.student_id = s.student_id JOIN JOB j ON a.job_id = j.job_id WHERE j.company_id = :cid", {"cid": company_id})
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []

def update_application_status(application_id, new_status):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE APPLICATION SET status = :status WHERE application_id = :app_id", {"status": new_status, "app_id": application_id})
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return False