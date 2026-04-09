import os
import sys
import time
import re
from bs4 import BeautifulSoup
from google.cloud import texttospeech

# --- CONFIGURATION ---
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gen-lang-client-0451405897-25b8e7e0a115.json"
BASE_AUDIO_FOLDER = "audio"

client = texttospeech.TextToSpeechClient()

FORCE_REGENERATE = "--force" in sys.argv

def generate_pro_voice(text, day_folder, filename):
    # Ensure the subfolder for the specific day exists
    os.makedirs(day_folder, exist_ok=True)
    filepath = os.path.join(day_folder, f"{filename}.mp3")
    
    # Check if file exists to save quota
    if os.path.exists(filepath) and not FORCE_REGENERATE:
        return True

    # Pacing logic: Letter (65% speed) -> 1.8s gap -> Word (75% speed)
    if "." in text:
        parts = text.split(".", 1)
        main_part = parts[0].strip()
        example_part = parts[1].strip()
    else:
        main_part = text
        example_part = ""

    ssml = f"""
    <speak>
        <prosody rate="65%">{main_part}</prosody>
        <break time="1800ms"/>
        <prosody rate="75%">{example_part}</prosody>
    </speak>
    """

    input_text = texttospeech.SynthesisInput(ssml=ssml)
    voice = texttospeech.VoiceSelectionParams(language_code="bg-BG", name="bg-BG-Standard-A")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    try:
        response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
        with open(filepath, "wb") as out:
            out.write(response.audio_content)
        print(f"   Success: {filename}.mp3")
        return True
    except Exception as e:
        print(f"   Error: {e}")
        return False

# --- THE CRAWLER LOGIC ---

def get_html_files():
    # Optional explicit targets: python generate_pro_audio.py --force day35.html exam-b1.html
    cli_targets = [arg for arg in sys.argv[1:] if arg != "--force"]
    if cli_targets:
        return [f for f in cli_targets if os.path.isfile(f) and f.endswith('.html')]

    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f.startswith('day')]

    # Include standalone exam pages that also use the same audio player pattern.
    for extra in ["exam-b1.html"]:
        if os.path.isfile(extra):
            html_files.append(extra)

    return sorted(set(html_files))

html_files = get_html_files()

print(f"Found {len(html_files)} HTML files. Starting generation...")

for html_file in html_files:
    # Get the day name (e.g., 'day01') to use as a folder name
    day_name = os.path.splitext(html_file)[0]
    day_folder = os.path.join(BASE_AUDIO_FOLDER, day_name)
    
    print(f"\nProcessing {html_file}...")
    
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        audio_items = soup.find_all(attrs={"data-text": True})
        
        if not audio_items:
            print(f"   No audio tags found in {html_file}")
            continue

        for item in audio_items:
            original_text = item['data-text']
            safe_filename = re.sub(r'[^\w\s]', '', original_text)
            safe_filename = re.sub(r'\s+', '_', safe_filename).lower()[:30]
            
            generate_pro_voice(original_text, day_folder, safe_filename)
            time.sleep(0.1) # Small delay to be kind to the API

print("\n✅ All days processed! Check your /audio/ subfolders.")
