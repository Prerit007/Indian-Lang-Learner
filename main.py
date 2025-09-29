from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sarvamai import SarvamAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("SARVAM_AI")
client = SarvamAI(api_subscription_key=api_key)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Language dictionary: code -> human-readable name
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


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "languages": LANGUAGES,
        "original_text": "",
        "src_selected": "hi-IN",   # default source language
        "tgt_selected": "en-IN",   # default target language
        "translated_text": ""
    })


@app.post("/translate", response_class=HTMLResponse)
def translate(
    request: Request,
    text: str = Form(...),
    src_lang: str = Form(...),
    tgt_lang: str = Form(...)
):
    try:
        response = client.text.translate(
            input=text,
            source_language_code=src_lang,
            target_language_code=tgt_lang,
            model="sarvam-translate:v1",
            speaker_gender="Male"
        )
        # SarvamAI returns TranslationResponse object
        translated_text = getattr(response, "translated_text", str(response))
    except Exception as e:
        translated_text = f"Error: {str(e)}"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "languages": LANGUAGES,
        "original_text": text,
        "src_selected": src_lang,
        "tgt_selected": tgt_lang,
        "translated_text": translated_text
    })
