# adapters/llm_google_genai.py
import google.generativeai as genai

def llm_completion(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")  # or whichever model you use
    resp = model.generate_content(prompt)
    return resp.text.strip()
