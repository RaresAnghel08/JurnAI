from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# Inițializează modelele
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
zero_shot = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Cuvinte cheie tematice
CANDIDATE_LABELS = ["școală", "familie", "prieteni", "oboseală", "anxietate", "fericire", "tehnologie", "pasiuni"]

# FastAPI config
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputText(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_journal(input: InputText):
    text = input.text

    # 1. Analiză de sentiment
    sentiment = sentiment_analyzer(text[:512])[0]
    emotion = sentiment["label"].lower()  # POSITIVE / NEGATIVE

    # 2. Sumarizare
    summary = summarizer(text, max_length=60, min_length=15, do_sample=False)[0]["summary_text"]

    # 3. Temă principală
    theme_result = zero_shot(text, CANDIDATE_LABELS)
    theme = theme_result["labels"][0]

    # 4. Recomandare simplă
    advice = {
        "positive": "Continuă să faci lucrurile care te fac fericit!",
        "negative": "Încearcă să iei o pauză sau să vorbești cu cineva de încredere.",
        "neutral": "Reflectă asupra zilei și vezi ce ai putea îmbunătăți."
    }.get(emotion, "Ai grijă de tine.")

    return {
        "result": f"📄 Sumar: {summary}\n\n🧠 Observație generală: Textul tău pare a fi scris cu o tonalitate {emotion}.",
        "emotion": emotion,
        "theme": theme,
        "advice": advice
    }
