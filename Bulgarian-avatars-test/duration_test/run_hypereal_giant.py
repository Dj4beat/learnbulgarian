"""Submit ~562s audio. Either lands a 10-min MP4 or hits the cap.

If it succeeds: shared mega-MP4s reused across many pages become viable.
If it fails: the error pins down the cap between 169s and 562s.
Credits auto-refund on rejection.
"""
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
IMG = f"{RAW}/Bulgarian-avatars-test/assets/elena-square.jpg"
AUD = f"{RAW}/Bulgarian-avatars-test/assets/day02-giant.mp3"
OUT = ROOT / "clips" / "day02" / "day02-giant.mp4"
def k():
    if os.getenv("HYPEREAL_API_KEY"): return os.environ["HYPEREAL_API_KEY"]
    for ln in ENV.read_text(encoding="utf-8").splitlines():
        if ln.startswith("HYPEREAL_API_KEY="):
            return ln.split("=",1)[1].strip().strip('"').strip("'")
def H(x): return {"Content-Type":"application/json","Authorization":f"Bearer {x}"}
key = k()
print("POST /videos/generate  (audio: 562.16s / 9:22)")
r = requests.post("https://api.hypereal.cloud/v1/videos/generate",
    json={"model": MODEL, "input": {"image": IMG, "audio": AUD}},
    headers=H(key), timeout=180)
print(f"  http_status: {r.status_code}")
if r.status_code >= 400:
    print(f"  REJECTED — body: {r.text[:800]}")
    sys.exit(0)
d = r.json()
jid = d.get("jobId") or d.get("id")
print(f"  jobId: {jid}  credits: {d.get('creditsUsed','?')}")
deadline = time.time() + 3000
last = None
while time.time() < deadline:
    rr = requests.get(f"https://api.hypereal.cloud/v1/jobs/{jid}",
        params={"model": MODEL, "type": "video"}, headers=H(key), timeout=30)
    if rr.status_code >= 400:
        print(f"poll err: {rr.text}")
        sys.exit(0)
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
        print(f"FAILED — body: {data}")
        sys.exit(0)
    time.sleep(10)
print("client timed out after 50min")
