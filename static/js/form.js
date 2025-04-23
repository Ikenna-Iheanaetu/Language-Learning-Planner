document.getElementById("plannerForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = {
    targetLanguage: document.getElementById("targetLanguage").value,
    nativeLanguage: document.getElementById("nativeLanguage").value,
    proficiency: document.querySelector('input[name="proficiency"]:checked')?.value,
    goal: document.getElementById("goal").value,
    timeCommitment: document.getElementById("timeCommitment").value,
    availableDays: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value)
  };

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData)
    });

    if (!res.ok) throw new Error("Failed to generate schedule.");
    const schedule = await res.json();

    sessionStorage.setItem("schedule", JSON.stringify(schedule));
    window.location.href = "/schedule";
  } catch (err) {
    alert("Error: " + err.message);
  }
});

document.getElementById("timeCommitment").addEventListener("input", function () {
  document.getElementById("timeValue").innerText = this.value;
});
