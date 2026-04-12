import oracledb as cx_Oracle
from database.db_config import get_connection

def apply_job_with_procedure(student_id, job_id):
    conn = get_connection()
    if not conn:
        return "CONNECTION_ERROR"
    try:
        cursor = conn.cursor()
        status_var = cursor.var(str)
        cursor.callproc("sp_apply_job", [student_id, job_id, status_var])
        conn.commit()
        result = status_var.getvalue()
        cursor.close()
        conn.close()
        return result
    except cx_Oracle.Error as e:
        print(f"Procedure error: {e}")
        return "ERROR"

def get_job_applications_view():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_job_applications")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(e)
        return []

def get_dept_placement_stats_view():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_dept_placement_stats")
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in data]
    except cx_Oracle.Error as e:
        print(e)
        return []