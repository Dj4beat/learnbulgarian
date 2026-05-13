"""Static verification of day02-prototype-v3.html.

Checks (all must pass):
  1. Every <button class="...play-audio...">'s data-text maps to a data-seg
  2. Every data-seg value has a corresponding .mp3 file on disk
  3. Every image src referenced in the file resolves to an existing file
  4. The MP4 src resolves to an existing file
  5. The old audio.js <script> is gone (no `var currentAudio` remaining)
  6. No 'Bulgarian-avatars-test/' prefix in any URL (the page lives INSIDE that folder)
  7. The page has exactly 1 cold-open block, 1 recap card, 1 outro card, 1 mini-avatar
  8. Inlined SOUNDBOARD references segment IDs that all have .mp3 files
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]  # Bulgarian-avatars-test/
V3 = ROOT / "day02-prototype-v3.html"
AUDIO_DIR = ROOT / "audio" / "elena-day02"

errors: list[str] = []
warnings: list[str] = []

def err(msg: str): errors.append(msg)
def warn(msg: str): warnings.append(msg)


def main():
    if not V3.exists():
        err(f"v3 HTML missing: {V3}")
        finish()
    html = V3.read_text(encoding="utf-8")
    print(f"Loaded {V3.name} ({len(html)} chars)")

    # --- Check 1+2: every play-audio data-text has data-seg and the seg file exists ---
    btn_pat = re.compile(
        r'<button[^>]*class="[^"]*play-audio[^"]*"[^>]*>',
        re.DOTALL
    )
    btns = btn_pat.findall(html)
    print(f"\n[1+2] Found {len(btns)} .play-audio buttons")
    missing_seg = []
    missing_file = []
    for b in btns:
        dt_m = re.search(r'data-text="([^"]+)"', b)
        ds_m = re.search(r'data-seg="([^"]+)"', b)
        if not dt_m:
            warn(f"    button without data-text: {b[:80]}")
            continue
        if not ds_m:
            missing_seg.append(dt_m.group(1))
            continue
        seg = ds_m.group(1)
        if not (AUDIO_DIR / f"{seg}.mp3").exists():
            missing_file.append((dt_m.group(1), seg))
    if missing_seg:
        err(f"[1] {len(missing_seg)} buttons lack data-seg:")
        for x in missing_seg[:5]: err(f"      {x!r}")
        if len(missing_seg) > 5: err(f"      ... and {len(missing_seg)-5} more")
    if missing_file:
        err(f"[2] {len(missing_file)} data-seg values point to MISSING files:")
        for dt, seg in missing_file: err(f"      {seg}.mp3  (button: {dt!r})")
    if not missing_seg and not missing_file:
        print("    OK — all buttons wired and files present")

    # --- Check 3: every image src resolves ---
    img_pat = re.compile(r'<img[^>]+src="([^"]+)"')
    img_srcs = set(img_pat.findall(html))
    print(f"\n[3] Found {len(img_srcs)} unique <img src> values")
    missing_imgs = []
    for src in img_srcs:
        if src.startswith(("http://", "https://", "data:")): continue
        # Resolve relative to v3 HTML location
        candidate = (V3.parent / src).resolve()
        if not candidate.exists():
            missing_imgs.append(src)
    if missing_imgs:
        err(f"[3] {len(missing_imgs)} missing images:")
        for x in missing_imgs: err(f"      {x}")
    else:
        print("    OK — all images resolve")

    # --- Check 4: the cold-open MP4 resolves ---
    mp4_pat = re.compile(r"COLD_OPEN_VIDEO\s*=\s*'([^']+)'")
    mp4 = mp4_pat.search(html)
    if mp4:
        mp4_src = mp4.group(1)
        candidate = (V3.parent / mp4_src).resolve()
        print(f"\n[4] Cold-open MP4: {mp4_src}")
        if not candidate.exists():
            err(f"[4] missing: {mp4_src} -> {candidate}")
        else:
            print(f"    OK — exists ({candidate.stat().st_size//1024} KB)")
    else:
        warn("[4] Could not find COLD_OPEN_VIDEO in v3 (unexpected)")

    # --- Check 5: old audio.js gone ---
    print("\n[5] Old audio.js removal check")
    if "var currentAudio = null" in html:
        err("[5] Old audio.js STILL PRESENT — would cause double-audio")
    else:
        print("    OK — old audio.js absent")

    # --- Check 6: no Bulgarian-avatars-test/ prefix in URLs ---
    print("\n[6] Path-prefix check")
    bad_paths = re.findall(r'(?:src|href)="(Bulgarian-avatars-test/[^"]+)"', html)
    if bad_paths:
        err(f"[6] {len(bad_paths)} paths still use Bulgarian-avatars-test/ prefix:")
        for x in bad_paths[:5]: err(f"      {x}")
    else:
        print("    OK — all paths relative to v3's location")

    # --- Check 7: structural blocks present (exactly once) ---
    print("\n[7] Structural blocks")
    expected = [
        ("cold-open", r'class="elena-cold-open"', 1),
        ("recap card", r'class="elena-recap-card"', 1),
        ("outro card", r'class="elena-outro"', 1),
        ("mini-avatar", r'class="elena-mini"', 1),
        ("soundboard", r'class="elena-soundboard"', 1),
    ]
    for name, pat, expected_count in expected:
        c = len(re.findall(pat, html))
        status = "OK" if c == expected_count else f"FAIL (got {c}, expected {expected_count})"
        if c != expected_count:
            err(f"[7] {name}: {status}")
        else:
            print(f"    {name}: {status}")

    # --- Check 8: every SOUNDBOARD tile id has an audio file ---
    sb_pat = re.compile(r"\{id:'([^']+)',", re.DOTALL)
    sb_ids = sb_pat.findall(html)
    print(f"\n[8] Soundboard tile IDs: {len(sb_ids)} found")
    missing_sb = [s for s in sb_ids if not (AUDIO_DIR / f"{s}.mp3").exists()]
    if missing_sb:
        err(f"[8] {len(missing_sb)} soundboard IDs lack audio files: {missing_sb}")
    else:
        print("    OK — all soundboard tiles have audio files")

    finish()


def finish():
    print("\n" + "=" * 60)
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings: print(f"  {w}")
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors: print(f"  {e}")
        print("\n  ✗ VERIFICATION FAILED")
        sys.exit(1)
    print("\n  ✓ VERIFICATION PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
