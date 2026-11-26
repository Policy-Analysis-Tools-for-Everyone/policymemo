#!/usr/bin/env python3
"""Build the Microsoft 365 Copilot and Google Gemini ports of policymemo.ai.

The canonical files are skills/<name>/SKILL.md. Everything this script writes is
generated from them plus ports/core.md, so a port never forks the method.

Usage, from the repository root:
    python3 tools/build-ports.py                       build into dist/ports/
    python3 tools/build-ports.py --check               validate only, write nothing
    python3 tools/build-ports.py --accept-house-rules  record that ports/core.md has
                                                       been reviewed against the
                                                       current house-rules, then build

Exit codes: 0 built or valid, 1 validation failed, 2 house-rules changed since the
last review of ports/core.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
PORTS = ROOT / "ports"
CORE = PORTS / "core.md"

# What a person sees after unzipping. Names say what to do, because many
# people will open the folder without reading anything else.
PREFIX = "policymemo"                      # knowledge file names; the instructions search by it
ZIP_NAME = "policymemo-ai-{surface}.zip"  # no folder inside: Extract All and Archive Utility make one
README_FILE = "0 Read me first.txt"
INSTRUCTIONS_FILE = "1 Paste into Instructions.txt"
SKILLS_DIR = "2 Upload these 8 skills"
KNOWLEDGE_FALLBACK_DIR = "3 No Skills option - upload these as knowledge instead"
GEMINI_SKILLS_DIR = "1 Upload these 10 skills"
FRONT_DOOR = "policymemo"
LICENCE_FILE = "Licence.txt"
LICENCE_ID = "CC BY-NC 4.0. policymemo.ai by Jack Strachan, https://policymemo.ai"
CREDIT = ("\n---\n\npolicymemo.ai by Jack Strachan (https://policymemo.ai), licensed under "
          "CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/\n")
LICENCE_TEXT = """policymemo.ai by Jack Strachan
https://policymemo.ai

Licensed under Creative Commons Attribution-NonCommercial 4.0 International
(CC BY-NC 4.0): https://creativecommons.org/licenses/by-nc/4.0/

You may use, share and adapt these files for non-commercial purposes, with
credit, a link to the licence, and a note of any changes. Using them in your own
analysis at work, including in paid employment, is permitted. Selling them,
selling something built from them, or offering them as part of a paid product or
service needs permission: jack@civicworks.co

Credit: "policymemo.ai by Jack Strachan (https://policymemo.ai), licensed under
CC BY-NC 4.0". Every file here carries that line; keep it in anything you share.

Full terms: https://github.com/Policy-Analysis-Tools-for-Everyone/policymemo/blob/main/LICENSE-CONTENT.md
"""
INSTALL_URL = "https://policymemo.ai/install/#{surface}"

# Copilot custom skills (Agent Builder): at most 8 per agent, SKILL.md under
# 20,000 characters, description at most 1,024. There are 9 capabilities, so one
# travels inside another as a supporting file, the way story carries writing.md.
SKILL_LIMIT = 8
SKILL_CHARS = 20000
SKILL_DESCRIPTION_CHARS = 1024
SKILL_NAME = "policymemo-{name}"
HOSTED = {"trade-offs": "decide"}  # capability -> skill that carries it
HOSTED_NOTE = {
    "trade-offs": (
        "This skill also carries the trade-offs capability. When the job is weighing what "
        "each serious option gains and gives up, how much, and what the choice turns on, "
        "read `trade-offs.md` in this folder and follow it.\n\n"
    ),
}
HOSTED_DESCRIPTION = {
    "trade-offs": (
        " Also use for trade-offs: comparing serious options by what each gains and gives "
        "up and how much, finding what the choice turns on, and who loses inside a positive "
        "total. That method is in trade-offs.md in this skill's folder."
    ),
}
# Copilot only: sections moved out of a skill's SKILL.md into a supporting file in
# the same zip, to keep SKILL.md well under SKILL_CHARS. Move only a section the
# skill uses conditionally, so loading it on demand loses nothing. Claude and
# Gemini carry the skill whole. capability -> [(heading, file, pointer)]
SPLIT = {
    "story": [(
        "PPC memo mode, section by section",
        "ppc-memo.md",
        "In PPC memo mode, read `ppc-memo.md` in this folder before drafting or "
        "reviewing, and follow it. It says what each of the 8 sections does, and that "
        "they are a guide, not a checklist.",
    )],
}
SKILL_HEADROOM = 0.95  # note any Copilot SKILL.md above this share of SKILL_CHARS
REVIEWED = PORTS / "house-rules.reviewed"
OUT = ROOT / "dist" / "ports"

# Order follows the README capability table. `evaluation` is for maintainers and
# is deliberately left out of every port.
CAPABILITIES = [
    "problem", "stakeholders", "evidence", "options", "criteria",
    "outcomes", "trade-offs", "decide", "story",
]

SURFACES = {
    "copilot": {
        "label": "Microsoft 365 Copilot",
        "hard_limit": 8000,   # Agent Builder field and declarative agent manifest
        "max_files": 20,      # embedded files uploaded from a device
        "skills": True,
        "knowledge_dir": KNOWLEDGE_FALLBACK_DIR,
        "readme": (
            "1. In Copilot Chat, click Create agent. When it opens a chat called\n"
            "   Message agent builder, press Skip.\n"
            "2. Open \"{instructions}\", select everything, copy it, and paste it\n"
            "   into the Instructions box.\n"
            "3. Under Skills, upload each of the 8 zip files in the \"{skills}\"\n"
            "   folder, one at a time. Do not unzip them and do not rename them.\n"
            "   No Skills option? Under Knowledge, upload the 10 files in\n"
            "   \"{knowledge}\" instead. No upload option at all? Skip this step.\n"
            "4. Click Create.\n"
        ),
        "knowledge_how": (
            "Each capability below is a skill named policymemo-<capability>; trade-offs "
            'sits inside policymemo-decide. Without skills, your knowledge holds "policymemo '
            '00 house rules", the full rules, and "policymemo 01 problem" to "policymemo 09 '
            'story". When the job changes, use that capability\'s skill or file and follow its moves.'
        ),
    },
    "gemini": {
        "label": "Google Gemini",
        # Gemini skills stand alone: no agent, no instructions box, no knowledge.
        # Every skill carries the house rules itself, and a front-door skill
        # holds them with the capability list.
        "standalone_skills": True,
        "readme": (
            "1. Open Gemini on a computer, at gemini.google.com or in the Mac app, and\n"
            "   go to Skills.\n"
            "2. Choose to upload a skill. In the \"{skills}\" folder, open each of\n"
            "   the 10 folders and upload the SKILL.md inside, one at a time. Start with\n"
            "   policymemo. Do not rename them.\n"
            "3. Start a new chat. Type /policymemo to begin, or just describe the\n"
            "   problem you are working on.\n"
        ),
        "knowledge_how": (
            "Each capability below is its own skill, named policymemo-<capability>, and "
            "carries these rules too. When the analytical job changes, use that skill and "
            "follow its moves."
        ),
    },
    "chatgpt": {
        "label": "ChatGPT",
        # A ChatGPT plugin: .codex-plugin/plugin.json plus skills/, uploaded as
        # one zip. Like Gemini, no instructions box, so every skill carries the
        # house rules; unlike Gemini, supporting files stay separate.
        "plugin": True,
        "knowledge_how": (
            "Each capability below is its own skill in this plugin, named "
            "policymemo-<capability>, and carries these rules too. When the analytical "
            "job changes, use that skill and follow its moves."
        ),
    },
}

LOAD_PARAGRAPH = re.compile(
    r"Load `house-rules` before anything else here.*?\n[ \t]*\n", re.DOTALL
)
PORT_LOAD_PARAGRAPH = (
    "The house rules in your instructions are already in force and bind everything "
    "below. Their 2 hardest rules hold throughout: invent nothing, and the user "
    "decides. Where this file says skill, read capability.\n\n"
)
HTML_COMMENT = re.compile(r"<!--.*?-->\s*", re.DOTALL)
PLACEHOLDER = re.compile(r"\{\{[A-Z_]+\}\}")
KEY_LINE = re.compile(r"^([A-Za-z_][\w-]*):[ \t]*(.*)$")
VERSION_LINE = re.compile(rb"^  version: .*\n", re.M)
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)  # stable zips, so rebuilds diff cleanly


class BuildError(Exception):
    """A problem that must be fixed before the ports are usable."""


def short_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def _closed_double_quote(value: str) -> bool:
    value = value.rstrip()
    if len(value) < 2 or not value.endswith('"'):
        return False
    inner = value[:-1]
    backslashes = len(inner) - len(inner.rstrip("\\"))
    return backslashes % 2 == 0


def parse_top_level(lines: list[str]) -> dict[str, str]:
    """Read top-level scalar keys from simple YAML frontmatter.

    Handles double-quoted, single-quoted, plain and block scalars, which covers
    every SKILL.md in this repository. Nested keys (metadata.status) are skipped.
    """
    fields: dict[str, str] = {}
    i = 0
    while i < len(lines):
        match = KEY_LINE.match(lines[i].rstrip("\n"))
        if not match:
            i += 1
            continue
        key, raw = match.group(1), match.group(2).strip()
        if raw[:1] in ("|", ">"):
            block, i = [], i + 1
            while i < len(lines) and (lines[i][:1] in (" ", "\t") or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            fields[key] = ("\n" if raw.startswith("|") else " ").join(block).strip()
            continue
        if raw.startswith('"'):
            while not _closed_double_quote(raw) and i + 1 < len(lines):
                i += 1
                raw += " " + lines[i].strip()
            try:
                fields[key] = json.loads(raw)
            except json.JSONDecodeError:
                fields[key] = raw.strip('"')
        elif raw.startswith("'") and raw.endswith("'") and len(raw) > 1:
            fields[key] = raw[1:-1].replace("''", "'")
        else:
            fields[key] = raw
        i += 1
    return fields


def read_skill(name: str) -> tuple[dict[str, str], str, str]:
    """Return frontmatter, body with supporting files appended, and a hash of them all."""
    fields, body, extras, sha = read_skill_parts(name)
    for extra_name, text in extras:
        body = (body.rstrip() + f"\n\n---\n\n# {extra_name}\n"
                f"Where this file says `{extra_name}` in this folder, it means this section.\n\n"
                + text + "\n")
    return fields, body, sha


def read_skill_parts(name: str) -> tuple[dict[str, str], str, list[tuple[str, str]], str]:
    """Return frontmatter, SKILL.md body, supporting files and a hash covering them all.

    Supporting files are any other Markdown in the skill's folder, such as
    skills/story/writing.md. Surfaces without folders get them appended to the
    capability's knowledge file, so they count towards its hash too.
    """
    path = SKILLS / name / "SKILL.md"
    if not path.is_file():
        raise BuildError(f"missing {path.relative_to(ROOT)}")
    raw = path.read_bytes()
    lines = raw.decode("utf-8").replace("\r\n", "\n").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise BuildError(f"{path.relative_to(ROOT)}: no frontmatter")
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            break
    else:
        raise BuildError(f"{path.relative_to(ROOT)}: frontmatter is not closed")
    fields = parse_top_level(lines[1:end])
    if fields.get("name") != name:
        raise BuildError(f"{path.relative_to(ROOT)}: name is {fields.get('name')!r}, expected {name!r}")
    body = "".join(lines[end + 1:])
    if name == "house-rules":
        # The review gate in ports/house-rules.reviewed is keyed to SKILL.md alone,
        # less the version line, which changes every release without changing a rule.
        return fields, body, [], short_hash(VERSION_LINE.sub(b"", raw))
    digest = raw
    extras = []
    for extra in sorted(f for f in path.parent.glob("*.md") if f.name != "SKILL.md"):
        data = extra.read_bytes()
        digest += data
        extras.append((extra.name, data.decode("utf-8").replace("\r\n", "\n").strip()))
    for sub in sorted(d for d in path.parent.iterdir() if d.is_dir()):
        raise BuildError(f"skills/{name}/{sub.name}/: subfolders are not ported; "
                         "update read_skill_parts in this script")
    return fields, body, extras, short_hash(digest)


def port_body(name: str, body: str) -> str:
    """A capability's SKILL.md body with provenance stripped and house-rules loading replaced."""
    body = HTML_COMMENT.sub("", body).strip() + "\n"
    body, replaced = LOAD_PARAGRAPH.subn(PORT_LOAD_PARAGRAPH, body, count=1)
    if replaced != 1:
        raise BuildError(
            f"skills/{name}/SKILL.md: the house-rules loading paragraph was not found. "
            "Update LOAD_PARAGRAPH in this script to match the new wording."
        )
    return body


def split_sections(name: str, body: str) -> tuple[str, dict[str, str]]:
    """Move each SPLIT section of a port body into its own file, leaving a pointer."""
    files = {}
    for heading, file_name, pointer in SPLIT.get(name, []):
        start = body.find(f"\n## {heading}\n")
        if start < 0:
            raise BuildError(f"skills/{name}/SKILL.md: no '## {heading}' section to split out. "
                             "Update SPLIT in this script to match the new heading.")
        end = body.find("\n## ", start + 1)
        end = len(body) if end < 0 else end
        section = body[start:end].strip()
        files[file_name] = f"# {heading}\n" + section.split("\n", 1)[1] + "\n"
        body = body[:start] + f"\n## {heading}\n\n{pointer}\n" + body[end:]
    return body, files


def copilot_skills() -> tuple[dict[str, bytes], list[dict], list[str], list[str]]:
    """One zip per Copilot skill, each holding a policymemo-<name>/ folder."""
    zips: dict[str, bytes] = {}
    report: list[dict] = []
    problems: list[str] = []
    notes: list[str] = []
    hosts: dict[str, list[str]] = {}
    for guest, host in HOSTED.items():
        hosts.setdefault(host, []).append(guest)
    for name in CAPABILITIES:
        if name in HOSTED:
            continue
        fields, body, extras, sha = read_skill_parts(name)
        skill = SKILL_NAME.format(name=name)
        description = " ".join(fields.get("description", "").split())
        body, split = split_sections(name, port_body(name, body))
        files = {f"{skill}/{f}": text for f, text in split.items()}
        for guest in hosts.get(name, []):
            g_fields, g_body, g_extras, g_sha = read_skill_parts(guest)
            if g_extras:
                raise BuildError(f"skills/{guest}/ has supporting files; hosting it needs them carried too")
            body = body.replace(PORT_LOAD_PARAGRAPH, PORT_LOAD_PARAGRAPH + HOSTED_NOTE[guest], 1)
            description += HOSTED_DESCRIPTION[guest]
            files[f"{skill}/{guest}.md"] = port_body(guest, g_body)
            sha = short_hash((sha + g_sha).encode())
        for extra_name, text in extras:
            files[f"{skill}/{extra_name}"] = HTML_COMMENT.sub("", text).strip() + "\n"
        data, skill_md = skill_zip(skill, description, body,
                                   {f.split("/", 1)[1]: v for f, v in files.items()})
        if len(skill_md) >= SKILL_CHARS:
            problems.append(f"copilot skill {skill}: SKILL.md is {len(skill_md)} characters; "
                            f"the limit is under {SKILL_CHARS}")
        elif len(skill_md) >= SKILL_CHARS * SKILL_HEADROOM:
            notes.append(f"copilot skill {skill}: SKILL.md is {len(skill_md)} characters, "
                         f"within {100 - round(SKILL_HEADROOM * 100)}% of the {SKILL_CHARS} limit")
        if len(description) > SKILL_DESCRIPTION_CHARS:
            problems.append(f"copilot skill {skill}: description is {len(description)} characters; "
                            f"the limit is {SKILL_DESCRIPTION_CHARS}")
        zips[f"{skill}.zip"] = data
        report.append({"skill": skill, "sha": sha, "skill_md_chars": len(skill_md),
                       "description_chars": len(description),
                       "files": ["SKILL.md"] + sorted(f.split("/", 1)[1] for f in files)})
    if len(zips) > SKILL_LIMIT:
        problems.append(f"copilot: {len(zips)} skills; the limit is {SKILL_LIMIT}")
    return zips, report, problems, notes


FRONT_DOOR_DESCRIPTION = (
    "Use for any public policy problem: a concern, rough notes, an inherited proposal, a "
    "draft, options to compare, a decision to make or a memo to write. Holds the house "
    "rules every policymemo skill follows and says which policymemo skill does each job. "
    "Start here when it is unclear which applies, or when the user asks for policymemo by name."
)
GEMINI_LOAD = (
    "The house rules below are in force throughout this skill and bind everything in it. "
    "Their 2 hardest rules hold throughout: invent nothing, and the user decides. "
    "Where this skill names another capability, it means the policymemo skill of that name.\n\n"
)


def skill_md(skill: str, description: str, body: str) -> str:
    return (f"---\nname: {skill}\ndescription: {json.dumps(description)}\n"
            f"license: {json.dumps(LICENCE_ID)}\n---\n\n" + body.rstrip() + "\n" + CREDIT)


def skill_zip(skill: str, description: str, body: str, extras: dict[str, str]) -> tuple[bytes, str]:
    """A skill zip with skill/SKILL.md at its main folder, as Copilot expects."""
    text = skill_md(skill, description, body)
    files = {f"{skill}/SKILL.md": text}
    files.update({f"{skill}/{name}": content.rstrip() + "\n" + CREDIT for name, content in extras.items()})
    return zip_bytes(files), text


def standalone_skills(rules: str, surface: str, fold_extras: bool) -> tuple[dict[str, str], list[dict], list[str]]:
    """The front door plus 1 skill per capability, each in its own folder.

    Every skill carries the house rules inline, because Gemini and ChatGPT
    skills have no instructions box. Gemini uploads one SKILL.md at a time, so
    there (fold_extras) supporting files are appended to the skill's own
    SKILL.md; ChatGPT keeps them as files beside it.
    """
    files: dict[str, str] = {}
    report: list[dict] = []
    problems: list[str] = []
    text = skill_md(FRONT_DOOR, FRONT_DOOR_DESCRIPTION, rules)
    files[f"{FRONT_DOOR}/SKILL.md"] = text
    report.append({"skill": FRONT_DOOR, "skill_md_chars": len(text),
                   "description_chars": len(FRONT_DOOR_DESCRIPTION)})
    start = rules.index("\n## ")
    inline = "## House rules\n" + re.sub(r"^## ", "### ", rules[start:].strip(), flags=re.M)
    for name in CAPABILITIES:
        fields, body, extras, sha = read_skill_parts(name)
        skill = SKILL_NAME.format(name=name)
        description = " ".join(fields.get("description", "").split())
        body = HTML_COMMENT.sub("", body).strip() + "\n"
        body, replaced = LOAD_PARAGRAPH.subn(
            lambda _: GEMINI_LOAD + inline + "\n\n---\n\n", body, count=1)
        if replaced != 1:
            raise BuildError(f"skills/{name}/SKILL.md: the house-rules loading paragraph was not found")
        for extra_name, extra in extras:
            extra = HTML_COMMENT.sub("", extra).strip() + "\n"
            if fold_extras:
                body = (body.rstrip() + f"\n\n---\n\n# {extra_name}\n"
                        f"Where this skill says `{extra_name}` in this folder, it means this section.\n\n"
                        + extra)
            else:
                files[f"{skill}/{extra_name}"] = extra.rstrip() + "\n" + CREDIT
        text = skill_md(skill, description, body)
        files[f"{skill}/SKILL.md"] = text
        if len(description) > SKILL_DESCRIPTION_CHARS:
            problems.append(f"{surface} skill {skill}: description is {len(description)} characters; "
                            f"the limit is {SKILL_DESCRIPTION_CHARS}")
        report.append({"skill": skill, "sha": sha, "skill_md_chars": len(text),
                       "description_chars": len(description)})
    return files, report, problems


def knowledge_file(name: str, fields: dict[str, str], body: str, sha: str,
                   surface_label: str, build_date: str) -> str:
    if name == "house-rules":
        body = HTML_COMMENT.sub("", body).strip() + "\n"
        use = "Use: always. Your instructions carry the core of these rules; this file holds the full text."
    else:
        body = port_body(name, body)
        description = " ".join(fields.get("description", "").split())
        use = description if description.lower().startswith("use when") else "Use when: " + description
    header = (
        f"policymemo.ai knowledge file: {name}\n{use}\n"
        f"Built {build_date} for {surface_label} from skills/{name}/SKILL.md ({sha}).\n\n"
    )
    return header + body.rstrip() + "\n" + CREDIT


def instructions(core: str, surface: str, house_sha: str, build_date: str) -> str:
    spec = SURFACES[surface]
    text = (core.replace("{{SURFACE}}", spec["label"])
                .replace("{{BUILD_DATE}}", build_date)
                .replace("{{HOUSE_RULES_SHA}}", house_sha)
                .replace("{{VERSION}}", version())
                .replace("{{KNOWLEDGE_HOW}}", spec["knowledge_how"]))
    leftover = sorted(set(PLACEHOLDER.findall(text)))
    if leftover:
        raise BuildError(f"ports/core.md: unfilled placeholders {', '.join(leftover)}")
    return text.strip() + "\n"


def version() -> str:
    """The Claude plugin's version, so every surface carries the same number."""
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    for plugin in marketplace["plugins"]:
        if plugin["name"] == "mdee":
            return plugin["version"]
    raise BuildError(".claude-plugin/marketplace.json: no mdee plugin entry")


def chatgpt_manifest() -> dict:
    """plugin.json for ChatGPT, from the same marketplace entry as the Claude plugin."""
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    entry = next(p for p in marketplace["plugins"] if p["name"] == "mdee")
    return {
        "name": "policymemo",
        "version": entry["version"],
        "description": entry["description"],
        "author": {"name": "Jack Strachan", "url": "https://policymemo.ai"},
        "homepage": "https://policymemo.ai",
        "repository": entry["repository"],
        "license": entry["license"],
        "keywords": entry["keywords"],
        "skills": "./skills/",
        "interface": {
            "displayName": "policymemo.ai",
            "shortDescription": "Work through a public policy problem properly",
            "longDescription": entry["description"],
            "developerName": "Jack Strachan",
            "category": "Productivity",
            "capabilities": ["Interactive"],
            "websiteURL": "https://policymemo.ai",
            "defaultPrompt": [
                "I think we've already jumped to a solution. Help me work out what the actual problem is.",
                "We've got evidence from another country that this worked. How much weight should we put on it?",
                "I've got 3 options and I'm struggling to decide what should count as better.",
            ],
        },
    }


def readme(surface: str, house_sha: str, build_date: str) -> str:
    spec = SURFACES[surface]
    steps = spec["readme"].format(instructions=INSTRUCTIONS_FILE, knowledge=spec.get("knowledge_dir", ""),
                                  skills=GEMINI_SKILLS_DIR if spec.get("standalone_skills") else SKILLS_DIR)
    return (
        f"policymemo.ai for {spec['label']}, beta {version()}\n\n"
        f"Full steps, with copy buttons and help if something goes wrong:\n"
        f"{INSTALL_URL.format(surface=surface)}\n\n"
        f"In short:\n{steps}\n"
        "Cannot upload the files? You may be looking inside the zip without having\n"
        "extracted it. Close this. On Windows, right-click the zip and choose\n"
        "Extract All. On a Mac, double-click the zip. Then use the folder that appears.\n\n"
        f"Built {build_date} from house-rules {house_sha}.\n"
    )


def lint(label: str, text: str) -> list[str]:
    """Style checks that would otherwise only surface in a tester's transcript."""
    notes = []
    if "\u2014" in text:
        notes.append(f"{label}: contains an em dash, which the house rules ban")
    odd = sorted({ch for ch in text if ord(ch) > 126})
    if odd:
        notes.append(f"{label}: non-ASCII characters {''.join(odd)!r} may count differently when pasted")
    return notes


def source_date() -> str:
    """Date of the last commit touching any input, so unchanged sources rebuild identically."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", "skills", "ports", "tools/build-ports.py",
             ".claude-plugin/marketplace.json"],
            cwd=ROOT, capture_output=True, text=True, check=True)
        if result.stdout.strip():
            return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return dt.date.today().isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def as_bytes(content: str | bytes) -> bytes:
    return content if isinstance(content, bytes) else content.encode("utf-8")


def zip_bytes(files: dict[str, str | bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for arcname in sorted(files):
            info = zipfile.ZipInfo(arcname, date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, as_bytes(files[arcname]))
    return buffer.getvalue()


def write_zip(path: Path, files: dict[str, str | bytes]) -> None:
    path.write_bytes(zip_bytes(files))


def build(check_only: bool, accept_house_rules: bool) -> int:
    house_fields, house_body, house_sha = read_skill("house-rules")

    reviewed = REVIEWED.read_text(encoding="utf-8").strip() if REVIEWED.exists() else None
    if accept_house_rules and not check_only:
        write_text(REVIEWED, house_sha + "\n")
        reviewed = house_sha
    if reviewed != house_sha:
        print(
            f"house-rules is now {house_sha}; ports/core.md was last reviewed against "
            f"{reviewed or 'nothing'}.\nRead the house-rules change, update ports/core.md "
            "to match, then run with --accept-house-rules.",
            file=sys.stderr,
        )
        return 2

    if not CORE.is_file():
        raise BuildError("missing ports/core.md")
    core = CORE.read_text(encoding="utf-8").replace("\r\n", "\n")
    build_date = source_date()
    skills = {"house-rules": (house_fields, house_body, house_sha)}
    for name in CAPABILITIES:
        skills[name] = read_skill(name)

    problems: list[str] = []
    notes: list[str] = []
    outputs: dict[str, dict[str, str | bytes]] = {}
    manifest = {"built": build_date, "house_rules": house_sha,
                "surfaces": {}}

    for surface, spec in SURFACES.items():
        files: dict[str, str | bytes] = {}
        text = instructions(core, surface, house_sha, build_date)
        if spec.get("standalone_skills"):
            notes.extend(lint(f"{surface} house rules", text))
            files[README_FILE] = readme(surface, house_sha, build_date)
            folders, skill_report, skill_problems = standalone_skills(text, surface, fold_extras=True)
            problems.extend(skill_problems)
            for path, content in folders.items():
                files[f"{GEMINI_SKILLS_DIR}/{path}"] = content
            files[LICENCE_FILE] = LICENCE_TEXT
            outputs[surface] = files
            manifest["surfaces"][surface] = {"label": spec["label"], "skills": skill_report}
            continue
        if spec.get("plugin"):
            notes.extend(lint(f"{surface} house rules", text))
            folders, skill_report, skill_problems = standalone_skills(text, surface, fold_extras=False)
            problems.extend(skill_problems)
            files[".codex-plugin/plugin.json"] = json.dumps(chatgpt_manifest(), indent=2) + "\n"
            for path, content in folders.items():
                files[f"skills/{path}"] = content
            files[LICENCE_FILE] = LICENCE_TEXT
            outputs[surface] = files
            manifest["surfaces"][surface] = {"label": spec["label"], "skills": skill_report}
            continue
        files[README_FILE] = readme(surface, house_sha, build_date)
        files[INSTRUCTIONS_FILE] = text
        files[LICENCE_FILE] = LICENCE_TEXT
        limit = spec["hard_limit"]
        if limit and len(text) > limit:
            problems.append(f"{surface}: instructions are {len(text)} characters; the limit is {limit}")
        elif limit and len(text) > 0.95 * limit:
            notes.append(f"{surface}: instructions are within 5% of the {limit}-character limit")
        notes.extend(lint(f"{surface} instructions", text))

        knowledge = []
        for index, name in enumerate(["house-rules"] + CAPABILITIES):
            fields, body, sha = skills[name]
            title = "house rules" if name == "house-rules" else name
            filename = f"{PREFIX} {index:02d} {title}.txt"
            content = knowledge_file(name, fields, body, sha, spec["label"], build_date)
            files[f"{spec['knowledge_dir']}/{filename}"] = content
            knowledge.append({"file": filename, "source": f"skills/{name}/SKILL.md",
                              "sha": sha, "chars": len(content)})
        if len(knowledge) > spec["max_files"]:
            problems.append(f"{surface}: {len(knowledge)} knowledge files; the limit is {spec['max_files']}")

        skill_report = []
        if spec["skills"]:
            zips, skill_report, skill_problems, skill_notes = copilot_skills()
            problems.extend(skill_problems)
            notes.extend(skill_notes)
            for zip_name, data in zips.items():
                files[f"{SKILLS_DIR}/{zip_name}"] = data

        outputs[surface] = files
        manifest["surfaces"][surface] = {
            "label": spec["label"],
            "instructions_chars": len(text),
            "instructions_limit": limit,
            "knowledge_files": knowledge,
            "knowledge_limit": spec["max_files"],
        }
        if spec["skills"]:
            manifest["surfaces"][surface]["skills"] = skill_report
            manifest["surfaces"][surface]["skill_limit"] = SKILL_LIMIT

    for line in notes:
        print(f"note: {line}")
    if problems:
        for line in problems:
            print(f"error: {line}", file=sys.stderr)
        return 1

    for surface, info in manifest["surfaces"].items():
        line = f"{surface:8}"
        if "instructions_chars" in info:
            line += (f" instructions {info['instructions_chars']:>5} / {info['instructions_limit']}   "
                     f"knowledge {len(info['knowledge_files'])} / {info['knowledge_limit']} files  ")
        largest = max(s["skill_md_chars"] for s in info["skills"])
        limit = f" / {info['skill_limit']}" if "skill_limit" in info else ""
        line += f" skills {len(info['skills'])}{limit}, largest SKILL.md {largest}"
        print(line)
    if check_only:
        print("check passed; nothing written")
        return 0

    if OUT.exists():
        shutil.rmtree(OUT)
    for surface, files in outputs.items():
        for relative, content in files.items():
            if isinstance(content, bytes):
                target = OUT / surface / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            else:
                write_text(OUT / surface / relative, content)
        write_zip(OUT / ZIP_NAME.format(surface=surface), files)
    write_text(OUT / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="validate only; write nothing")
    parser.add_argument("--accept-house-rules", action="store_true",
                        help="record that ports/core.md matches the current house-rules")
    args = parser.parse_args()
    try:
        return build(args.check, args.accept_house_rules)
    except BuildError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
