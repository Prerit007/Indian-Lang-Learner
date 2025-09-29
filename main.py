from sarvamai import SarvamAI
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("SARVAM_AI")

client = SarvamAI(api_subscription_key=api_key)

app = FastAPI()

class TranslationRequest(BaseModel):
    text: str
    src_lang: str
    tgt_lang: str


@app.post("/translate")
def translate(req: TranslationRequest):
    try:
        response = client.text.translate(
    input=req.text,
    source_language_code=req.src_lang,
    target_language_code=req.tgt_lang,
    model="sarvam-translate:v1"
)
        translated_text = getattr(response, "translated_text", None) or getattr(response, "translation", None)

        return {"translation": translated_text}

    except Exception as e:
        return {"error": str(e)}



languages = {"Bengali": "bn-IN",
"English": "en-IN",
"Gujarati": "gu-IN",
"Hindi": "hi-IN",
"Kannada": "kn-IN",
"Malayalam": "ml-IN",
"Marathi": "mr-IN",
"Odia": "od-IN",
"Punjabi": "pa-IN",
"Tamil": "ta-IN",
"Telugu": "te-IN",
"Assamese": "as-IN",
"Bodo": "brx-IN",
"Dogri": "doi-IN",
"Konkani": "kok-IN",
"Kashmiri": "ks-IN",
"Maithili": "mai-IN",
"Manipuri (Meiteilon)": "mni-IN",
"Nepali": "ne-IN",
"Sanskrit": "sa-IN",
"Santali": "sat-IN",
"Sindhi": "sd-IN",
"Urdu": "ur-IN"}

