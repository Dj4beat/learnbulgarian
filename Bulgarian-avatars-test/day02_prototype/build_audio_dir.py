"""Build the per-segment audio delivery directory.

Copies the right MP3 for each of the 91 segment IDs to
`Bulgarian-avatars-test/audio/elena-day02/<segment_id>.mp3`. Slow
segments get their `_slow.mp3` variant.

Each file is then probed to verify it's decodable and has a sensible
duration. Audit log is printed.
"""
from __future__ import annotations
import re
import shutil
import subprocess
import sys
from pathlib import Path
import imageio_ffmpeg

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "elena" / "_work_master"
DEST = ROOT / "audio" / "elena-day02"
DEST.mkdir(parents=True, exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

SLOW_PREFIXES = ("cold_open", "recap_intro", "intro_", "spotlight_", "outro")


def is_slow(seg_id: str) -> bool:
    return any(seg_id.startswith(p) for p in SLOW_PREFIXES)


# Canonical list of all 91 segment IDs (from build_master_audio.py SCRIPT).
SEGMENT_IDS = [
    "cold_open", "recap_intro",
    *[f"recap_{i}" for i in range(1, 12)],
    "intro_s2", "intro_s3", "intro_s4", "intro_s5", "intro_s6",
    "intro_s7", "intro_s8", "intro_roleplays",
    # Phrase clips
    "p_zdravey", "p_zdraveite", "p_dobro_utro", "p_dobar_den", "p_dobar_vecher",
    "p_dovizhdane", "p_chao", "p_do_skoro", "p_leka_nosht", "p_priyaten_den",
    "p_izvini", "p_izvinete", "p_chakay", "p_chakayte", "p_govori", "p_govorete",
    "p_zapovyaday", "p_zapovyadayte",
    "p_molya", "p_blagodarya", "p_mnogo_blag", "p_nyama_nishto",
    "p_nazdrave", "p_mersi", "p_dobre_doshli", "p_s_udovolstvie", "p_dostatachno",
    "p_ne_razbiram", "p_ne_govoria", "p_govorite_en", "p_po_bavno",
    "p_kak_se_kazva", "p_razbrah", "p_ucha_bg", "p_povtorete", "p_mozhem_na_ti",
    "p_utro", "p_banichka", "p_zdrave", "p_dobro", "p_dobar", "p_dobra_vecher",
    # Roleplay 1
    "rp1_owner_1", "rp1_you_1", "rp1_owner_2", "rp1_you_2",
    "rp1_owner_3", "rp1_you_3", "rp1_owner_4",
    # Roleplay 2
    "rp2_ivan", "rp2_baba_1", "rp2_you_1", "rp2_baba_2",
    "rp2_you_2", "rp2_baba_3", "rp2_you_3",
    # Roleplay 3
    "rp3_friend_1", "rp3_you_1", "rp3_friend_2", "rp3_you_2",
    "rp3_friend_3", "rp3_you_3", "rp3_friend_4",
    # Spotlights + outro
    "spotlight_te", "spotlight_mersi", "spotlight_zapovyadayte",
    "spotlight_vie", "spotlight_dobra_vs_dobar", "spotlight_ucha_bg",
    "outro",
]


def probe_duration_s(path: Path) -> float | None:
    result = subprocess.run(
        [FFMPEG, "-i", str(path)],
        capture_output=True, text=True, check=False, timeout=15,
    )
    blob = (result.stdout or "") + (result.stderr or "")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", blob)
    if not m:
        return None
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def main():
    print(f"Expecting {len(SEGMENT_IDS)} segments")
    assert len(SEGMENT_IDS) == 91, f"got {len(SEGMENT_IDS)} not 91"

    audit = []
    missing = []
    for sid in SEGMENT_IDS:
        src_name = f"{sid}_slow.mp3" if is_slow(sid) else f"{sid}.mp3"
        src_path = SRC / src_name
        if not src_path.exists():
            missing.append(src_name)
            audit.append({"id": sid, "status": "MISSING", "src": src_name})
            continue
        dest_path = DEST / f"{sid}.mp3"
        shutil.copy2(src_path, dest_path)
        dur = probe_duration_s(dest_path)
        audit.append({
            "id": sid,
            "status": "OK" if dur and dur > 0.3 else "SUSPECT",
            "src": src_name,
            "duration_s": round(dur, 3) if dur else None,
            "size_kb": dest_path.stat().st_size // 1024,
        })

    if missing:
        print(f"\n!! MISSING ({len(missing)}):")
        for m in missing:
            print(f"   {m}")
        sys.exit(1)

    suspect = [a for a in audit if a["status"] != "OK"]
    print(f"\nAudit: {len(audit) - len(suspect)} OK, {len(suspect)} SUSPECT")

    # Spot-check 5 of each kind: short, medium, long
    print("\nSpot check (durations):")
    by_dur = sorted(audit, key=lambda a: a.get("duration_s") or 0)
    print("  Shortest 3:")
    for a in by_dur[:3]:
        print(f"    {a['id']:30}  {a['duration_s']}s")
    print("  Longest 3:")
    for a in by_dur[-3:]:
        print(f"    {a['id']:30}  {a['duration_s']}s")

    total_kb = sum(a.get("size_kb", 0) for a in audit)
    total_dur = sum(a.get("duration_s", 0) for a in audit)
    print(f"\nTotal: {len(audit)} files, {total_kb} KB, {total_dur:.1f}s of audio")
    print(f"Written to: {DEST}")


if __name__ == "__main__":
    main()
