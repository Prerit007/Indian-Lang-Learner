from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sarvamai import SarvamAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os, base64

load_dotenv()
api_key = os.getenv("SARVAM_AI")
client = SarvamAI(api_subscription_key=api_key)

app = FastAPI()

LANGUAGES = {
    "bn-IN": "Bengali",
    "en-IN": "English",
    "gu-IN": "Gujarati",
    "hi-IN": "Hindi",
    "kn-IN": "Kannada",
    "ml-IN": "Malayalam",
    "mr-IN": "Marathi",
    "od-IN": "Odia",
    "pa-IN": "Punjabi",
    "ta-IN": "Tamil",
    "te-IN": "Telugu",
    "as-IN": "Assamese",
    "brx-IN": "Bodo",
    "doi-IN": "Dogri",
    "kok-IN": "Konkani",
    "ks-IN": "Kashmiri",
    "mai-IN": "Maithili",
    "mni-IN": "Manipuri (Meiteilon)",
    "ne-IN": "Nepali",
    "sa-IN": "Sanskrit",
    "sat-IN": "Santali",
    "sd-IN": "Sindhi",
    "ur-IN": "Urdu"
}


pdf_path = r"documents\Mahabharata (Unabridged in English).pdf"
reader = PdfReader(pdf_path)
text = ""
audio_files = []

for page in reader.pages:
    text += page.extract_text() + "\n"

def chunk_text(text, max_chars=1000):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks

chunks = chunk_text(text, max_chars=1000)

for i, chunk in enumerate(chunks):
    tts = client.text_to_speech.convert(
        text=chunk,
        target_language_code="hi-IN",  # change to your target language
        speaker="anushka",
        pitch=0,
        pace=0.9,
        loudness=1,
        speech_sample_rate=22050,
        enable_preprocessing=True,
        model="bulbul:v2"
    )

    audio_base64 = "".join(tts.audios)
    audio_bytes = base64.b64decode(audio_base64)
    
    audio_files.append(audio_bytes)

