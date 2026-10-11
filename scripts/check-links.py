#!/usr/bin/env python3
"""Check relative Markdown links and #anchors in README.md and docs/**/*.md.

Skips docs/sources/ (original documents kept unchanged).
Usage: check-links.py [repo-root]    Exit 0 if no broken links, else 1.
"""
import re
import sys
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+[^)]*)?\)")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")


def slug(text):
    text = re.sub(r"[^\w\- ]", "", text.strip().lower())
    return text.replace(" ", "-")


def scan(path):
    """Yield (line_number, text, in_fence) for lines outside code fences."""
    fence = None
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = FENCE.match(line)
        if m:
            fence = None if fence == m.group(1) else (fence or m.group(1))
            continue
        if not fence:
            yield n, line


def anchors(path, cache={}):
    if path not in cache:
        found = set()
        for _, line in scan(path):
            m = HEADING.match(line)
            if m:
                base, k = slug(m.group(1)), 0
                while (base if k == 0 else f"{base}-{k}") in found:
                    k += 1
                found.add(base if k == 0 else f"{base}-{k}")
        cache[path] = found
    return cache[path]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent).resolve()
    files = [root / "README.md"] + sorted((root / "docs").rglob("*.md"))
    files = [f for f in files if f.is_file() and (root / "docs" / "sources") not in f.parents]
    total = broken = 0
    for f in files:
        for n, line in scan(f):
            for m in LINK.finditer(INLINE_CODE.sub("", line)):
                target = m.group(1)
                if SCHEME.match(target):
                    continue
                total += 1
                file_part, _, frag = target.partition("#")
                dest = (f.parent / file_part) if file_part else f
                ok = dest.exists()
                if ok and frag and dest.suffix == ".md" and dest.is_file():
                    ok = frag.lower() in anchors(dest)
                if not ok:
                    broken += 1
                    print(f"{f.relative_to(root)}:{n}: {target}")
    print(f"checked {total} links, {broken} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
