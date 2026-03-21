@echo off
echo ================================
echo    Diet and Health App
echo ================================
echo Starting backend server...
cd /d "D:\project\diet_health_app\backend"
call venv\Scripts\activate.bat
start "" http://127.0.0.1:5001
python app.py
pause
```

---

**Step 3 — Save the file**

1. Click **File** → **Save As**
2. On the left side click **This PC** → **D drive** → **project** → **diet_health_app**
3. At the bottom change these:
   - File name: `start`
   - Save as type: click the dropdown → select **All Files**
4. Click **Save**

---

**Step 4 — Check it saved correctly**

Open File Explorer and go to:
```
D:\project\diet_health_app\