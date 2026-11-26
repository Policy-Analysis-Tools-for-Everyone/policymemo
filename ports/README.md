# Ports

Microsoft 365 Copilot and Google Gemini versions of policymemo.ai, generated from the
Claude version. `skills/` is the only source of the method. Nothing here edits it, and
a port never forks it.

| File | What it is |
|---|---|
| `core.md` | The only hand-written port text: the house rules compressed to fit Copilot's 8,000-character instructions field, and 1 line per capability. Placeholders in double braces are filled at build time |
| `house-rules.reviewed` | The house-rules hash that `core.md` was last checked against |
| `testing.md` | The test plan. Results go in `evals/` |

## Building

    python3 tools/build-ports.py           build into dist/ports/
    python3 tools/build-ports.py --check   validate only, write nothing

Set-up steps for people installing a port live on the install page, `site/install/body.html`,
which is the only copy. Each zip, `dist/ports/policymemo-ai-<surface>.zip`, opens to files
named for what to do with them, because many people will not read anything else:

Copilot:

    0 Read me first.txt                  short steps, and a link to the install page
    1 Paste into Instructions.txt
    2 Upload these 8 skills/             policymemo-problem.zip to policymemo-story.zip
    3 No Skills option - upload these as knowledge instead/       the 10 knowledge files

Gemini:

    0 Read me first.txt
    1 Upload these 10 skills/            policymemo/SKILL.md, policymemo-criteria/SKILL.md ... policymemo-trade-offs/SKILL.md

ChatGPT, uploaded as one zip without unzipping it:

    .codex-plugin/plugin.json            the plugin manifest, from marketplace.json's mdee entry
    skills/                              policymemo/, then policymemo-criteria/ to policymemo-trade-offs/
    Licence.txt

All 3 also carry `Licence.txt`, and every skill, knowledge file and instructions text
ends with the CC BY-NC 4.0 credit line (`CREDIT` in the script). Port skills carry a
`license` field in their frontmatter, as the Claude skills do.

**Copilot skills.** Agent Builder accepts SKILL.md skill zips, the same format as
the Claude skills. It allows at most 8 skills per agent, each SKILL.md under 20,000
characters with a description of at most 1,024. Each skill is the capability's
SKILL.md with provenance stripped and house-rules loading replaced, named
`policymemo-<capability>`, with its supporting files beside it. There are 9
capabilities, so `trade-offs` travels inside `policymemo-decide` as `trade-offs.md`,
with a line in decide's body and description pointing to it (`HOSTED` in the
script). The build fails if any of those limits is broken, and notes any SKILL.md
within 5% of 20,000.

`story` is the longest skill, so its Copilot SKILL.md moves one section, *PPC
memo mode, section by section*, into `ppc-memo.md` in the same zip, leaving a
line that says to read it in PPC mode (`SPLIT` in the script). That section is
only used when someone asks for that memo format, so loading it on demand loses
nothing. The source isn't touched: Claude and Gemini carry `story` whole, and the
Copilot knowledge file keeps the section inline. If the heading changes, the
build stops until `SPLIT` is updated. Split a section out only if it is used
conditionally, never a rule that holds on every use.

**ChatGPT plugin.** A ChatGPT plugin is `.codex-plugin/plugin.json` plus a `skills/`
folder of ordinary skill folders. ChatGPT skills have no instructions box either, so
the skills are the Gemini set: the front door plus 9 capability skills, each carrying
the house rules inline. Unlike Gemini, a plugin keeps supporting files, so `story`'s
`writing.md` stays a separate file. Free accounts have no Skills option but can upload
a plugin; paid accounts can do either.

**Gemini skills.** Gemini replaced Gems with skills, which stand alone: there is no
agent, no instructions box and no knowledge. So every capability skill carries the
house rules itself, as the compressed text from `core.md`, put where the Claude skill
says to load `house-rules`. A tenth skill, `policymemo`, is the front door: the same
house rules and the capability list, for people who type `/policymemo`. Gemini has no
8-skill limit, so `trade-offs` is its own skill there. Gemini uploads one `SKILL.md`
at a time, so each skill is a single file: `story`'s `writing.md` is appended to it. Descriptions are capped at 1,024
characters; Google publishes no SKILL.md limit.

The zip has no folder inside it. Windows Extract All and the Mac's Archive Utility each
make one named after the zip, so an inner folder would nest a second copy. The Copilot
knowledge file prefix, `policymemo`, is what the instructions search for, so renaming
the files breaks the link between them.

Each knowledge file is a skill's `SKILL.md` with its provenance comments removed and its house-rules loading paragraph replaced,
followed by any other Markdown in that skill's folder (today, `story/writing.md`).

The build fails if the Copilot instructions exceed 8,000 characters, or Copilot would
need more than 20 knowledge files.
Inputs are dated by their last commit, so an unchanged source rebuilds identically.

## When house-rules changes

The build stops with exit code 2. Read the house-rules change, update `core.md` to
match, then run:

    python3 tools/build-ports.py --accept-house-rules

Only `house-rules` is gated, because `core.md` compresses it. Changes to a capability
skill flow into its knowledge file on the next build with nothing to review, unless
the skill's description changes enough that its 1-line entry under Capabilities in
`core.md` no longer fits.
