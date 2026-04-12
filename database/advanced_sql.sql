-- =============================================
-- 1. VIEW: Job application summary with company details
-- =============================================
CREATE OR REPLACE VIEW vw_job_applications AS
SELECT j.job_id, j.job_title, c.company_name, COUNT(a.application_id) AS total_apps,
       AVG(s.cgpa) AS avg_cgpa
FROM JOB j
JOIN COMPANY c ON j.company_id = c.company_id
LEFT JOIN APPLICATION a ON j.job_id = a.job_id
LEFT JOIN STUDENT s ON a.student_id = s.student_id
GROUP BY j.job_id, j.job_title, c.company_name;

-- =============================================
-- 2. VIEW: Student placement statistics by department
-- =============================================
CREATE OR REPLACE VIEW vw_dept_placement_stats AS
SELECT department, COUNT(student_id) AS total_students,
       SUM(CASE WHEN student_id IN (SELECT student_id FROM PLACEMENT) THEN 1 ELSE 0 END) AS placed,
       ROUND(AVG(CASE WHEN student_id IN (SELECT student_id FROM PLACEMENT) THEN cgpa END), 2) AS avg_placed_cgpa
FROM STUDENT
GROUP BY department;

-- =============================================
-- 3. TRIGGER: Log job applications to AUDIT_LOG table
-- =============================================
CREATE TABLE AUDIT_LOG (
    log_id NUMBER PRIMARY KEY,
    table_name VARCHAR2(30),
    action VARCHAR2(10),
    record_id VARCHAR2(20),
    changed_by VARCHAR2(20),
    change_date DATE
);

CREATE SEQUENCE log_seq START WITH 1;

CREATE OR REPLACE TRIGGER trg_application_audit
AFTER INSERT ON APPLICATION
FOR EACH ROW
BEGIN
    INSERT INTO AUDIT_LOG (log_id, table_name, action, record_id, changed_by, change_date)
    VALUES (log_seq.NEXTVAL, 'APPLICATION', 'INSERT', :NEW.application_id, USER, SYSDATE);
END;
/

-- =============================================
-- 4. PROCEDURE: Apply for job with validation
-- =============================================
CREATE OR REPLACE PROCEDURE sp_apply_job(
    p_student_id VARCHAR2,
    p_job_id VARCHAR2,
    p_status OUT VARCHAR2
) AS
    v_cgpa NUMBER;
    v_req_cgpa NUMBER;
    v_deadline DATE;
    v_exists NUMBER;
BEGIN
    -- Check if already applied
    SELECT COUNT(*) INTO v_exists FROM APPLICATION WHERE student_id = p_student_id AND job_id = p_job_id;
    IF v_exists > 0 THEN
        p_status := 'ALREADY_APPLIED';
        RETURN;
    END IF;
    
    -- Get student CGPA and job requirements
    SELECT cgpa INTO v_cgpa FROM STUDENT WHERE student_id = p_student_id;
    SELECT required_cgpa, deadline_date INTO v_req_cgpa, v_deadline FROM JOB WHERE job_id = p_job_id;
    
    IF v_cgpa < v_req_cgpa THEN
        p_status := 'CGPA_TOO_LOW';
        RETURN;
    END IF;
    
    IF v_deadline < SYSDATE THEN
        p_status := 'DEADLINE_PASSED';
        RETURN;
    END IF;
    
    -- Insert application
    INSERT INTO APPLICATION (application_id, student_id, job_id, status)
    VALUES ('A'||p_student_id||p_job_id, p_student_id, p_job_id, 'Pending');
    COMMIT;
    p_status := 'SUCCESS';
EXCEPTION
    WHEN OTHERS THEN
        p_status := 'ERROR';
END;
/