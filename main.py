from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sarvamai import SarvamAI
from dotenv import load_dotenv
import os, base64

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
    return templates.TemplateResponse("index.html", {"request": request, "languages": LANGUAGES})

@app.post("/translate", response_class=HTMLResponse)
def translate(request: Request, text: str = Form(...), src_lang: str = Form(...), tgt_lang: str = Form(...)):
    try:
        # Step 1: Translation
        translation = client.text.translate(
            input=text,
            source_language_code=src_lang,
            target_language_code=tgt_lang,
            model="sarvam-translate:v1"
        )
        translated_text = translation.translated_text

        # Step 2: TTS
        tts = client.text_to_speech.convert(
            text=translated_text,
            target_language_code=tgt_lang,
            speaker="anushka",
            pitch=0,
            pace=0.9,
            loudness=1,
            speech_sample_rate=22050,
            enable_preprocessing=True,
            model="bulbul:v2"
        )

        audio_base64 = "".join(tts.audios)  # if it's a list
        audio_data_uri = f"data:audio/wav;base64,{audio_base64}"


        with open("out.wav", "wb") as f:
            f.write(base64.b64decode(audio_base64))

    except Exception as e:
        translated_text = f"Error: {str(e)}"
        audio_data_uri = None

    return templates.TemplateResponse("index.html", {
        "request": request,
        "languages": LANGUAGES,
        "original_text": text,
        "tgt_selected": tgt_lang,
        "translated_text": translated_text,
        "audio_data": audio_data_uri
    })