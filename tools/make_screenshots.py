"""Capture the store and README screenshots from the demo vault.

Drives a running Obsidian through the CLI -- open a note, switch theme, scroll
to a heading -- grabs the window with tools/capture_window.ps1, then crops and
scales with Pillow. Element geometry is read out of the live DOM rather than
hard-coded, so a crop stays right when the content moves.

    uv run build.py
    uv run tools/setup_demo_vault.py
    # open demo/ in Obsidian, then:
    uv run --with pillow tools/make_screenshots.py
    uv run --with pillow tools/make_screenshots.py --only callouts --only cjk

Writes screenshots/*.png. The window is resized to 1600x900 (16:9), which is
what the 512x288 store image wants; on a scaled display the grab comes back
larger and is downsampled, which is why the text survives.

The listing is read by English speakers, so the app is switched to English for
the run and put back afterwards -- otherwise the tab bar, the status bar and
the properties header come out in whatever locale the machine runs.

Two things the run refuses to guess at, because both fail silently and are only
visible by eyeballing the output: a window that did not take the size it was
asked for, and an anchor heading that no longer exists in the note.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "screenshots"
CAPTURE = ROOT / "tools" / "capture_window.ps1"
VAULT = "demo"

WINDOW = (1600, 900)


def _obsidian_cli() -> str:
    found = shutil.which("obsidian")
    if found:
        return found
    guess = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Obsidian" / "Obsidian.com"
    if guess.exists():
        return str(guess)
    sys.exit("obsidian CLI not found -- add it to PATH")


CLI = _obsidian_cli()


def cli(*args: str) -> str:
    r = subprocess.run([CLI, f"vault={VAULT}", *args], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"obsidian {' '.join(args)} failed: {r.stderr or r.stdout}")
    return r.stdout.strip()


def js(code: str):
    """Run JS in the app and decode the `=> …` line the CLI prints back."""
    out = cli("eval", f"code={code}")
    out = out.removeprefix("=>").strip()
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return out


def app_ready(timeout: float = 60.0) -> None:
    """Block until the CLI can talk to the app again (used across a reload)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = subprocess.run([CLI, f"vault={VAULT}", "eval", "code=1"],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            return
        time.sleep(1.0)
    sys.exit("Obsidian did not come back after the reload")


def wait_for(expr: str, what: str, timeout: float = 20.0) -> None:
    """Poll a JS expression until it is truthy.

    Fixed sleeps are not enough here: right after a reload the reading view can
    take a couple of seconds to build, and every later step -- finding an anchor
    heading, measuring the pane -- reads an empty DOM if it goes early.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        if js(f"JSON.stringify(Boolean({expr}))") is True:
            return
        time.sleep(0.3)
    sys.exit(f"timed out after {timeout:.0f}s waiting for {what}")


def set_language(lang: str | None) -> None:
    """Set the app's UI language and reload. None restores the system locale."""
    setter = ("window.localStorage.removeItem('language')" if lang is None
              else f"window.localStorage.setItem('language', {json.dumps(lang)})")
    js(f"{setter}; 'ok'")
    js("app.commands.executeCommandById('app:reload'); 'ok'")
    time.sleep(3.0)
    app_ready()


_dpr: float | None = None
_frame: tuple[int, int] | None = None


def dpr() -> float:
    """The display's scale factor, so pixel sizes can be checked against CSS ones."""
    global _dpr
    if _dpr is None:
        _dpr = float(js("window.devicePixelRatio"))
    return _dpr


def capture(path: Path, size: tuple[int, int] | None = None) -> None:
    """Grab the window, and refuse to carry on if it is not the size we expect.

    MoveWindow has been seen to land on a 32767px-tall window instead of the
    one asked for. Nothing downstream notices -- the crop still succeeds and
    the PNG still gets written -- so the mismatch is caught here instead.
    """
    global _frame
    cmd = ["pwsh", "-NoProfile", "-File", str(CAPTURE), "-Out", str(path)]
    if size:
        cmd += ["-Width", str(size[0]), "-Height", str(size[1])]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"capture failed: {r.stderr or r.stdout}")

    got = Image.open(path).size
    if size:
        want = (round(size[0] * dpr()), round(size[1] * dpr()))
        if max(abs(got[0] - want[0]), abs(got[1] - want[1])) > 4:
            sys.exit(f"the window did not take the size it was asked for: wanted "
                     f"{size[0]}x{size[1]} at {dpr()}x scale ({want[0]}x{want[1]} px), "
                     f"grabbed {got[0]}x{got[1]} px -- restore the window and rerun")
        _frame = got
    elif _frame and got != _frame:
        sys.exit(f"the window changed size mid-run: {_frame[0]}x{_frame[1]} px -> "
                 f"{got[0]}x{got[1]} px -- leave it alone and rerun")


@dataclass
class Shot:
    name: str
    note: str
    theme: str = "light"
    anchor: str | None = None       # heading text to pull to the top of the pane
    height: int | None = None       # crop height in CSS px; None = whole window
    scroll: int = 0                 # extra scroll, CSS px, applied after the anchor
    width: int = 1400               # output width; the crop is scaled to it
    size: tuple[int, int] | None = None   # exact output size, overrides width


SHOTS: list[Shot] = [
    # Store listing: whole window, 16:9, at exactly 512x288.
    Shot("store", "Wikidian", size=(512, 288)),
    # README hero, both modes.
    Shot("light", "Wikidian", theme="light"),
    Shot("dark", "Wikidian", theme="dark"),
    # Feature shots, cropped to the reading pane.
    Shot("infobox", "Infoboxes", height=520, width=1200),
    Shot("properties", "Properties", height=520, width=1200),
    Shot("callouts", "Callouts", anchor="The set", height=520, width=1200),
    Shot("typography", "Typography", height=560, width=1200),
    Shot("images", "Figures", height=520, width=1200),
    Shot("semantic-colors", "Semantic colours", anchor="In use", height=420, width=1200),
    Shot("cjk", "中文排版", height=520, width=1200),
]

PANE = ".workspace-leaf.mod-active .markdown-reading-view"


def prepare(shot: Shot) -> None:
    cli("open", f"file={shot.note}")
    wait_for(f"app.workspace.getActiveFile()?.basename === {json.dumps(shot.note)}",
             f"{shot.note!r} to become the active file")
    js("const l=app.workspace.activeLeaf, s=l.getViewState(); "
       "s.state.mode='preview'; l.setViewState(s); 'ok'")
    js(f"app.changeTheme('{'obsidian' if shot.theme == 'dark' else 'moonstone'}'); 'ok'")
    wait_for(f"document.querySelectorAll('{PANE} .markdown-preview-sizer > div').length > 2",
             f"{shot.note!r} to render in reading view "
             "(is the Obsidian window minimised or covered?)")
    time.sleep(0.4)

    scroll = shot.scroll
    if shot.anchor:
        r = js(f"const t={json.dumps(shot.anchor)}; "
               f"const hs=[...document.querySelectorAll('{PANE} h2, {PANE} h3')]; "
               "const h=hs.find(e=>e.textContent.trim()===t); "
               "if(h) h.scrollIntoView({block:'start'}); "
               "JSON.stringify({found:!!h, headings:hs.map(e=>e.textContent.trim())})")
        if not r["found"]:
            sys.exit(f"{shot.name}: {shot.note} has no heading {shot.anchor!r} to "
                     f"scroll to. Its headings are: {', '.join(r['headings']) or '(none)'}. "
                     f"Fix the anchor in SHOTS.")
    elif not scroll:
        js(f"document.querySelector('{PANE} .markdown-preview-view').scrollTop=0; 'ok'")
    if scroll:
        js(f"document.querySelector('{PANE} .markdown-preview-view').scrollTop+={scroll}; 'ok'")
    time.sleep(0.6)


def pane_rect() -> dict:
    return js(f"const e=document.querySelector('{PANE}'); const b=e.getBoundingClientRect(); "
              "JSON.stringify({x:b.left,y:b.top,w:b.width,h:b.height,dpr:window.devicePixelRatio})")


def raise_window(tmp: Path) -> None:
    """Bring the window forward at the size every grab expects.

    This has to happen before the first note is prepared, not just before the
    first grab: Obsidian does not build the reading view while its window is
    minimised or fully covered, so a run that starts with the window buried
    finds an empty pane and no headings to anchor to.
    """
    capture(tmp / "_frame.png", WINDOW)


def run(shot: Shot, tmp: Path) -> None:
    prepare(shot)
    raw = tmp / f"{shot.name}-raw.png"
    capture(raw)

    img = Image.open(raw)
    if shot.height is not None:
        r = pane_rect()
        d = r["dpr"]
        img = img.crop((
            round(r["x"] * d),
            round(r["y"] * d),
            round((r["x"] + r["w"]) * d),
            round(min(r["y"] + shot.height, r["y"] + r["h"]) * d),
        ))

    if shot.size:
        img = img.resize(shot.size, Image.LANCZOS)
    elif img.width > shot.width:
        h = round(img.height * shot.width / img.width)
        img = img.resize((shot.width, h), Image.LANCZOS)

    # These are flat UI screenshots -- 256 indexed colours are visually
    # indistinguishable from truecolour here and about a third of the bytes,
    # which matters for images the README loads on every page view.
    img = img.convert("RGB").quantize(colors=256, dither=Image.NONE)

    dest = OUT / f"{shot.name}.png"
    img.save(dest, optimize=True)
    print(f"{img.width}x{img.height}  {dest.relative_to(ROOT)}")


def select(only: list[str] | None) -> list[Shot]:
    if not only:
        return SHOTS
    known = {s.name: s for s in SHOTS}
    unknown = [n for n in only if n not in known]
    if unknown:
        sys.exit(f"no such shot: {', '.join(unknown)}. "
                 f"Known shots: {', '.join(known)}")
    return [known[n] for n in only]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--only", action="append", metavar="NAME",
                    help="rebuild just this shot; repeatable")
    args = ap.parse_args(argv)
    shots = select(args.only)

    OUT.mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="wikidian-shots-"))
    was = js("JSON.stringify(window.localStorage.getItem('language'))")

    try:
        if was != "en":
            set_language("en")
        raise_window(tmp)
        for shot in shots:
            run(shot, tmp)
    finally:
        js("app.changeTheme('moonstone'); 'ok'")
        if was != "en":
            set_language(was)
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
