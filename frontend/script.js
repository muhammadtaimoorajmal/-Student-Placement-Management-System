let currentUser = null;
let currentRole = null;

let tpoData = {
    students: [],
    companies: [],
    jobs: [],
    apps: []
};

function showModal(type, id) {
    const modal = document.getElementById('data-modal');
    const title = document.getElementById('modal-title');
    const body = document.getElementById('modal-body');
    
    modal.classList.remove('hidden');
    body.innerHTML = '';
    
    if (type === 'student') {
        const student = tpoData.students.find(s => (s.STUDENT_ID || s.student_id) === id);
        if (student) {
            title.textContent = "Student Profile";
            body.innerHTML = `
                <div><strong>ID:</strong> ${student.STUDENT_ID || student.student_id}</div>
                <div><strong>Name:</strong> ${student.NAME || student.name}</div>
                <div><strong>Email:</strong> ${student.EMAIL || student.email}</div>
                <div><strong>Phone:</strong> ${student.PHONE || student.phone || '-'}</div>
                <div><strong>Department:</strong> ${student.DEPARTMENT || student.department}</div>
                <div><strong>CGPA:</strong> ${student.CGPA || student.cgpa}</div>
                <div><strong>Grad Year:</strong> ${student.GRADUATION_YEAR || student.graduation_year || '-'}</div>
                <div style="grid-column: span 2;"><strong>Skills:</strong> ${student.SKILLS || student.skills || '-'}</div>
            `;
        }
    } else if (type === 'company') {
        const company = tpoData.companies.find(c => (c.COMPANY_ID || c.company_id) === id);
        if (company) {
            title.textContent = "Company Details";
            body.innerHTML = `
                <div><strong>ID:</strong> ${company.COMPANY_ID || company.company_id}</div>
                <div><strong>Name:</strong> ${company.COMPANY_NAME || company.company_name}</div>
                <div><strong>Industry:</strong> ${company.INDUSTRY || company.industry || '-'}</div>
                <div><strong>Email:</strong> ${company.EMAIL || company.email}</div>
                <div><strong>Phone:</strong> ${company.PHONE || company.phone || '-'}</div>
                <div><strong>Verified:</strong> ${(company.TPO_VERIFIED || company.tpo_verified) === 'Y' ? 'Yes' : 'No'}</div>
                <div style="grid-column: span 2;"><strong>Address:</strong> ${company.ADDRESS || company.address || '-'}</div>
            `;
        }
    }
}

function closeModal() {
    document.getElementById('data-modal').classList.add('hidden');
}

async function apiCall(endpoint, method = 'GET', body = null) {
    console.log(`[API] ${method} ${endpoint}`, body);
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) options.body = JSON.stringify(body);

    try {
        const response = await fetch(endpoint, options);
        if (!response.ok) {
            const text = await response.text();
            throw new Error(`Server Error (${response.status}): ${text}`);
        }
        return await response.json();
    } catch (err) {
        console.error(`[API Error] ${endpoint}:`, err);
        throw err;
    }
}

async function login() {
    const role = document.getElementById('role').value;
    const userId = document.getElementById('userId').value.trim();
    const password = document.getElementById('password').value.trim();
    const errorMsg = document.getElementById('login-error');

    if (!userId || !password) {
        alert("Please enter both ID and Password");
        return;
    }

    try {
        const res = await apiCall('/api/login', 'POST', { role, userId, password });

        if (res.success) {
            currentUser = userId;
            currentRole = role;
            errorMsg.style.display = 'none';

            // Switch view
            document.getElementById('login-section').classList.add('hidden');
            const dashboard = document.getElementById(`${role}-dashboard`);
            if (dashboard) {
                dashboard.classList.remove('hidden');
                loadDashboardData();
            } else {
                console.error(`Dashboard for role ${role} not found`);
            }
        } else {
            errorMsg.textContent = res.message || "Invalid credentials";
            errorMsg.style.display = 'block';
        }
    } catch (err) {
        alert("Login failed: " + err.message);
    }
}

function logout() {
    currentUser = null;
    currentRole = null;
    document.querySelectorAll('.dashboard-section').forEach(el => el.classList.add('hidden'));
    document.getElementById('login-section').classList.remove('hidden');
    document.getElementById('userId').value = '';
    document.getElementById('password').value = '';
}

function switchTab(role, tab) {
    // Update nav buttons
    const navButtons = document.querySelectorAll(`#${role}-dashboard .nav-links button`);
    navButtons.forEach(btn => btn.classList.remove('active'));
    if (event && event.target) {
        event.target.classList.add('active');
    }

    // Update views
    const cards = document.querySelectorAll(`#${role}-dashboard .info-card`);
    cards.forEach(c => c.classList.add('hidden'));
    const targetCard = document.getElementById(`${role}-${tab}`);
    if (targetCard) {
        targetCard.classList.remove('hidden');
    }
}

async function loadDashboardData() {
    console.log(`Loading dashboard data for ${currentRole} (${currentUser})`);

    // Show loading state
    const profileContent = document.getElementById(`${currentRole}-profile-content`);
    if (profileContent) profileContent.innerHTML = '<div style="grid-column: span 2;">Loading data...</div>';

    try {
        if (currentRole === 'student') {
            const details = await apiCall(`/api/student/details?userId=${currentUser}`);
            document.getElementById('student-profile-content').innerHTML = `
                <div><strong>Name:</strong> ${details.NAME || details.name || '-'}</div>
                <div><strong>Email:</strong> ${details.EMAIL || details.email || '-'}</div>
                <div><strong>Department:</strong> ${details.DEPARTMENT || details.department || '-'}</div>
                <div><strong>CGPA:</strong> ${details.CGPA || details.cgpa || '-'}</div>
                <div><strong>Skills:</strong> ${details.SKILLS || details.skills || '-'}</div>
            `;

            const jobs = await apiCall(`/api/student/jobs`);
            const jobsHtml = Array.isArray(jobs) ? jobs.map(j => `
                <tr>
                    <td>${j.COMPANY_NAME || j.company_name}</td>
                    <td>${j.JOB_TITLE || j.job_title}</td>
                    <td>${j.LOCATION || j.location}</td>
                    <td>${j.REQUIRED_CGPA || j.required_cgpa}</td>
                    <td><button class="btn btn-secondary" style="padding: 6px 12px; font-size: 12px;" onclick="applyJob('${j.JOB_ID || j.job_id}')">Apply</button></td>
                </tr>
            `).join('') : '<tr><td colspan="5">No jobs available</td></tr>';
            document.getElementById('student-jobs-list').innerHTML = jobsHtml || '<tr><td colspan="5">No jobs available</td></tr>';

            const apps = await apiCall(`/api/student/applications?userId=${currentUser}`);
            const appsHtml = Array.isArray(apps) ? apps.map(a => `
                <tr>
                    <td>${a.COMPANY_NAME || a.company_name}</td>
                    <td>${a.JOB_TITLE || a.job_title}</td>
                    <td><span class="status-badge status-${(a.STATUS || a.status || 'pending').toLowerCase()}">${a.STATUS || a.status}</span></td>
                </tr>
            `).join('') : '<tr><td colspan="3">No applications found</td></tr>';
            document.getElementById('student-apps-list').innerHTML = appsHtml || '<tr><td colspan="3">No applications found</td></tr>';
        }
        else if (currentRole === 'company') {
            const details = await apiCall(`/api/company/details?userId=${currentUser}`);
            document.getElementById('company-profile-content').innerHTML = `
                <div><strong>Company Name:</strong> ${details.COMPANY_NAME || details.company_name || '-'}</div>
                <div><strong>Industry:</strong> ${details.INDUSTRY || details.industry || '-'}</div>
                <div><strong>Email:</strong> ${details.EMAIL || details.email || '-'}</div>
                <div><strong>Verified:</strong> ${(details.TPO_VERIFIED || details.tpo_verified) === 'Y' ? 'Yes' : 'No'}</div>
            `;

            const jobs = await apiCall(`/api/company/jobs?userId=${currentUser}`);
            document.getElementById('company-jobs-list').innerHTML = Array.isArray(jobs) ? jobs.map(j => `
                <tr>
                    <td>${j.JOB_TITLE || j.job_title}</td>
                    <td>${j.LOCATION || j.location}</td>
                    <td>${j.REQUIRED_CGPA || j.required_cgpa}</td>
                    <td>${(j.DEADLINE_DATE || j.deadline_date || '').split('00:00')[0]}</td>
                    <td>${(j.IS_ACTIVE || j.is_active) === 'Y' ? 'Active' : 'Closed'}</td>
                </tr>
            `).join('') : '<tr><td colspan="5">No jobs posted</td></tr>';

            const applicants = await apiCall(`/api/company/applicants?userId=${currentUser}`);
            document.getElementById('company-applicants-list').innerHTML = Array.isArray(applicants) ? applicants.map(a => `
                <tr>
                    <td>${a.NAME || a.name} (${a.CGPA || a.cgpa} CGPA)</td>
                    <td>${a.JOB_TITLE || a.job_title}</td>
                    <td>${a.CGPA || a.cgpa}</td>
                    <td><span class="status-badge status-${(a.STATUS || a.status || 'pending').toLowerCase()}">${a.STATUS || a.status}</span></td>
                    <td>
                        <select onchange="updateStatus('${a.APPLICATION_ID || a.application_id}', this.value)">
                            <option value="">Update...</option>
                            <option value="Shortlisted">Shortlisted</option>
                            <option value="Selected">Selected</option>
                            <option value="Rejected">Rejected</option>
                        </select>
                    </td>
                </tr>
            `).join('') : '<tr><td colspan="5">No applicants found</td></tr>';
        }
        else if (currentRole === 'tpo') {
            tpoData.students = await apiCall('/api/tpo/students');
            document.getElementById('tpo-students-list').innerHTML = Array.isArray(tpoData.students) ? tpoData.students.map(s => `<tr><td>${s.STUDENT_ID || s.student_id}</td><td>${s.NAME || s.name}</td><td>${s.DEPARTMENT || s.department}</td><td>${s.CGPA || s.cgpa}</td><td><button class="btn btn-secondary" style="padding: 4px 8px; font-size: 12px;" onclick="showModal('student', '${s.STUDENT_ID || s.student_id}')">View</button></td></tr>`).join('') : '<tr><td colspan="5">No students found</td></tr>';

            tpoData.companies = await apiCall('/api/tpo/companies');
            document.getElementById('tpo-companies-list').innerHTML = Array.isArray(tpoData.companies) ? tpoData.companies.map(c => `<tr><td>${c.COMPANY_ID || c.company_id}</td><td>${c.COMPANY_NAME || c.company_name}</td><td>${c.INDUSTRY || c.industry}</td><td>${c.TPO_VERIFIED || c.tpo_verified}</td><td>
                <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 12px;" onclick="showModal('company', '${c.COMPANY_ID || c.company_id}')">View</button>
                ${(c.TPO_VERIFIED || c.tpo_verified) !== 'Y' ? `<button class="btn" style="padding: 4px 8px; font-size: 12px; margin-left: 5px;" onclick="verifyCompany('${c.COMPANY_ID || c.company_id}')">Verify</button>` : ''}
            </td></tr>`).join('') : '<tr><td colspan="5">No companies found</td></tr>';

            tpoData.jobs = await apiCall('/api/tpo/jobs');
            document.getElementById('tpo-jobs-list').innerHTML = Array.isArray(tpoData.jobs) ? tpoData.jobs.map(j => `<tr><td>${j.JOB_ID || j.job_id}</td><td>${j.JOB_TITLE || j.job_title}</td><td>${j.COMPANY_NAME || j.company_name}</td><td>${j.LOCATION || j.location}</td></tr>`).join('') : '<tr><td colspan="4">No jobs found</td></tr>';

            tpoData.apps = await apiCall('/api/tpo/applications');
            document.getElementById('tpo-apps-list').innerHTML = Array.isArray(tpoData.apps) ? tpoData.apps.map(a => `<tr><td>${a.APPLICATION_ID || a.application_id}</td><td>${a.STUDENT_NAME || a.student_name} (${a.STUDENT_CGPA || a.student_cgpa})</td><td>${a.JOB_TITLE || a.job_title} - ${a.COMPANY_NAME || a.company_name}</td><td><span class="status-badge status-${(a.STATUS || a.status || 'pending').toLowerCase()}">${a.STATUS || a.status}</span></td></tr>`).join('') : '<tr><td colspan="4">No applications found</td></tr>';

            // Load Reports
            const repCompanies = await apiCall('/api/tpo/report/companies');
            document.getElementById('report-companies-list').innerHTML = Array.isArray(repCompanies) ? repCompanies.map(r => {
                const name = r.COMPANY_NAME || r.company_name || '-';
                const jobs = r.TOTAL_JOBS ?? r.total_jobs ?? 0;
                return `<tr><td>${name}</td><td>${jobs}</td></tr>`;
            }).join('') : '';

            const repApps = await apiCall('/api/tpo/report/applications');
            document.getElementById('report-apps-list').innerHTML = Array.isArray(repApps) ? repApps.map(r => {
                const status = r.STATUS || r.status || '-';
                const count = r.COUNT ?? r.count ?? 0;
                return `<tr><td>${status}</td><td>${count}</td></tr>`;
            }).join('') : '';

            const repDepts = await apiCall('/api/tpo/report/departments');
            document.getElementById('report-depts-list').innerHTML = Array.isArray(repDepts) ? repDepts.map(r => {
                const dept = r.DEPARTMENT || r.department || '-';
                const placed = r.TOTAL_PLACED ?? r.total_placed ?? 0;
                const pkg = r.AVG_PACKAGE ?? r.avg_package ?? '0.00';
                return `<tr><td>${dept}</td><td>${placed}</td><td>${pkg}</td></tr>`;
            }).join('') : '';
        }
    } catch (err) {
        console.error("Error loading dashboard data:", err);
        alert("Failed to load dashboard data. Please ensure your Oracle database is running and credentials in database/db_config.py are correct.");
    }
}


async function applyJob(jobId) {
    try {
        const res = await apiCall('/api/student/apply', 'POST', { userId: currentUser, jobId });
        if (res.success) {
            alert("Applied successfully!");
            loadDashboardData();
        } else {
            alert("Application failed. You might have already applied or your CGPA is low.");
        }
    } catch (err) {
        alert("Error applying: " + err.message);
    }
}

async function postJob() {
    const title = document.getElementById('job-title').value;
    const location = document.getElementById('job-location').value;
    const cgpa = document.getElementById('job-cgpa').value;
    const deadline = document.getElementById('job-deadline').value;
    const desc = document.getElementById('job-desc').value;

    try {
        const res = await apiCall('/api/company/post_job', 'POST', {
            companyId: currentUser,
            title, location, reqCgpa: cgpa, deadline, description: desc
        });
        if (res.success) {
            alert("Job posted!");
            document.getElementById('post-job-form').classList.add('hidden');
            loadDashboardData();
        } else {
            alert("Failed to post job");
        }
    } catch (err) {
        alert("Error posting job: " + err.message);
    }
}

async function updateStatus(appId, status) {
    if (!status) return;
    try {
        const res = await apiCall('/api/company/update_status', 'POST', { applicationId: appId, status });
        if (res.success) {
            alert("Status updated!");
            loadDashboardData();
        }
    } catch (err) {
        alert("Error updating status: " + err.message);
    }
}

async function verifyCompany(companyId) {
    try {
        const res = await apiCall('/api/tpo/verify_company', 'POST', { companyId });
        if (res.success) {
            alert("Company verified!");
            loadDashboardData();
        }
    } catch (err) {
        alert("Error verifying company: " + err.message);
    }
}

