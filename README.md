# 🌿 NutriFlow
### Personalized Diet & Vitamin Advisory System

A full-stack health and nutrition web application that 
analyzes symptoms, detects vitamin deficiencies, and 
provides personalized diet plans, daily routines, and 
health reminders.

## 🌐 Live Demo
https://diet-health-app.onrender.com

## ✨ Features
- 🔍 Health Analysis - Symptom-based vitamin deficiency detection
- 🥗 Diet Planning - Personalized meal plans (Veg/Non-Veg/Vegan)
- 📅 Routine Generator - Daily schedule based on health goals
- 🔔 Smart Reminders - Medicine, meal, water, exercise notifications
- 📊 Progress Tracker - Track daily health habits
- 👤 User Profile - Personal health history
- 🌙 Dark/Light Theme - Customizable interface
- 📱 PWA Support - Install on mobile like a native app

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Progressive Web App (PWA)
- Responsive Design (Mobile + Desktop)
- Chart.js for data visualization

### Backend
- Python 3.12
- Flask (REST API framework)
- Flask-CORS (Cross-origin resource sharing)
- Werkzeug (Password hashing)

### Database
- SQLite (Local development)

### Deployment
- GitHub (Version control)
- Render.com (Cloud hosting)

### Analysis Engine
- Rule-based inference system
- WHO nutritional standards
- Symptom to deficiency mapping
- BMI and vitals analysis

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/amarthya1/diet-health-app.git
cd diet-health-app
```

2. Set up virtual environment:
```bash
cd backend
python -m venv venv
venv\Scripts\activate.bat  (Windows)
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the app:
Double click start.bat
OR
```bash
python app.py
```

5. Open in browser:
http://127.0.0.1:5001

## 📱 Mobile Access
1. Open https://diet-health-app.onrender.com on phone
2. Tap menu (3 dots) → Add to Home Screen
3. App installs like a native app!

## 🔬 How It Works
1. User registers and completes health profile
2. User selects symptoms from interactive checklist
3. Rule-based engine maps symptoms to deficiencies
4. System generates personalized diet plan
5. Daily routine created based on goals
6. Browser notifications remind user of tasks
7. Progress tracked daily

## 📋 API Endpoints

### Authentication
- POST /api/user/register
- POST /api/user/login
- POST /api/user/forgot-password

### Health Analysis
- POST /api/health/analyze-health
- GET /api/health/history/<user_id>
- GET /api/health/latest/<user_id>

### Diet
- POST /api/diet/generate-diet
- GET /api/diet/get-plan/<user_id>

### Routine
- POST /api/routine/generate-routine
- GET /api/routine/get-routine/<user_id>

### Progress
- POST /api/progress/log
- GET /api/progress/<user_id>

### Reminders
- POST /api/reminders/save
- GET /api/reminders/<user_id>
- POST /api/reminders/add-custom
- DELETE /api/reminders/<reminder_id>

## 👨💻 Developer
- GitHub: @amarthya1

## 📄 License
MIT License

---
Built with ❤️ for health and wellness
