# policymemo.ai

policymemo.ai helps you work through a public policy problem properly: working out what
the problem actually is, testing what you know, building and weighing options,
deciding, and writing it up for someone else to read.

It's built to make bad analysis harder to write. It challenges weak framing,
refuses to invent figures, keeps competing framings visible instead of quietly
picking one, and asks you one real question at a time rather than handing you a
plausible-looking document on request.

Inside it are 10 analytical capabilities that work together as one toolkit. You
don't pick between them. Claude does.

> **Beta 0.2.0.** The skills change as people use them. Read [Status](#status)
> before you rely on this for anything that matters.
>
> **Private beta, autumn 2026.** We're testing with policy students and a small group
> of practitioners, invited in waves. To take part, request access at
> [policymemo.ai/beta](https://policymemo.ai/beta/).

---

## Install

**[policymemo.ai/install](https://policymemo.ai/install/)** has the steps for Claude
(every plan, Free included), Microsoft 365 Copilot and Google Gemini. It takes
about 2 minutes, and there's a
[short video for Claude](https://www.loom.com/share/7a0075882a884d71bbc6a4b4dd29c9bc).

## Using it

Start an ordinary chat and describe the policy problem you're actually working on,
the way you'd describe it to a colleague. Claude reaches for the relevant capability
as the work develops. You never need to type `/problem` or any other command.

> "I think we've already jumped to a solution. Help me work out what the actual
> problem is."

> "We've got evidence from another country that this worked. How much weight
> should we put on it?"

> "I've got 3 options and I'm struggling to decide what should count as better."

It asks questions back. That's deliberate. If you want a document produced without
being asked anything, this is the wrong tool.

| Capability | The question it handles |
|---|---|
| `house-rules` | How the whole thing behaves. Always in play |
| `problem` | What is the problem? |
| `stakeholders` | Who matters, why, and with what power? |
| `evidence` | What do we know, and how strong is it? |
| `options` | What could we do? |
| `criteria` | What counts as better? |
| `outcomes` | What would probably happen? |
| `trade-offs` | What do we gain and give up? |
| `decide` | What should we choose? |
| `story` | How should this be communicated? |

There's no order you have to follow. Evidence sends you back to the problem,
trade-offs expose a criterion nobody stated, deciding reveals the options were poor.

**On one problem for weeks?** Create a Project in Claude, put your draft, evidence
and notes in it, and paste [`skills/house-rules/SKILL.md`](skills/house-rules/SKILL.md)
into the project instructions. Your material then stays in context, and the house
rules apply on every turn.

## Status

Written is not tested. What has been run, by whom, on which version, and what it
showed is recorded in [`evals/`](evals/) and nowhere else. Start with
[`evals/wiki/findings.md`](evals/wiki/findings.md).

## Telling us when it goes wrong

The most useful thing you can send is a conversation where it was **confidently
wrong**. Those are worth more than the ones where it worked.

[**Send a session report**](https://github.com/Policy-Analysis-Tools-for-Everyone/policymemo/issues/new?template=session-report.yml).
It takes about 3 minutes. **Reports are public**, so take out names, organisations,
figures and anything sensitive first. The form says how. If you're in the student
study, use the study feedback form instead.

## What's in this repository

| Folder | What it is |
|---|---|
| `skills/` | The skills. The only copy |
| `reference/` | The methods behind them, their sources, and how to write a skill |
| `evals/` | Tester reports and the findings drawn from them |
| `site/` | Sources for policymemo.ai |
| `ports/`, `tools/` | The Copilot and Gemini versions, and the build scripts |
| `docs/`, `dist/` | Generated: the website and the downloads |

Working on it? Read [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

Copyright (c) 2026 Jack Strachan. Code (`tools/`, `.github/`, `.claude-plugin/`)
is under the [MIT Licence](LICENSE). Everything else written for this project,
including the skills, methods, docs and evals, is under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): use, share and adapt it for
non-commercial purposes, with credit. Third-party sources are
cited, not licensed. See [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md) for the detail.
