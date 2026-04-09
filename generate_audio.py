import os
import time
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# --- CONFIGURATION ---
# Set GOOGLE_API_KEY as an environment variable — never hard-code keys here
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
HTML_FILE = "day01.html" 
OUTPUT_FOLDER = "audio"

# Use the dedicated TTS model variant
MODEL_ID = "gemini-2.5-flash-tts" 

client = genai.Client(api_key=API_KEY)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def generate_voiceover(text, filename):
    filepath = os.path.join(OUTPUT_FOLDER, f"{filename}.wav")
    
    # Updated Prompt for the TTS engine
    prompt = f"Say clearly in Bulgarian: {text}. Pause for one second between the letter and the word."

    print(f"Generating audio for: {text}...")
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                # You MUST specify a voice for the TTS model
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Aoede' # 'Aoede' is clear and instructional
                        )
                    )
                )
            )
        )

        if response.candidates and response.candidates[0].content.parts:
            audio_data = response.candidates[0].content.parts[0].inline_data.data
            with open(filepath, "wb") as f:
                f.write(audio_data)
            return True
            
    except Exception as e:
        print(f"Error generating {text}: {e}")
        return False

# --- MAIN EXECUTION ---
with open(HTML_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

audio_items = soup.find_all(attrs={"data-text": True})

for item in audio_items:
    original_text = item['data-text']
    safe_filename = original_text.replace(".", "").replace(",", "").replace(" ", "_").lower()
    
    if not os.path.exists(os.path.join(OUTPUT_FOLDER, f"{safe_filename}.wav")):
        success = generate_voiceover(original_text, safe_filename)
        if success:
            time.sleep(0.5) # Flash TTS is very fast

print("\n✅ All audio files generated!")