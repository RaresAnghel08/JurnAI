# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS – permite accesul frontendului de pe alt domeniu (ex: Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sau specific: ["https://jurnai.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JournalRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_journal(req: JournalRequest):
    prompt = f"""
Ești un asistent empatic care analizează un jurnal zilnic scris de un elev. Pentru textul de mai jos, generează:
1. Rezumatul zilei (max 2 fraze)
2. Emoțiile predominante exprimate
3. Un sfat empatic pentru ziua de mâine
4. Un citat motivațional

Textul: \"\"\"{req.text}\"\"\"

Scrie fiecare punct clar, cu titlu:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message["content"]
        return {"result": content}
    except Exception as e:
        return {"error": str(e)}
