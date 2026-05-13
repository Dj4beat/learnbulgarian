"""Submit the 57s duration-probe Hypereal i2v job.

If this succeeds, we know Hypereal handles ~60s and the
"one render per day" strategy is feasible. If it fails, the error
message tells us where the cap is (and credits auto-refund).
"""
from __future__ import annotations
import os, sys, time
from pathlib import Path
import requests

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = Path(r"C:/Users/Dj4be/Desktop/Thesportsguru/.env")
API_BASE = "https://api.hypereal.cloud"
MODEL = "ai-avatar-i2v"
BRANCH = "claude/blissful-bouman-36288c"
RAW_BASE = f"https://raw.githubusercontent.com/Dj4beat/learnbulgarian/{BRANCH}"
IMAGE_URL = f"{RAW_BASE}/Bulgarian-avatars-test/assets/elena-square.jpg"
AUDIO_URL = f"{RAW_BASE}/Bulgarian-avatars-test/assets/day02-long.mp3"
OUT_PATH = ROOT / "clips" / "day02" / "day02-long.mp4"

def key():
    if os.getenv("HYPEREAL_API_KEY"): return os.environ["HYPEREAL_API_KEY"]
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("HYPEREAL_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("no key")

def h(k): return {"Content-Type": "application/json", "Authorization": f"Bearer {k}"}

def main():
    k = key()
    print(f"POST /videos/generate  (audio: 57.38s)")
    r = requests.post(f"{API_BASE}/v1/videos/generate",
        json={"model": MODEL, "input": {"image": IMAGE_URL, "audio": AUDIO_URL}},
        headers=h(k), timeout=180)
    if r.status_code >= 400:
        sys.exit(f"submit failed ({r.status_code}): {r.text}")
    d = r.json()
    jid = d.get("jobId") or d.get("id")
    print(f"  jobId: {jid}  (credits: {d.get('creditsUsed', '?')})")
    deadline = time.time() + 900  # longer ceiling for longer audio
    last = None
    while time.time() < deadline:
        rr = requests.get(f"{API_BASE}/v1/jobs/{jid}",
            params={"model": MODEL, "type": "video"}, headers=h(k), timeout=30)
        if rr.status_code >= 400:
            sys.exit(f"poll fail: {rr.text}")
        data = rr.json()
        s = data.get("status")
        if s != last:
            print(f"  status: {s}")
            last = s
        if s == "completed":
            url = data.get("outputUrl") or data.get("url")
            OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
            print(f"  downloading {url}")
            with requests.get(url, stream=True, timeout=300) as resp:
                resp.raise_for_status()
                with OUT_PATH.open("wb") as fh:
                    for c in resp.iter_content(64*1024):
                        if c: fh.write(c)
            print(f"  saved {OUT_PATH} ({OUT_PATH.stat().st_size//1024} KB)")
            return
        if s in ("failed", "error"):
            sys.exit(f"FAILED — useful info for the cap question: {data}")
        time.sleep(5)
    sys.exit("client timed out")

if __name__ == "__main__":
    main()
