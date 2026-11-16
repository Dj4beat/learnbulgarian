#!/usr/bin/env python3
"""Upload the public allowlist for bg60day.com to IONOS over SFTP.

The command is a dry run until ``--send``. Only paths in ``PUBLIC_FILES``,
plus the site-root IndexNow key file, are uploaded.

After a successful ``--send``, changed files are submitted to IndexNow.
Pass ``--skip-indexnow`` to skip that step. IndexNow problems print a warning
and do not fail the deploy.

SFTP settings come from the environment and are never printed:
    IONOS_SFTP_HOST
    IONOS_SFTP_USER
    IONOS_SFTP_REMOTE_DIR
    IONOS_SFTP_PASSWORD or IONOS_SFTP_KEY
    IONOS_SFTP_PORT (optional, default 22)

Requires paramiko for a real upload: pip install paramiko
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import sys
from pathlib import Path

from indexnow import HOST, find_key_file, sitemap_urls, submit

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / ".deploy-state.json"

# Explicit publish set. Anything not listed here stays off the server.
# The IndexNow key file is not named below; public_files() appends it.
PUBLIC_FILES = (
    "index.html",
    "sitemap.xml",
    "feedback.html",
    "media.html",
    "exam-b1.html",
    "module01.html",
    "module02.html",
    "module03.html",
    *[f"day{number:02d}.html" for number in range(1, 61)],
    "o-0bIpQlx3QUlC5A4PNB6Ryti20_6n1iPHjc5ardu2ui.woff2",
    "o-0kIpQlx3QUlC5A4PNr4C5OaxRsfNNlKbCePevHtVtX57DGjDU1QDce2VTSyFtY.woff2",
    "audio",
)


def public_files(root: Path | None = None) -> list[Path]:
    """Files the next deploy will upload, including the IndexNow key."""
    root = root or ROOT
    chosen: list[Path] = []
    for rel in PUBLIC_FILES:
        path = root / rel
        if path.is_dir():
            chosen.extend(sorted(item for item in path.rglob("*") if item.is_file()))
        elif path.is_file():
            chosen.append(path)
        else:
            print(f"warning: allowlisted path missing: {rel}")
    key = find_key_file(root)
    if key is not None and key not in chosen:
        chosen.append(key)
    elif key is None:
        print("warning: IndexNow key file is not in the publish set")
    return chosen


def main(argv: list[str] | None = None, uploader=None) -> int:
    parser = argparse.ArgumentParser(description="Deploy bg60day.com public files over SFTP.")
    parser.add_argument(
        "--send",
        action="store_true",
        help="Upload to IONOS. Without this flag the command only prints the allowlist.",
    )
    parser.add_argument(
        "--skip-indexnow",
        action="store_true",
        help="Do not submit uploaded URLs to IndexNow after a real deploy.",
    )
    args = parser.parse_args(argv)
    root = ROOT
    files = public_files(root)

    if not args.send:
        _print_plan(files, root)
        print("IndexNow: not submitted (deploy dry run).")
        return 0

    if uploader is None:
        try:
            uploader = SftpUploader.from_env()
        except ValueError as exc:
            print(f"error: {exc}")
            return 1

    try:
        changed = uploader.upload(files, root)
    except Exception as exc:
        print(f"error: deploy failed ({exc})")
        return 1

    if args.skip_indexnow:
        print("IndexNow: skipped (--skip-indexnow).")
        return 0

    _notify_indexnow(changed, root)
    return 0


def _notify_indexnow(changed: list[Path] | None, root: Path) -> None:
    """Submit changed URLs. Failures are warnings and never fail the deploy."""
    try:
        if changed is None:
            print("IndexNow: changed files unknown; submitting sitemap.xml")
            code = submit(sitemap_urls(root), send=True, root=root)
        else:
            urls = [
                f"https://{HOST}/{path.relative_to(root).as_posix()}"
                for path in changed
            ]
            code = submit(urls, send=True, root=root)
    except Exception as exc:
        print(f"warning: IndexNow submission failed ({exc}). Deploy succeeded.")
        return
    if code != 0:
        print("warning: IndexNow submission reported a problem. Deploy succeeded.")


def _print_plan(files: list[Path], root: Path) -> None:
    print(f"dry run: {len(files)} public files would be uploaded")
    audio = 0
    for path in files:
        rel = path.relative_to(root).as_posix()
        if rel.startswith("audio/"):
            audio += 1
            continue
        print(f"  {rel}")
    if audio:
        print(f"  audio/: {audio} files")


class SftpUploader:
    """Upload allowlisted files. Returns the files whose contents changed.

    A previous successful upload is recorded in ``.deploy-state.json`` (gitignored)
    so unchanged files are not sent again. Returns None only when the caller
    cannot tell what changed; this uploader always returns a list.
    """

    def __init__(self, host: str, user: str, remote_dir: str, password: str = "", key_filename: str = "", port: int = 22):
        self.host = host
        self.user = user
        self.remote_dir = remote_dir
        self.password = password
        self.key_filename = key_filename
        self.port = port

    @classmethod
    def from_env(cls) -> "SftpUploader":
        host = os.environ.get("IONOS_SFTP_HOST", "").strip()
        user = os.environ.get("IONOS_SFTP_USER", "").strip()
        remote_dir = os.environ.get("IONOS_SFTP_REMOTE_DIR", "").strip()
        password = os.environ.get("IONOS_SFTP_PASSWORD", "")
        key_filename = os.environ.get("IONOS_SFTP_KEY", "").strip()
        port_text = os.environ.get("IONOS_SFTP_PORT", "22").strip() or "22"
        missing = [
            name
            for name, value in (
                ("IONOS_SFTP_HOST", host),
                ("IONOS_SFTP_USER", user),
                ("IONOS_SFTP_REMOTE_DIR", remote_dir),
            )
            if not value
        ]
        if missing:
            raise ValueError("missing SFTP setting: " + ", ".join(missing))
        if not password and not key_filename:
            raise ValueError("set IONOS_SFTP_PASSWORD or IONOS_SFTP_KEY")
        try:
            port = int(port_text)
        except ValueError as exc:
            raise ValueError("IONOS_SFTP_PORT must be an integer") from exc
        return cls(host, user, remote_dir, password, key_filename, port)

    def upload(self, files: list[Path], root: Path) -> list[Path]:
        import paramiko

        state = _load_state()
        transport = paramiko.Transport((self.host, self.port))
        changed: list[Path] = []
        try:
            if self.key_filename:
                pkey = _load_private_key(paramiko, self.key_filename)
                transport.connect(username=self.user, pkey=pkey)
            else:
                transport.connect(username=self.user, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            if sftp is None:
                raise RuntimeError("could not open SFTP session")
            try:
                for path in files:
                    rel = path.relative_to(root).as_posix()
                    digest = _sha256(path)
                    if state.get(rel) == digest:
                        continue
                    remote = posixpath.join(self.remote_dir.rstrip("/"), rel)
                    _mkdirs(sftp, posixpath.dirname(remote))
                    sftp.put(str(path), remote)
                    state[rel] = digest
                    changed.append(path)
            finally:
                sftp.close()
        finally:
            transport.close()
        _save_state(state)
        print(f"uploaded {len(changed)} changed file(s); {len(files) - len(changed)} unchanged")
        return changed


def _load_private_key(paramiko, key_filename: str):
    errors: list[str] = []
    for loader in (paramiko.Ed25519Key, paramiko.ECDSAKey, paramiko.RSAKey):
        try:
            return loader.from_private_key_file(key_filename)
        except Exception as exc:
            errors.append(f"{loader.__name__}: {exc}")
    raise RuntimeError("could not read IONOS_SFTP_KEY (" + "; ".join(errors) + ")")


def _mkdirs(sftp, remote_dir: str) -> None:
    if not remote_dir or remote_dir == "/":
        return
    parts = [part for part in remote_dir.split("/") if part]
    path = "/" if remote_dir.startswith("/") else ""
    for part in parts:
        path = posixpath.join(path, part) if path else part
        try:
            sftp.stat(path)
        except OSError:
            sftp.mkdir(path)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_state() -> dict[str, str]:
    if not STATE_PATH.is_file():
        return {}
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(key): str(value) for key, value in data.items()}


def _save_state(state: dict[str, str]) -> None:
    temporary = STATE_PATH.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(STATE_PATH)


if __name__ == "__main__":
    sys.exit(main())
