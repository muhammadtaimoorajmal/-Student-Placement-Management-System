import oracledb as cx_Oracle
from database.db_config import get_connection

def get_report_companies_with_jobs():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT c.company_name, COUNT(j.job_id) AS total_jobs FROM COMPANY c LEFT JOIN JOB j ON c.company_id = j.company_id GROUP BY c.company_name ORDER BY total_jobs DESC")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []

def get_report_applications_by_status():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) AS count FROM APPLICATION GROUP BY status")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []

def get_report_department_placement_stats():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT s.department, COUNT(p.placement_id) AS total_placed, ROUND(AVG(p.package_lpa), 2) AS avg_package FROM STUDENT s LEFT JOIN PLACEMENT p ON s.student_id = p.student_id GROUP BY s.department ORDER BY total_placed DESC")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(f"DB Error: {e}")
        return []