import os
from flask import Flask, request, jsonify, send_from_directory

from backend.student_ops import authenticate_student, get_student_details, get_available_jobs, apply_for_job, get_my_applications
from backend.company_ops import authenticate_company, get_company_details, get_company_jobs, post_new_job, get_applicants_for_company, update_application_status
from backend.tpo_ops import authenticate_tpo, get_all_students, get_all_companies, get_all_jobs, get_all_applications, verify_company
# from backend.report_ops import ... (if needed)

app = Flask(__name__, static_folder='frontend', static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    role = data.get('role')
    user_id = data.get('userId')
    password = data.get('password')
    
    if role == 'student':
        success = authenticate_student(user_id, password)
    elif role == 'company':
        success = authenticate_company(user_id, password)
    elif role == 'tpo':
        success = authenticate_tpo(user_id, password)
    else:
        return jsonify({"success": False, "message": "Invalid role"})
        
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"})

# --- Student Endpoints ---
@app.route('/api/student/details', methods=['GET'])
def student_details():
    user_id = request.args.get('userId')
    return jsonify(get_student_details(user_id))

@app.route('/api/student/jobs', methods=['GET'])
def student_jobs():
    return jsonify(get_available_jobs())

@app.route('/api/student/applications', methods=['GET'])
def student_applications():
    user_id = request.args.get('userId')
    return jsonify(get_my_applications(user_id))

@app.route('/api/student/apply', methods=['POST'])
def student_apply():
    data = request.json
    success = apply_for_job(data.get('userId'), data.get('jobId'))
    return jsonify({"success": success})

# --- Company Endpoints ---
@app.route('/api/company/details', methods=['GET'])
def company_details():
    user_id = request.args.get('userId')
    return jsonify(get_company_details(user_id))

@app.route('/api/company/jobs', methods=['GET'])
def company_jobs():
    user_id = request.args.get('userId')
    return jsonify(get_company_jobs(user_id))

@app.route('/api/company/post_job', methods=['POST'])
def company_post_job():
    data = request.json
    success = post_new_job(
        data.get('companyId'),
        data.get('title'),
        data.get('description'),
        data.get('reqCgpa'),
        data.get('location'),
        data.get('deadline')
    )
    return jsonify({"success": success})

@app.route('/api/company/applicants', methods=['GET'])
def company_applicants():
    user_id = request.args.get('userId')
    return jsonify(get_applicants_for_company(user_id))

@app.route('/api/company/update_status', methods=['POST'])
def company_update_status():
    data = request.json
    success = update_application_status(data.get('applicationId'), data.get('status'))
    return jsonify({"success": success})

# --- TPO Endpoints ---
@app.route('/api/tpo/students', methods=['GET'])
def tpo_students():
    return jsonify(get_all_students())

@app.route('/api/tpo/companies', methods=['GET'])
def tpo_companies():
    return jsonify(get_all_companies())

@app.route('/api/tpo/jobs', methods=['GET'])
def tpo_jobs():
    return jsonify(get_all_jobs())

@app.route('/api/tpo/applications', methods=['GET'])
def tpo_applications():
    return jsonify(get_all_applications())

@app.route('/api/tpo/verify_company', methods=['POST'])
def tpo_verify_company():
    data = request.json
    success = verify_company(data.get('companyId'))
    return jsonify({"success": success})


from backend.report_ops import get_report_companies_with_jobs, get_report_applications_by_status, get_report_department_placement_stats

@app.route('/api/tpo/report/companies', methods=['GET'])
def tpo_report_companies():
    return jsonify(get_report_companies_with_jobs())

@app.route('/api/tpo/report/applications', methods=['GET'])
def tpo_report_applications():
    return jsonify(get_report_applications_by_status())

@app.route('/api/tpo/report/departments', methods=['GET'])
def tpo_report_departments():
    return jsonify(get_report_department_placement_stats())

if __name__ == "__main__":
    app.run(debug=True, port=5000)