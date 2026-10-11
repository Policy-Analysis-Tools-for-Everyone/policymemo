# Evaluation

Evidence about what policymemo.ai actually does, as opposed to what its skills say it
should do. Method: `reference/methods/capabilities/agent-evaluation-guidance.md`. The
runtime skill that applies it is `evaluation`.

This file is the schema. It says how the folder is laid out and how to work in it.

```text
evals/
  raw/
    alpha/     17 sessions on 0.1.1, T001–T004. Frozen
    beta/      one file per beta report, from TEMPLATE.md
  wiki/
    index.md     every wiki page, one line each
    log.md       append-only: what changed in the wiki, and when
    findings.md  what recurs, counted per version. Read first
    testers.md   pseudonymous register of who ran what
    prompts/     open questions the evidence is asking
  tests/       capability and regression cases. Synthetic
  student-study/  the UCL student beta research plan and its documents. No participant data
```

**Raw is evidence and is never rewritten.** If a skill changes afterwards, the wiki
records it, not the raw file. **The wiki is the distillate**, and it is rewritten as
often as the evidence demands.

The loop: real use → raw report → finding → change hypothesis → skill revision →
regression test → cold re-test.

## Three operations

### Ingest: a report arrives

Beta reports come in through three channels:

| Channel | Who | What to commit |
|---|---|---|
| GitHub issue, *session report* template | Anyone | The report, anonymised. Issues are public, so it should already be |
| Reply to the invite email | Practitioners | Only with consent to publish. Otherwise the finding and no conversation |
| Student study feedback form | Students | **Stays within the study.** Commit only what the study's consent allows: usually an anonymised note, or the finding alone. See `student-study/README.md` |

Then:

1. Give the tester an ID, continuing from the last row in `wiki/testers.md`, and add
   or update their row. One person keeps one ID across every report.
2. Copy `raw/beta/TEMPLATE.md` to `raw/beta/YYYY-MM-DD-T0NN-<topic>.md` and fill
   it in. A field nobody can confirm says so.
3. Mine it into `wiki/findings.md` with three questions:
   - **Does it add a sighting to an existing finding?** Add it with its version and
     update the `0.2.0` column. The count is the argument.
   - **Does it contradict one?** The valuable case. Record the contradiction rather
     than smoothing it over. F5 exists because two sessions disagreed.
   - **Does it leave something with nowhere to go?** That is a new prompt in
     `wiki/prompts/`, listed in `wiki/index.md`.
4. Delete any prompt the report answered or killed.
5. Add a line to `wiki/log.md`, and fill in the report's *Mined into* section.

### Query: what do we know about X?

Start at `wiki/index.md`, then `wiki/findings.md`. Cite the raw file behind any claim,
and give its version. A finding with only alpha sightings says nothing yet about `0.2.0`.

### Lint: after each beta wave

- Every finding's beta column is current against `raw/beta/`.
- Every prompt is still open. One nobody has run in six months was probably never a
  test, so delete it.
- `testers.md` count matches the raw files.
- Every page is in `index.md`. Record the lint in `log.md`.

## Four kinds of evidence, and what each is worth

Every raw file names its kind in the header. They are not equivalent.

**Transcript.** What the agent actually said. The only behavioural evidence.

**Debrief.** The agent's own account of a session, produced by the `evaluation` skill. A
model grading itself. **Never cite one where a transcript exists.** Its value is the
invocation log, since the chat surface doesn't show whether a skill loaded.

**Synthesis.** One author's cross-session review. May rest on sessions this repository
doesn't hold, and says so when it does. Change proposals in it stay proposals.

**Note.** A tester's own words, no transcript. Weaker than a transcript and not nothing:
it reports what the tester noticed. Never cite a note for what the agent said. Most
beta reports will be notes.

## Conventions

**Figures are substituted.** Every case number in every file is an invented
illustration, re-derived as a set so the relationships an argument depends on still
hold. Never cite one as evidence.

**Substitutions are made inside quotations too.** Quotes are otherwise verbatim,
typos included. Where a quote could not survive substitution it is paraphrased in
square brackets, never silently altered.

**Organisations are substituted consistently across files.**

**Headers carry what a reader needs**: kind, version, model, date, tester, cold or warm,
what loaded. The session report form asks for version, model and first-time use, so the
beta should have fewer gaps than the alpha.

## Counting

**n testers / m sessions.** Never a percentage, never "most users". A behaviour seen 4
times in one person's sessions is *1 tester (4 sessions)*.

Keep counts per version. Alpha (`0.1.1`) and beta (`0.2.0`) evidence are never added
together into one number.

## Cold testing, and what must never reach the agent

A session is **cold** when the tester hasn't read the skill files, hasn't seen what the
evals expect, and hasn't used policymemo.ai before. Their second session is not cold.

**Nothing about a tester reaches policymemo.ai.** The register and anything in this folder
go nowhere near a Project, a skill, a system prompt or Claude's memory. Break that and
every later result measures a personalised build, not the product a new person installs.

Never give an evaluation file the name of a file a runtime feature loads, and never use
auto memory as an evidence source.

## Privacy

1. **Pseudonymous IDs in the repository.** The mapping to real people is held privately
   by the maintainer and never committed.
2. **Consent before committing a conversation.** Record it in the report header and in
   `testers.md`.
3. **Where consent is refused,** or the work is pre-decision, commercially sensitive or
   politically sensitive, write the finding and don't commit the conversation.
4. **Redact before committing, never after.**
5. **Register fields stay broad categories.** No free text about a person.

## `tests/`

**Capability cases** (`capability-pack.md`) are hard, realistic and possibly unsolved. A
meaningful failure rate is the point. **Regression cases** protect behaviour already
shown to work and should pass almost every time.

Never report one score across both. For any behaviour that fires conditionally, keep a
matched pair: a case where it must fire and one where it must not. An agent tested only
on whether it challenges learns to challenge everything.

Run cases in the configuration you ship: an ordinary Claude chat with the plugin
installed.

## Do not overclaim

| State | What it means |
|---|---|
| **Written** | The skill exists and says what it should do |
| **Structurally checked** | Frontmatter valid, links resolve, no contradictions found by reading |
| **Behaviourally tested** | Run on real work, in a session that was saved |
| **Regression-tested** | A saved case re-runs and still passes after changes |

A self-test in the same session catches structure, not behaviour, because the author
already knows what the file says.
