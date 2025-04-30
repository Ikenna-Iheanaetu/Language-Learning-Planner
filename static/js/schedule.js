document.addEventListener("DOMContentLoaded", function () {
  const scheduleData = JSON.parse(sessionStorage.getItem("schedule"));
  const container = document.getElementById("scheduleContainer");

  if (!scheduleData) {
    container.innerHTML = "<p class='text-danger'>No schedule data found. Please generate a schedule first.</p>";
    return;
  }

  for (const day in scheduleData) {
    const activities = scheduleData[day].map(act => `
      <div class="card mb-2 ${act.type === 'Review' ? 'bg-warning' : 'bg-info'} text-white">
        <div class="card-body p-2">
          <strong>${act.duration} mins</strong><br>
          ${act.type} - ${act.description}
        </div>
      </div>
    `).join("");

    container.innerHTML += `
      <div class="col">
        <h5>${day}</h5>
        ${activities}
      </div>
    `;
  }
});
