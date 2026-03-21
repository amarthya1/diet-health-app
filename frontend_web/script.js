
const API_BASE = 'http://127.0.0.1:5001/api';

async function login(email, password) {
    if (!email || !password) {
        alert('Email and password are required.');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/user/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Login failed');
        }

        localStorage.setItem('userEmail', email);
        alert('Login successful!');
        window.location.href = 'home.html';
        return data;
    } catch (error) {
        console.error('Login error:', error);
        alert(`Login error: ${error.message}`);
        throw error;
    }
}

async function register(email, password) {
    if (!email || !password) {
        alert('Email and password are required.');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/user/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Registration failed');
        }

        alert('Registration successful! Please login.');
        window.location.href = 'login.html';
        return data;
    } catch (error) {
        console.error('Registration error:', error);
        alert(`Registration error: ${error.message}`);
        throw error;
    }
}

function logout() {
    try {
        localStorage.clear();
        alert('Logged out successfully.');
        window.location.href = 'login.html';
    } catch (error) {
        console.error('Logout error:', error);
        alert('Logout error. Please try again.');
    }
}

async function analyzeHealth(data) {
    if (!data || typeof data !== 'object') {
        throw new Error('Invalid data for health analysis.');
    }

    try {
        const response = await fetch(`${API_BASE}/health/analyze-health`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || 'Health analysis failed');
        }

        alert('Health analysis complete.');
        return result;
    } catch (error) {
        console.error('Analyze health error:', error);
        alert(`Analyze health error: ${error.message}`);
        throw error;
    }
}

async function getDietPlan(deficiency, foodPreference) {
    if (!deficiency || !foodPreference) {
        throw new Error('Deficiency and food preference are required.');
    }

    try {
        const response = await fetch(`${API_BASE}/diet/generate-diet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ deficiency, foodPreference })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || 'Diet plan generation failed');
        }

        alert('Diet plan generated successfully.');
        return result;
    } catch (error) {
        console.error('Get diet plan error:', error);
        alert(`Diet plan error: ${error.message}`);
        throw error;
    }
}

window.appApi = {
    login,
    register,
    logout,
    analyzeHealth,
    getDietPlan
};
