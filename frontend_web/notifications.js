/* notifications.js */
function requestNotificationPermission() {
    if ("Notification" in window) {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                showToast("Notifications enabled!", "success");
            }
        });
    }
}

function scheduleReminder(id, title, body, timeString) {
    const now = new Date();
    const [hours, minutes] = timeString.split(":").map(Number);
    
    const reminderTime = new Date();
    reminderTime.setHours(hours, minutes, 0, 0);
    
    if (reminderTime <= now) {
        reminderTime.setDate(reminderTime.getDate() + 1);
    }
    
    const delay = reminderTime - now;
    
    const timerId = setTimeout(() => {
        if (Notification.permission === "granted") {
            new Notification(title, {
                body: body,
                icon: "/static/icon-192.png",
                badge: "/static/icon-192.png",
                tag: id
            });
        }
        scheduleReminder(id, title, body, timeString);
    }, delay);
    
    const reminders = JSON.parse(localStorage.getItem("activeReminders") || "{}");
    reminders[id] = { title, body, timeString, timerId };
    localStorage.setItem("activeReminders", JSON.stringify(reminders));
}

function cancelReminder(id) {
    const reminders = JSON.parse(localStorage.getItem("activeReminders") || "{}");
    if (reminders[id]) {
        clearTimeout(reminders[id].timerId);
        delete reminders[id];
        localStorage.setItem("activeReminders", JSON.stringify(reminders));
    }
}

function cancelAllReminders() {
    const reminders = JSON.parse(localStorage.getItem("activeReminders") || "{}");
    Object.keys(reminders).forEach(id => {
        clearTimeout(reminders[id].timerId);
    });
    localStorage.setItem("activeReminders", "{}");
}

function scheduleAllReminders() {
    const routine = JSON.parse(localStorage.getItem("userRoutine") || "null");
    const user = JSON.parse(localStorage.getItem("user") || "null");
    
    if (!routine) return;
    
    cancelAllReminders();
    
    const defaultReminders = [
        {
            id: "wake_water",
            title: "Good Morning! 🌅",
            body: "Start your day with 2 glasses of water",
            time: routine.wake_time || "07:00"
        },
        {
            id: "breakfast",
            title: "Breakfast Time! 🍳",
            body: "Time for a healthy breakfast",
            time: routine.breakfast_time || "08:00"
        },
        {
            id: "water_morning",
            title: "Stay Hydrated! 💧",
            body: "Drink a glass of water",
            time: "10:00"
        },
        {
            id: "lunch",
            title: "Lunch Time! 🥗",
            body: "Time for your healthy lunch",
            time: routine.lunch_time || "13:00"
        },
        {
            id: "water_afternoon",
            title: "Drink Water! 💧",
            body: "Have a glass of water",
            time: "15:00"
        },
        {
            id: "snack",
            title: "Snack Time! 🍎",
            body: "Have a healthy snack",
            time: "16:00"
        },
        {
            id: "exercise",
            title: "Exercise Time! 💪",
            body: "Time for your daily workout",
            time: routine.exercise_time || "17:00"
        },
        {
            id: "dinner",
            title: "Dinner Time! 🍽️",
            body: "Time for a light healthy dinner",
            time: routine.dinner_time || "19:00"
        },
        {
            id: "water_evening",
            title: "Evening Water! 💧",
            body: "Have a glass of water",
            time: "20:00"
        },
        {
            id: "sleep",
            title: "Sleep Time! 😴",
            body: "Time to wind down for bed",
            time: routine.sleep_time || "22:00"
        }
    ];
    
    defaultReminders.forEach(reminder => {
        scheduleReminder(
            reminder.id,
            reminder.title,
            reminder.body,
            reminder.time
        );
    });
    
    const medications = JSON.parse(localStorage.getItem("userMedications") || "[]");
    medications.forEach((med, index) => {
        scheduleReminder(
            "med_" + index,
            "Medicine Reminder 💊",
            "Time to take: " + med.name,
            med.time
        );
    });
    
    const customReminders = JSON.parse(localStorage.getItem("customReminders") || "[]");
    customReminders.forEach(reminder => {
        if (reminder.active) {
            scheduleReminder(
                reminder.id,
                reminder.title,
                reminder.body,
                reminder.time
            );
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    if (Notification.permission === "granted") {
        scheduleAllReminders();
    } else if (Notification.permission === "default") {
        requestNotificationPermission();
    }
});
