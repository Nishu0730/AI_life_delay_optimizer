// 🔔 REQUEST PERMISSION
let currentEditTaskId = null;

function showNotification(message) {

    const box =
        document.getElementById(
            "notificationBox"
        );

    box.innerText =
        message;

    box.classList.remove(
        "hidden"
    );

    setTimeout(() => {

        box.classList.add(
            "hidden"
        );

    }, 3000);
}

async function requestNotificationPermission() {
    if ("Notification" in window) {
        const permission = await Notification.requestPermission();
        console.log("Notification permission:", permission);
    }
}

// 🔥 STORE LAST NOTIFICATION (prevents spam)
let lastNotification = "";
let lastProblemNotification = "";
let analyticsCache = {};


async function getCurrentLocation() {

    return new Promise((resolve) => {

        if (!navigator.geolocation) {

            console.log(
                "Geolocation not supported"
            );

            resolve({
                lat: null,
                lon: null
            });

            return;
        }

        navigator.geolocation.getCurrentPosition(

            (position) => {

                console.log(
                    "GPS Success:",
                    position.coords.latitude,
                    position.coords.longitude
                );

                resolve({
                    lat:
                        position.coords.latitude,
                    lon:
                        position.coords.longitude
                });

            },

            (error) => {

                console.log(
                    "GPS Error:",
                    error
                );

                resolve({
                    lat: null,
                    lon: null
                });

            },

            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    });
}


async function loadDashboard() {

    // GET TASKS
    const tasksResponse = await fetch('/tasks');
    const tasksData = await tasksResponse.json();
    const tasks = tasksData.tasks;

    // 🔥 TODAY'S SCHEDULE

    const scheduleList = document.getElementById('scheduleList');
    scheduleList.innerHTML = "";

    tasks.sort((a, b) => a.planned_time.localeCompare(b.planned_time));

    tasks.forEach(task => {

    const li = document.createElement("li");

    li.innerHTML = `
    <div>
        ${task.status === "completed" ? "✔️ " : ""}
        ${task.planned_time} -
        ${task.task_name}
        (${task.task_type})
    </div>

    <div class="schedule-buttons">

        <button
            type="button"
            onclick="editTask(${task.id})"
        >
            ✏️ Edit
        </button>

        <button
            type="button"
            onclick="deleteTask(${task.id})"
        >
            🗑 Delete
        </button>

        ${task.status === "completed"
    ? `
        <button
            type="button"
            disabled
            style="
                opacity:0.5;
                cursor:not-allowed;
            "
        >
            ✔️ Completed
        </button>
      `
    : `
        <button
            type="button"
            onclick="completeTask(${task.id})"
        >
            ✅ Complete
        </button>
      `
}

    </div>
`;

    scheduleList.appendChild(li);
});
    await generateSmartNotification(tasks);
    loadTopProblem();


    // TOTAL TASKS
    document.getElementById('totalTasks').innerText = tasks.length;

    // COMPLETED TASKS
    const completed = tasks.filter(t => t.status === "completed");
    document.getElementById('completedTasks').innerText = completed.length;

    // DELAYED TASKS
    const delayed = completed.filter(t => {
        if (!t.actual_start) return false;
        return t.actual_start > t.planned_time;
    });
    document.getElementById('delayedTasks').innerText = delayed.length;

    // PRODUCTIVITY SCORE
    const scoreResponse = await fetch('/productivity_score');
    const scoreData = await scoreResponse.json();
    document.getElementById('score').innerText =
        scoreData.productivity.score;

    // RECOMMENDATIONS
    const recResponse = await fetch('/recommendations');
    const recData = await recResponse.json();
    const recList = document.getElementById('recommendations');
    recList.innerHTML = "";
    recData.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.innerText = rec;
        recList.appendChild(li);
    });

    // INSIGHTS
    const insightsResponse = await fetch('/insights');
    const insightsData = await insightsResponse.json();
    const insightsList = document.getElementById('insights');
    insightsList.innerHTML = "";
    insightsData.insights.forEach(ins => {
        const li = document.createElement('li');
        li.innerText = ins;
        insightsList.appendChild(li);
    });

    // TRAVEL
    const location =
    await getCurrentLocation();
    if (
    !location.lat ||
    !location.lon
) {
    location.lat = 12.9716;
    location.lon = 77.5946;

    console.log(
        "Using default Bengaluru coordinates."
    );
}

const travelResponse =
    await fetch('/travel_advice/1', {
        method: "POST",
        headers: {
            "Content-Type":
                "application/json"
        },
        body: JSON.stringify({
            user_lat: location.lat,
            user_lon: location.lon
        })
    });
    const travelData = await travelResponse.json();
    document.getElementById('travel').innerText =
        travelData.travel_advice || "No travel required";

    // SMART SCHEDULER
    const scheduleResponse = await fetch('/smart_schedule');
    const scheduleData = await scheduleResponse.json();
    document.getElementById('schedule').innerText =
        scheduleData.suggestion;

    // ANALYTICS CHART

    const analyticsResponse = await fetch('/analytics_data');
    const analyticsData = await analyticsResponse.json();

    let labels = Object.keys(analyticsData.analytics);
    let values = Object.values(analyticsData.analytics);

    const filteredLabels = [];
    const filteredValues = [];

    labels.forEach((label, i) => {
        if (values[i] > 0) {
            filteredLabels.push(label);
            filteredValues.push(values[i]);
        }
    });

    if (filteredLabels.length === 0) {
        filteredLabels.push("No Data");
        filteredValues.push(1);
    }

    const ctx = document.getElementById('delayChart');

    if (window.delayChartInstance) {
        window.delayChartInstance.destroy();
    }

    window.delayChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: filteredLabels,
            datasets: [{
                label: 'Average Delay (mins)',
                data: filteredValues,
                backgroundColor: 'rgba(56, 189, 248, 0.7)',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // WEEKLY TREND

    const trendResponse = await fetch('/weekly_trend');
    const trendData = await trendResponse.json();

    const trendLabels = Object.keys(trendData.trend);
    const trendValues = Object.values(trendData.trend);

    const trendCtx = document.getElementById('trendChart');

    if (window.trendChartInstance) {
        window.trendChartInstance.destroy();
    }

    window.trendChartInstance = new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: trendLabels,
            datasets: [{
                label: 'Weekly Delay Trend',
                data: trendValues,
                borderColor: '#38bdf8',
                backgroundColor: 'rgba(56, 189, 248, 0.2)',
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}


// 🔥 NOTIFICATION FUNCTION

function showNotification(message) {

    // 🔔 Browser notification
    if (
        "Notification" in window &&
        Notification.permission === "granted"
    ) {

        new Notification(
            "AI Life Delay Optimizer",
            {
                body: message,
                icon: "https://cdn-icons-png.flaticon.com/512/1827/1827370.png"
            }
        );
    }

    // 🔔 Notification box on dashboard
    const box =
        document.getElementById(
            "notificationBox"
        );

    if (!box)
        return;

    // Reset animation if already visible
    box.classList.add("hidden");

    setTimeout(() => {

        box.innerText = message;

        box.classList.remove(
            "hidden"
        );

        box.style.display =
            "block";

        // Auto hide after 5 sec
        setTimeout(() => {

            box.classList.add(
                "hidden"
            );

            box.style.display =
                "none";

        }, 5000);

    }, 100);
}
async function generateSmartNotification(tasks) {

    const analyticsResponse =
        await fetch('/analytics_data');

    const analyticsData =
        await analyticsResponse.json();

    analyticsCache =
        analyticsData.analytics || {};

    const now = new Date();

    const currentTime =
        now.getHours() * 60 +
        now.getMinutes();

    const upcoming = tasks
        .map(task => ({
            ...task,
            timeMin:
                parseInt(task.planned_time.split(":")[0]) * 60 +
                parseInt(task.planned_time.split(":")[1])
        }))
        .sort((a, b) =>
            a.timeMin - b.timeMin
        )
        .find(task =>
            task.timeMin >= currentTime &&
            task.status !== "completed"
        );

    if (!upcoming)
        return;

    const diff =
        upcoming.timeMin -
        currentTime;

    let message = "";

    if (
        diff <= 10 &&
        diff >= 0
    ) {

        message =
            `⏰ ${upcoming.task_name} starts in ${diff} mins.`;
    }

    else if (
        upcoming.location &&
        diff <= 30
    ) {

        message =
            `🚗 Leave soon for ${upcoming.task_name} at ${upcoming.location}.`;
    }

    if (
        message &&
        message !== lastNotification
    ) {

        showNotification(message);

        lastNotification =
            message;
    }
}
function loadTopProblem() {

    let worstTask = "";
    let worstDelay = 0;

    Object.entries(
        analyticsCache
    ).forEach(([task, delay]) => {

        if (delay > worstDelay) {

            worstTask = task;
            worstDelay = delay;
        }
    });

    if (
        worstTask &&
        worstDelay > 0
    ) {

        const message =
            `📊 ${worstTask} has been your most delayed activity (${Math.round(worstDelay)} mins average delay).`;

        if (
            message !==
            lastProblemNotification
        ) {

            showNotification(
                message
            );

            lastProblemNotification =
                message;
        }
    }
}

// 🔥 ADD TASK

async function addTask() {

    const name = document.getElementById('taskName').value;
    const time = document.getElementById('taskTime').value;
    let type = document.getElementById('taskType').value;
    const location = document.getElementById('taskLocation')?.value || "";

    type = type.toLowerCase();

    if (type.includes("meeting")) type = "Meeting";
    else if (type.includes("exercise") || type.includes("gym")) type = "Exercise";
    else if (type.includes("sleep")) type = "Sleep";
    else if (type.includes("work")) type = "Deep Work";
    else if (type.includes("entertainment")) type = "Entertainment";
    else type = type.charAt(0).toUpperCase() + type.slice(1);

    await fetch('/add_task', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            task_name: name,
            planned_time: time,
            task_type: type,
            location: location,
            planned_duration: 60,
            priority: "medium",
            difficulty: 3
        })
    });

    document.getElementById('taskName').value = "";
    document.getElementById('taskTime').value = "";
    document.getElementById('taskType').value = "";

    loadDashboard();
    showNotification(
    "✅ Task added successfully"
);
}

async function editTask(taskId) {

    console.log("Edit clicked", taskId);

    const response =
        await fetch("/tasks");

    console.log("Fetched tasks");

    const data =
        await response.json();

    console.log(data);

    const tasks =
        data.tasks;

    console.log(tasks);

    const task =
        tasks.find(
            t => t.id === taskId
        );

    console.log("Found task:", task);

    if (!task) {
        console.log("Task not found");
        return;
    }

    currentEditTaskId =
        taskId;

    document.getElementById(
        "editName"
    ).value =
        task.task_name;

    document.getElementById(
        "editTime"
    ).value =
        task.planned_time;

    document.getElementById(
        "editType"
    ).value =
        task.task_type;

    document.getElementById(
        "editLocation"
    ).value =
        task.location;

    console.log("Opening modal");

    document.getElementById(
        "editModal"
    ).style.display =
        "flex";
}


function closeEditModal() {

    document.getElementById(
        "editModal"
    ).style.display =
        "none";

    currentEditTaskId =
        null;
}

async function saveEditTask() {

    if (
        currentEditTaskId === null
    ) {
        return;
    }

    const taskName =
        document.getElementById(
            "editName"
        ).value;

    const taskTime =
        document.getElementById(
            "editTime"
        ).value;

    const taskType =
        document.getElementById(
            "editType"
        ).value;

    const taskLocation =
        document.getElementById(
            "editLocation"
        ).value;

    await fetch(
        `/update_task/${currentEditTaskId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                task_name:
                    taskName,
                planned_time:
                    taskTime,
                task_type:
                    taskType,
                location:
                    taskLocation
            })
        }
    );

    closeEditModal();

    loadDashboard();
    showNotification(
    "✏️ Task updated successfully"
);
}

window.onclick = function (event) {

    const modal =
        document.getElementById(
            "editModal"
        );

    if (
        event.target === modal
    ) {

        closeEditModal();
    }
};

async function deleteTask(taskId) {

    const confirmDelete =
        confirm(
            "Delete this task?"
        );

    if (!confirmDelete)
        return;

    await fetch(
        `/delete_task/${taskId}`,
        {
            method: "DELETE"
        }
    );

    loadDashboard();
    loadDashboard();
}

async function completeTask(taskId) {

    const now =
        new Date();

    const actualStart =
        now.toTimeString()
            .slice(0, 5);

    await fetch(
        `/complete_task/${taskId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                actual_start:
                    actualStart,

                actual_end:
                    actualStart,

                actual_duration:
                    0
            })
        }
    );

    loadDashboard();
    showNotification(
    "🎉 Task completed"
);
}
const themeButton =
    document.getElementById(
        "themeToggle"
    );

themeButton.onclick = function () {

    document.body.classList.toggle(
        "light-theme"
    );

    const light =
        document.body.classList.contains(
            "light-theme"
        );

    localStorage.setItem(
        "theme",
        light ? "light" : "dark"
    );

    themeButton.innerText =
        light
            ? "🌞 Light Mode"
            : "🌙 Dark Mode";
};
if (
    localStorage.getItem(
        "theme"
    ) === "light"
) {

    document.body.classList.add(
        "light-theme"
    );

    document.getElementById(
        "themeToggle"
    ).innerText =
        "🌞 Light Mode";
}
// 🔥 INIT

requestNotificationPermission();
setInterval(loadDashboard, 60000);
loadDashboard();