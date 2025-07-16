from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import random

app = FastAPI()

# CORS pt. frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sau ["https://jurnai.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JournalRequest(BaseModel):
    text: str

HF_TOKEN = os.getenv("HF_TOKEN")  # HuggingFace access token
HF_MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"

@app.post("/analyze")
async def analyze_journal(req: JournalRequest):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    data = {
        "inputs": req.text
    }
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=data
        )
        result = response.json()

        stars = result[0][0]['label']  # ex: "4 stars"
        rating = int(stars[0])

        sentiment_map = {
            1: "foarte negativă",
            2: "negativă",
            3: "neutră",
            4: "pozitivă",
            5: "foarte pozitivă"
        }

        tip = random.choice([
            "Amintește-ți să respiri adânc și să apreciezi progresul făcut.",
            "Mâine e o nouă oportunitate — încearcă din nou cu încredere.",
            "Fii blând cu tine. Fiecare pas contează."
        ])

        quote = random.choice([
            "„Chiar și cea mai lungă călătorie începe cu un singur pas.”",
            "„Astăzi e greu, mâine va fi mai bine.”",
            "„Nu renunța. Lucrurile bune vin cu răbdare.”"
        ])

        return {
            "result": f"""
📌 **Rezumat:** Ai avut o zi evaluată cu {stars}, deci starea generală a fost {sentiment_map[rating]}.

💬 **Emoții predominante:** {sentiment_map[rating]}

💡 **Sfat pentru mâine:** {tip}

✨ **Citat motivațional:** {quote}
"""
        }

    except Exception as e:
        return {"error": str(e)}
