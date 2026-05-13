"""Submit one Hypereal i2v job for the Day 2 avatar test.

Uses the same auth + endpoints as the Sports Guru pipeline. Inputs are
served from raw.githubusercontent.com on the current branch (already
committed + pushed). Output mp4 lands in clips/day02/day02-greetings.mp4.

Cost: 23 credits per generation. Credits auto-refund on failure.
"""
from __future__ import annotations
import os
import sys
import time
from pathlib import Path

import requests

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
ENV_PATH = Path(r"C:/Users/Dj4be/Desktop/Thesportsguru/.env")

API_BASE = "https://api.hypereal.cloud"
GENERATE_ENDPOINT = f"{API_BASE}/v1/videos/generate"
JOB_ENDPOINT = f"{API_BASE}/v1/jobs"
MODEL = "ai-avatar-i2v"

# These must already be committed and pushed.
BRANCH = "claude/blissful-bouman-36288c"
RAW_BASE = f"https://raw.githubusercontent.com/Dj4beat/learnbulgarian/{BRANCH}"
IMAGE_URL = f"{RAW_BASE}/Bulgarian-avatars-test/assets/elena-square.jpg"
AUDIO_URL = f"{RAW_BASE}/Bulgarian-avatars-test/assets/day02-greetings.mp3"

OUT_PATH = ROOT / "clips" / "day02" / "day02-greetings.mp4"


def load_key() -> str:
    if os.getenv("HYPEREAL_API_KEY"):
        return os.environ["HYPEREAL_API_KEY"]
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("HYPEREAL_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("HYPEREAL_API_KEY not found")


def headers(api_key: str) -> dict[str, str]:
    return {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}


def submit(api_key: str) -> str:
    payload = {"model": MODEL, "input": {"image": IMAGE_URL, "audio": AUDIO_URL}}
    print(f"POST {GENERATE_ENDPOINT}")
    print(f"  image: {IMAGE_URL}")
    print(f"  audio: {AUDIO_URL}")
    resp = requests.post(GENERATE_ENDPOINT, json=payload, headers=headers(api_key), timeout=180)
    if resp.status_code >= 400:
        sys.exit(f"submit failed ({resp.status_code}): {resp.text[:500]}")
    data = resp.json()
    job_id = data.get("jobId") or data.get("job_id") or data.get("id")
    if not job_id:
        sys.exit(f"no jobId in response: {data}")
    print(f"  jobId: {job_id}  (credits used: {data.get('creditsUsed', '?')})")
    return job_id


def poll(api_key: str, job_id: str, max_wait: int = 600) -> dict:
    url = f"{JOB_ENDPOINT}/{job_id}"
    params = {"model": MODEL, "type": "video"}
    deadline = time.time() + max_wait
    last = None
    while time.time() < deadline:
        resp = requests.get(url, params=params, headers=headers(api_key), timeout=30)
        if resp.status_code >= 400:
            sys.exit(f"poll failed ({resp.status_code}): {resp.text[:300]}")
        data = resp.json()
        status = data.get("status")
        if status != last:
            print(f"  status: {status}")
            last = status
        if status == "completed":
            return data
        if status in ("failed", "error"):
            sys.exit(f"job failed: {data}")
        time.sleep(5)
    sys.exit(f"timed out after {max_wait}s")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"downloading {url} -> {dest.name}")
    resp = requests.get(url, stream=True, timeout=300)
    resp.raise_for_status()
    with dest.open("wb") as fh:
        for chunk in resp.iter_content(chunk_size=64 * 1024):
            if chunk:
                fh.write(chunk)
    print(f"saved {dest} ({dest.stat().st_size // 1024} KB)")


def main() -> None:
    api_key = load_key()
    print("Submitting Hypereal i2v job (23 credits)...")
    job_id = submit(api_key)
    print("Polling for completion...")
    result = poll(api_key, job_id)
    output_url = result.get("outputUrl") or result.get("output_url") or result.get("url")
    if not output_url:
        sys.exit(f"no outputUrl: {result}")
    download(output_url, OUT_PATH)
    print(f"\nDone. Watch: {OUT_PATH}")


if __name__ == "__main__":
    main()
