# 🥗 Diet & Health Analysis App

A full-stack diet planner and health analysis application.

- **Backend**: Python Flask REST API
- **Frontend**: Flutter (Android + Web)

---

## 📁 Project Structure

```
diet_health_app/
├── backend/                    ← Python Flask API
│   ├── app.py                  ← Flask entry point
│   ├── requirements.txt        ← Python dependencies
│   ├── .env.example            ← Environment variable template
│   ├── config/
│   │   └── settings.py         ← App configuration
│   ├── routes/
│   │   ├── diet_routes.py      ← /api/diet endpoints
│   │   ├── health_routes.py    ← /api/health endpoints
│   │   ├── user_routes.py      ← /api/user endpoints
│   │   └── analysis_routes.py  ← /api/analysis endpoints
│   ├── services/
│   │   ├── diet_service.py     ← Meal plan & food logic
│   │   ├── health_service.py   ← BMI, TDEE, vitals logic
│   │   ├── user_service.py     ← Auth & profile logic
│   │   └── analysis_service.py ← AI insights & reports
│   ├── data/
│   │   ├── models/
│   │   │   └── models.py       ← Domain dataclasses
│   │   └── sample_data/
│   │       └── foods.json      ← Sample food nutrition DB
│   └── utils/
│       └── helpers.py          ← Shared utility functions
│
└── frontend/                   ← Flutter App (Android + Web)
    ├── pubspec.yaml            ← Flutter dependencies
    ├── lib/
    │   ├── main.dart           ← App entry point
    │   ├── themes/
    │   │   └── app_theme.dart  ← Light & dark theme
    │   ├── services/
    │   │   └── api_service.dart ← HTTP client for Flask API
    │   ├── screens/
    │   │   ├── home/           ← Bottom nav shell
    │   │   ├── auth/           ← Login & registration
    │   │   ├── diet/           ← Meal planner & food log
    │   │   ├── health/         ← BMI, TDEE, vitals
    │   │   ├── analysis/       ← Charts & AI insights
    │   │   └── profile/        ← User profile & goals
    │   ├── widgets/            ← Reusable UI components
    │   ├── models/             ← Dart data models
    │   └── utils/              ← Helper utilities
    ├── assets/
    │   ├── images/             ← App images
    │   └── icons/              ← Custom icons
    ├── android/                ← Android build files
    └── web/                    ← Web build files
```

---

## 🚀 Getting Started

### Backend

```bash
cd backend

# Create a virtual environment
python -m venv venv
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
copy .env.example .env

# Run the server
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend

```bash
cd frontend

# Install Flutter packages
flutter pub get

# Run on web
flutter run -d chrome

# Run on Android (device/emulator must be connected)
flutter run -d android
```

---

## 🔗 API Endpoints

| Method | Endpoint                        | Description                  |
|--------|---------------------------------|------------------------------|
| GET    | `/api/diet/meal-plan`           | Get personalized meal plan   |
| POST   | `/api/diet/log-meal`            | Log a meal                   |
| GET    | `/api/diet/food-search?q=...`   | Search food nutrition DB     |
| POST   | `/api/health/bmi`               | Calculate BMI                |
| POST   | `/api/health/tdee`              | Calculate TDEE               |
| POST   | `/api/health/log-vitals`        | Log health vitals            |
| POST   | `/api/user/register`            | Register user                |
| POST   | `/api/user/login`               | Login user                   |
| GET    | `/api/analysis/weekly-report/:id` | Weekly diet report         |
| GET    | `/api/analysis/nutrient-gaps/:id` | Nutritional gap analysis   |
| GET    | `/api/analysis/vitamin-check/:id` | Vitamin level check        |
| GET    | `/api/analysis/ai-insights/:id`   | AI health insights         |
