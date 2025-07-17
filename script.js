const form = document.getElementById("journalForm");
const textArea = document.getElementById("journalText");
const resultBox = document.getElementById("resultContainer");
const resultText = document.getElementById("resultText");

const API_URL = "https://jurnai.onrender.com/analyze";

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
        } else {
            resultText.textContent = "Eroare: " + (data.error || "răspuns invalid");
        }
    } catch (err) {
        resultText.textContent = "Eroare de rețea sau server. Încearcă mai târziu.";
    }
});
