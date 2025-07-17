const form = document.getElementById("journalForm");
const textArea = document.getElementById("journalText");
const resultBox = document.getElementById("resultContainer");
const resultText = document.getElementById("resultText");
const emotionSpan = document.getElementById("emotion");
const adviceSpan = document.getElementById("advice");
const themeSpan = document.getElementById("theme");
const historyList = document.getElementById("historyList");

const API_URL = "https://jurnai.onrender.com/analyze";

// încarcă jurnalele salvate
function loadHistory() {
  const entries = JSON.parse(localStorage.getItem("journalEntries") || "[]");
  historyList.innerHTML = "";
  entries.reverse().forEach(entry => {
    const li = document.createElement("li");
    li.textContent = `${entry.date} – ${entry.preview}`;
    historyList.appendChild(li);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userText = textArea.value.trim();
  if (userText.length < 10) {
    alert("Te rugăm să scrii ceva mai detaliat 🙂");
    return;
  }

  resultText.textContent = "Se analizează... ⏳";
  resultBox.classList.remove("hidden");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: userText })
    });

    const data = await response.json();

    if (data.result) {
      resultText.textContent = data.result;
      emotionSpan.textContent = data.emotion || "necunoscută";
      adviceSpan.textContent = data.advice || "–";
      themeSpan.textContent = data.theme || "necunoscută";

      // salvare în localStorage
      const history = JSON.parse(localStorage.getItem("journalEntries") || "[]");
      history.push({
        date: new Date().toLocaleString(),
        preview: userText.substring(0, 60) + "...",
        emotion: data.emotion,
        advice: data.advice,
        theme: data.theme
      });
      localStorage.setItem("journalEntries", JSON.stringify(history));
      loadHistory();

    } else {
      resultText.textContent = "Eroare: " + (data.error || "răspuns invalid");
    }
  } catch (err) {
    resultText.textContent = "Eroare de rețea sau server. Încearcă mai târziu.";
  }
});

loadHistory();
