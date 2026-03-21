/* === NutriFlow - Core JS === */
const BASE_URL = (() => {
    const hostname = window.location.hostname;
    
    if (hostname === 'localhost' || 
        hostname === '127.0.0.1' ||
        hostname === '192.168.1.3') {
        return 'http://' + hostname + ':5001/api';
    } else {
        return 'https://' + hostname + '/api';
    }
})();

/* --- Auth --- */
const Auth = {
    saveUser(u) {
        const d = typeof u === 'object' ? u : {};
        localStorage.setItem('user', JSON.stringify(d));
        if (d.id) localStorage.setItem('userId', d.id);
    },
    getUser() {
        try { return JSON.parse(localStorage.getItem('user') || '{}'); } catch { return {}; }
    },
    getUserId() { return localStorage.getItem('userId'); },
    isLoggedIn() { return !!this.getUserId(); },
    logout() { localStorage.clear(); window.location.href = 'login.html'; },
    checkAuth() {
        const p = window.location.pathname;
        const pub = ['login.html','register.html','forgot-password.html','reset-password.html',''];
        const isPublic = pub.some(x => p.endsWith(x)) || p === '/';
        if (!this.isLoggedIn() && !isPublic) window.location.href = 'login.html';
    }
};

/* --- API --- */
const API = {
    async post(ep, data) { return this.req(ep, 'POST', data); },
    async get(ep) { return this.req(ep, 'GET'); },
    async put(ep, data) { return this.req(ep, 'PUT', data); },
    async req(ep, method, data) {
        showLoading();
        try {
            const opts = { method, headers: { 'Content-Type': 'application/json' } };
            if (data) opts.body = JSON.stringify(data);
            const res = await fetch(`${BASE_URL}${ep}`, opts);
            if (res.status === 401) { Auth.logout(); throw new Error('Session expired'); }
            const json = await res.json();
            if (!res.ok) throw new Error(json.message || 'Request failed');
            return json;
        } catch (e) {
            if (e.message === 'Failed to fetch') {
                showToast('Cannot connect to server. Is the backend running?', 'error');
            } else {
                showToast(e.message, 'error');
            }
            throw e;
        } finally { hideLoading(); }
    },
    async ping() {
        try { const r = await fetch(`${BASE_URL}/status`); return r.ok; }
        catch { return false; }
    }
};

/* --- Theme --- */
const Theme = {
    load() {
        const t = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', t);
    },
    toggle() {
        const cur = document.documentElement.getAttribute('data-theme');
        const next = cur === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
    },
    get() { return localStorage.getItem('theme') || 'light'; }
};

/* --- UI Helpers --- */
function showLoading() { const l = document.getElementById('loading-overlay'); if (l) l.style.display = 'flex'; }
function hideLoading() { const l = document.getElementById('loading-overlay'); if (l) l.style.display = 'none'; }

function showToast(msg, type = 'success') {
    let c = document.getElementById('toast-container');
    if (!c) { c = document.createElement('div'); c.id = 'toast-container'; document.body.appendChild(c); }
    const t = document.createElement('div');
    t.className = `toast toast-${type}`;
    t.textContent = msg;
    c.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; setTimeout(() => t.remove(), 300); }, 3000);
}

function showError(msg) {
    const el = document.getElementById('error-message');
    if (el) { el.textContent = msg; el.style.display = 'block'; setTimeout(() => el.style.display = 'none', 8000); }
    else showToast(msg, 'error');
}

function formatDate(d) {
    const dt = new Date(d);
    return dt.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

function calculateBMI(w, h) {
    if (!w || !h) return 0;
    const hm = h / 100;
    return Math.round((w / (hm * hm)) * 10) / 10;
}

function getBMICategory(bmi) {
    if (bmi < 18.5) return { cat: 'Underweight', color: '#F59E0B' };
    if (bmi <= 24.9) return { cat: 'Normal', color: '#10B981' };
    if (bmi <= 29.9) return { cat: 'Overweight', color: '#F59E0B' };
    return { cat: 'Obese', color: '#EF4444' };
}

function getGreeting() {
    const h = new Date().getHours();
    if (h < 12) return 'Good morning';
    if (h < 17) return 'Good afternoon';
    return 'Good evening';
}

function getInitials(name) {
    return (name || 'U').split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
}

/* --- Global Init --- */
document.addEventListener('DOMContentLoaded', async () => {
    Theme.load();
    Auth.checkAuth();

    // Set active nav
    const page = window.location.pathname.split('/').pop() || 'home.html';
    document.querySelectorAll('.nav-item,.nav-desktop a').forEach(a => {
        if (a.getAttribute('href') === page) { a.classList.add('active'); }
        else { a.classList.remove('active'); }
    });

    // Logout
    document.querySelectorAll('.logout-btn').forEach(b => { b.onclick = e => { e.preventDefault(); Auth.logout(); }; });

    // Ping server (non-blocking)
    API.ping().then(ok => { if (!ok) showToast('Server offline. Start the backend.', 'warning'); });
});

/* --- Reminders Sync --- */
const RemindersSync = {
    async afterLogin() {
        if (!Auth.isLoggedIn()) return;
        try {
            const bRems = await API.get('/routine/reminders/' + Auth.getUserId());
            if (bRems && Array.isArray(bRems)) {
                // Extract custom reminders
                const customs = bRems.filter(r => r.category !== 'routine');
                const customRems = customs.map(c => ({
                    backend_id: c.id, title: c.title, body: c.body, time: c.reminder_time, 
                    repeat: c.repeat_type, category: c.category, active: c.is_active === 1
                }));
                localStorage.setItem("customReminders", JSON.stringify(customRems));
                
                // Extract preferences
                const routineParts = bRems.filter(r => r.category === 'routine');
                const activePrefs = JSON.parse(localStorage.getItem('reminderPrefs') || '{}');
                routineParts.forEach(rp => {
                    // Try to map back to default ids based on title...
                    // Let's just store the fact they are loaded
                });
            }
            if (window.scheduleAllReminders) scheduleAllReminders();
        } catch(e) {}
    },
    async afterRoutineGenerated(r) {
        if (!r) return;
        localStorage.setItem("userRoutine", JSON.stringify(r));
        if (window.scheduleAllReminders) scheduleAllReminders();
    },
    async afterProfileUpdate(p) {
        if (!p) return;
        if (p.medications) {
            let userMeds = p.medications.split(',').map(m => m.trim()).filter(Boolean).map(m => {
                let obj = {name: m, time: "09:00"};
                if (m.toLowerCase().includes('morning')) obj.time = "08:00";
                if (m.toLowerCase().includes('night')) obj.time = "21:00";
                return obj;
            });
            localStorage.setItem("userMedications", JSON.stringify(userMeds));
        } else {
            localStorage.setItem("userMedications", "[]");
        }
        if (window.scheduleAllReminders) scheduleAllReminders();
    }
};
