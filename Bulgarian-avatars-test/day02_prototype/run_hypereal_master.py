"""Render Elena's Day 2 master MP4 — workhorse pose, 6:48 of audio."""
import os, sys, time
from pathlib import Path
import requests
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
ENV = Path(r"C:/Users/Dj4be/Desktop/Thesportsguru/.env")
MODEL = "ai-avatar-i2v"
BRANCH = "claude/blissful-bouman-36288c"
RAW = f"https://raw.githubusercontent.com/Dj4beat/learnbulgarian/{BRANCH}"
IMG = f"{RAW}/Bulgarian-avatars-test/assets/elena/01-workhorse.jpg"
AUD = f"{RAW}/Bulgarian-avatars-test/assets/elena/day02-master.mp3"
OUT = ROOT / "clips" / "day02" / "elena-day02-master.mp4"

def key():
    if os.getenv("HYPEREAL_API_KEY"): return os.environ["HYPEREAL_API_KEY"]
    for ln in ENV.read_text(encoding="utf-8").splitlines():
        if ln.startswith("HYPEREAL_API_KEY="):
            return ln.split("=",1)[1].strip().strip('"').strip("'")
def H(k): return {"Content-Type":"application/json","Authorization":f"Bearer {k}"}

k = key()
print(f"POST /videos/generate (6:48 audio, workhorse pose)")
r = requests.post("https://api.hypereal.cloud/v1/videos/generate",
    json={"model": MODEL, "input": {"image": IMG, "audio": AUD}},
    headers=H(k), timeout=180)
print(f"  http_status: {r.status_code}")
if r.status_code >= 400:
    sys.exit(f"REJECTED: {r.text[:500]}")
d = r.json()
jid = d.get("jobId") or d.get("id")
print(f"  jobId: {jid}  credits: {d.get('creditsUsed','?')}")
deadline = time.time() + 1800
last = None
while time.time() < deadline:
    rr = requests.get(f"https://api.hypereal.cloud/v1/jobs/{jid}",
        params={"model": MODEL, "type": "video"}, headers=H(k), timeout=30)
    if rr.status_code >= 400:
        sys.exit(f"poll: {rr.text}")
    data = rr.json()
    s = data.get("status")
    if s != last:
        print(f"  status: {s}"); last = s
    if s == "completed":
        url = data.get("outputUrl") or data.get("url")
        OUT.parent.mkdir(parents=True, exist_ok=True)
        print(f"  downloading {url}")
        with requests.get(url, stream=True, timeout=900) as resp:
            resp.raise_for_status()
            with OUT.open("wb") as fh:
                for c in resp.iter_content(64*1024):
                    if c: fh.write(c)
        print(f"  saved {OUT} ({OUT.stat().st_size//1024} KB)")
        sys.exit(0)
    if s in ("failed","error"):
        sys.exit(f"FAILED: {data}")
    time.sleep(8)
sys.exit("client timed out")
