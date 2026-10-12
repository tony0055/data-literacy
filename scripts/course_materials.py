#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Import or verify an immutable, course-only Git snapshot.

Run: python3 scripts/course_materials.py import /path/to/source-checkout
     python3 scripts/course_materials.py check [source-checkout]
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Final
import zipfile

ROOT: Final = Path(__file__).resolve().parents[1]
REVISION: Final = "f25491512e69c264097fb1d10b650f0ceb135f7c"
SNAPSHOT: Final = Path("school/school_materials/pnu-lectures-2026") / REVISION[:12]
PLAN: Final = "plans/데이터리터러시-5-16주-계획.md"
REPOSITORY: Final = "https://github.com/shain1912/pnu-lectures-2026"


def selected(path: str) -> bool:
    """Select course sources and the shared PDF build dependency only."""
    return (
        path.startswith(("dataliteracy/", "배포/데이터리터러시/"))
        or path in (PLAN, "tools/print_pdf.py")
    )


def source_paths(source: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(source), "ls-tree", "-rz", "--name-only", REVISION],
        check=True, capture_output=True,
    )
    return sorted(path for path in result.stdout.decode().split("\0") if selected(path))


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def import_snapshot(source: Path, root: Path = ROOT) -> int:
    """Write original Git blobs exclusively; never overwrite existing material."""
    destination = root / SNAPSHOT
    paths = source_paths(source)
    entries = []
    for path in paths:
        data = subprocess.run(
            ["git", "-C", str(source), "show", f"{REVISION}:{path}"],
            check=True, capture_output=True,
        ).stdout
        target = destination / path
        if target.exists():
            if target.read_bytes() != data:
                raise FileExistsError(target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)
        entries.append({
            "path": path, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob": blob_id(data),
            "url": f"{REPOSITORY}/blob/{REVISION}/{path}",
        })
    manifest = json.dumps({
        "repository": REPOSITORY, "revision": REVISION,
        "retrieved_on": "2026-10-02", "files": entries,
    }, ensure_ascii=False, indent=2) + "\n"
    manifest_path = destination / "manifest.json"
    if manifest_path.exists():
        if manifest_path.read_text() != manifest:
            raise FileExistsError(manifest_path)
    else:
        with manifest_path.open("x") as stream:
            stream.write(manifest)
    print(f"IMPORTED: {len(paths)} original files -> {destination}")
    return 0


def check_snapshot(root: Path = ROOT, source: Path | None = None) -> int:
    """Detect missing, altered, out-of-scope and unrecorded snapshot files."""
    destination = root / SNAPSHOT
    manifest = json.loads((destination / "manifest.json").read_text())
    failures: list[str] = []
    if manifest["revision"] != REVISION or manifest["repository"] != REPOSITORY:
        failures.append("snapshot identity")
    paths = [entry["path"] for entry in manifest["files"]]
    if len(paths) != len(set(paths)):
        failures.append("duplicate manifest paths")
    for entry in manifest["files"]:
        path = entry["path"]
        relative = Path(path)
        if not selected(path) or relative.is_absolute() or ".." in relative.parts:
            failures.append(f"out of scope: {path}")
            continue
        target = destination / path
        if not target.is_file():
            failures.append(f"missing: {path}")
            continue
        data = target.read_bytes()
        if (len(data) != entry["bytes"]
                or hashlib.sha256(data).hexdigest() != entry["sha256"]
                or blob_id(data) != entry["git_blob"]):
            failures.append(f"changed: {path}")
    actual = {
        path.relative_to(destination).as_posix()
        for path in destination.rglob("*")
        if path.is_file() and path != destination / "manifest.json"
    }
    failures.extend(f"unrecorded: {path}" for path in sorted(actual - set(paths)))
    if source is not None:
        expected = source_paths(source)
        if set(expected) != set(paths):
            failures.append("source tree coverage")
        for entry in manifest["files"]:
            if entry["path"] in expected:
                original = subprocess.run(
                    ["git", "-C", str(source), "rev-parse",
                     f"{REVISION}:{entry['path']}"],
                    check=True, capture_output=True, text=True,
                ).stdout.strip()
                if original != entry["git_blob"]:
                    failures.append(f"source blob mismatch: {entry['path']}")
    for failure in failures:
        print(f"FAILED: {failure}", file=sys.stderr)
    print(f"SNAPSHOT: {len(paths)} files, {len(failures)} failures")
    return int(bool(failures))


def audit_archives(root: Path = ROOT) -> int:
    """Index ZIP variants and export their otherwise hidden reading documents."""
    snapshot = root / SNAPSHOT
    destination = root / "school/school_project/course-domain/zip-text"
    destination.mkdir(parents=True, exist_ok=True)
    reports = []
    for archive in sorted((snapshot / "dataliteracy/dist").glob("*.zip")):
        entries = []
        with zipfile.ZipFile(archive) as bundle:
            for member in bundle.infolist():
                name = member.filename.replace("\\", "/")
                if name.endswith("/"):
                    continue
                relative = name.split("/", 1)[1]
                data = bundle.read(member)
                original = snapshot / "dataliteracy" / relative
                identical = original.is_file() and original.read_bytes() == data
                entries.append({
                    "path": relative, "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "matches_source": identical,
                })
                if not identical:
                    target = destination / archive.stem / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if target.exists():
                        if target.read_bytes() != data:
                            raise FileExistsError(target)
                    else:
                        with target.open("xb") as stream:
                            stream.write(data)
        reports.append({"archive": archive.name, "entries": entries})
    report_path = destination / "archive-audit.json"
    with report_path.open("w") as stream:
        stream.write(json.dumps(reports, ensure_ascii=False, indent=2) + "\n")
    print(f"ARCHIVES: {len(reports)} ZIPs indexed; hidden documents -> {destination}")
    return 0


def main() -> int:
    args = sys.argv[1:]
    match args:
        case ["import", source]:
            return import_snapshot(Path(source))
        case ["check"]:
            return check_snapshot()
        case ["check", source]:
            return check_snapshot(source=Path(source))
        case ["archives"]:
            return audit_archives()
        case _:
            print(__doc__, file=sys.stderr)
            return 2


if __name__ == "__main__":
    sys.exit(main())
