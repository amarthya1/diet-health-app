import os

folder = 'd:/project - Copy/diet_health_app/frontend_web'
files = [f for f in os.listdir(folder) if f.endswith('.html') and f != 'reminders.html']

for fn in files:
    path = os.path.join(folder, fn)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Desktop nav
    content = content.replace(
        '<a href="routine.html">Routine</a><a href="progress.html">Progress</a>',
        '<a href="routine.html">Routine</a><a href="reminders.html">Reminders</a><a href="progress.html">Progress</a>'
    )
    content = content.replace(
        '<a href="routine.html">Routine</a>\n            <a href="progress.html">Progress</a>',
        '<a href="routine.html">Routine</a><a href="reminders.html">Reminders</a>\n            <a href="progress.html">Progress</a>'
    )

    # Bottom nav
    content = content.replace(
        '<a href="routine.html" class="nav-item"><span>📅</span>Routine</a>\n        <a href="profile.html" class="nav-item"><span>👤</span>Profile</a>',
        '<a href="routine.html" class="nav-item"><span>📅</span>Routine</a>\n        <a href="reminders.html" class="nav-item"><span>⏰</span>Reminders</a>\n        <a href="profile.html" class="nav-item"><span>👤</span>Profile</a>'
    )
    
    # Analysis page has slightly different bottom nav missing progress?
    # Profile has same bottom nav.
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated', fn)
