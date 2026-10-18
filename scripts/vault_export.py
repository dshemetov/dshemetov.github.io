# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml", "typer"]
# ///
"""Export blog posts from an Obsidian vault into Hugo page bundles.

See notes/obsidian-workflow.md for the workflow and conversion rules.
"""

import datetime
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

import typer
import yaml

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif"}
SKIP_DIRS = {".obsidian", ".trash", ".git"}
GENERATED_NOTE = "# Generated from the Obsidian vault by scripts/vault_export.py. Edit the note there.\n"

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.S)
CODE = re.compile(r"(^```.*?^```[^\n]*$|`[^`\n]+`)", re.S | re.M)
COMMENT = re.compile(r"%%.*?%%", re.S)
EMBED = re.compile(r"!\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]*))?\]\]")
MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]*))?(?:\|([^\]]*))?\]\]")


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def warn(note: Path, msg: str) -> None:
    print(f"warning: {note.name}: {msg}", file=sys.stderr)


def read_front_matter(text: str) -> dict:
    fm = FRONT_MATTER.match(text)
    return (yaml.safe_load(fm.group(1)) if fm else None) or {}


class Exporter:
    def __init__(self, vault: Path, out: Path):
        self.vault = vault
        self.out = out
        candidates = sorted(
            p for p in (vault / "blog").rglob("*.md") if p.read_text().strip()
        )
        self.notes = [p for p in candidates if not read_front_matter(p.read_text()).get("draft")]
        self.drafts = len(candidates) - len(self.notes)
        self.slugs = {p.stem.lower(): slugify(p.stem) for p in self.notes}
        self.files: dict[str, list[Path]] = {}
        for p in vault.rglob("*"):
            if p.is_file() and not SKIP_DIRS & set(p.relative_to(vault).parts):
                self.files.setdefault(p.name.lower(), []).append(p)

    def find_file(self, note: Path, name: str) -> Path | None:
        """Resolve an attachment like Obsidian does: relative path, then by filename."""
        rel = note.parent / name
        if rel.is_file():
            return rel
        matches = self.files.get(Path(name).name.lower(), [])
        if len(matches) > 1:
            warn(note, f"{name!r} matches {len(matches)} files, using the shortest path")
        return min(matches, key=lambda p: len(p.parts), default=None)

    def copy_image(self, note: Path, bundle: Path, name: str) -> str | None:
        src = self.find_file(note, name)
        if src is None:
            warn(note, f"image {name!r} not found in vault")
            return None
        dest = src.name.replace(" ", "-")
        bundle.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, bundle / dest)
        return dest

    def convert(self, note: Path, bundle: Path, text: str) -> str:
        def embed(m: re.Match) -> str:
            target, option = m.group(1).strip(), (m.group(2) or "").strip()
            if Path(target).suffix.lower() not in IMAGE_EXTS:
                warn(note, f"embed {m.group(0)!r} is not an image, left as is")
                return m.group(0)
            dest = self.copy_image(note, bundle, target)
            if dest is None:
                return m.group(0)
            if re.fullmatch(r"\d+(x\d+)?", option):
                return f'{{{{< figure src="{dest}" width="{option.split("x")[0]}" >}}}}'
            return f"![{option}]({dest})"

        def md_image(m: re.Match) -> str:
            alt, target = m.groups()
            if re.match(r"[a-z]+:", target) or target.startswith("/"):
                return m.group(0)
            dest = self.copy_image(note, bundle, unquote(target))
            return f"![{alt}]({dest})" if dest else m.group(0)

        def wikilink(m: re.Match) -> str:
            target, heading, alias = m.group(1).strip(), m.group(2), m.group(3)
            label = alias or target
            slug = self.slugs.get(target.lower())
            if slug is None:
                warn(note, f"[[{target}]] is not a blog post, exported as plain text")
                return label
            anchor = f"#{slugify(heading)}" if heading else ""
            return f'[{label}]({{{{< relref "/blog/{slug}{anchor}" >}}}})'

        def transform(segment: str) -> str:
            segment = COMMENT.sub("", segment)
            segment = EMBED.sub(embed, segment)
            segment = MD_IMAGE.sub(md_image, segment)
            return WIKILINK.sub(wikilink, segment)

        parts = CODE.split(text)
        return "".join(p if i % 2 else transform(p) for i, p in enumerate(parts))

    def ensure_date(self, note: Path, text: str, fm: re.Match | None) -> str:
        """Write a missing date back into the vault note so it stays stable."""
        now = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
        if fm:
            text = f"---\n{fm.group(1)}\ndate: {now}\n---\n" + text[fm.end() :]
        else:
            text = f"---\ndate: {now}\n---\n\n" + text
        note.write_text(text)
        warn(note, f"no date, wrote date: {now} to the vault note")
        return text

    def export_note(self, note: Path) -> None:
        text = note.read_text()
        fm = FRONT_MATTER.match(text)
        data = read_front_matter(text)
        if "date" not in data:
            text = self.ensure_date(note, text, fm)
            fm = FRONT_MATTER.match(text)
        header = fm.group(1)
        if not data.get("title"):
            header = re.sub(r"^title:.*\n?", "", header, flags=re.M)
            header = f"title: {yaml.safe_dump(note.stem).splitlines()[0]}\n{header}"
        bundle = self.out / self.slugs[note.stem.lower()]
        body = self.convert(note, bundle, text[fm.end() :])
        bundle.mkdir(parents=True, exist_ok=True)
        (bundle / "index.md").write_text(f"---\n{GENERATED_NOTE}{header}\n---\n{body}")

    def run(self) -> None:
        if not self.notes:
            sys.exit(f"no notes found in {self.vault / 'blog'}")
        seen: dict[str, Path] = {}
        for note in self.notes:
            slug = self.slugs[note.stem.lower()]
            if slug in seen:
                sys.exit(f"{note} and {seen[slug]} both map to /blog/{slug}/")
            seen[slug] = note
        for p in self.out.iterdir():
            if p.is_dir():
                shutil.rmtree(p)
            elif p.name != "_index.md":
                p.unlink()
        for note in self.notes:
            self.export_note(note)
        print(f"exported {len(self.notes)} posts to {self.out}, skipped {self.drafts} drafts")


def read_group(s: str, i: int) -> tuple[str, int]:
    """Read a balanced {...} group starting at s[i]; return its content and the index after it."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "\\":
            continue
        if s[j] == "{" and (j == 0 or s[j - 1] != "\\"):
            depth += 1
        elif s[j] == "}" and s[j - 1] != "\\":
            depth -= 1
            if depth == 0:
                return s[i + 1 : j], j + 1
    raise ValueError(f"unbalanced braces near {s[i : i + 40]!r}")


def parse_preamble(text: str) -> dict[str, str | list]:
    """Turn \\newcommand and \\DeclareMathOperator lines into MathJax macro definitions."""
    text = re.sub(r"(?<!\\)%.*", "", text)
    macros: dict[str, str | list] = {}
    command = re.compile(r"\\(newcommand|renewcommand|DeclareMathOperator)\*?\s*")
    for m in command.finditer(text):
        i = m.end()
        if text[i] == "{":
            name, i = read_group(text, i)
        else:
            name = re.match(r"\\[A-Za-z]+", text[i:]).group(0)
            i += len(name)
        n_args = re.match(r"\s*\[(\d)\]", text[i:])
        if n_args:
            i += n_args.end()
        i += len(text[i:]) - len(text[i:].lstrip())
        body, _ = read_group(text, i)
        if m.group(1) == "DeclareMathOperator":
            body = f"\\operatorname{{{body}}}"
        name = name.strip().lstrip("\\")
        macros[name] = [body, int(n_args.group(1))] if n_args else body
    return macros


def export_macros(vault: Path, out: Path) -> None:
    preamble = vault / "preamble.sty"
    if not preamble.exists():
        print(f"warning: {preamble} not found, left {out} as is", file=sys.stderr)
        return
    macros = parse_preamble(preamble.read_text())
    out.write_text(json.dumps(dict(sorted(macros.items())), indent=2) + "\n")
    print(f"exported {len(macros)} math macros to {out}")


def main(
    vault: Path,
    out: Path = Path("content/blog"),
    macros: Path = Path("data/math_macros.json"),
) -> None:
    vault = vault.expanduser()
    Exporter(vault, out).run()
    export_macros(vault, macros)


if __name__ == "__main__":
    typer.run(main)
