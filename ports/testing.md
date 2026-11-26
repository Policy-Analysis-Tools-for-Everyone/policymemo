# Testing the ports

How to test the ports. What has been run, and what it showed, is recorded in
`evals/` and nowhere else.

## What the ports can't inherit

The Claude evidence in `evals/` doesn't transfer. Every session there ran on Claude
with the skills loaded as skills. A port changes 3 things at once: the model, the
house rules (compressed into `core.md`), and how capability text arrives (Copilot and
Gemini skills, or Copilot knowledge files). A failure on a port can come from any of the 3.

## Order

Run these in order. Each stage is cheap and stops a wasted run at the next.

1. **Install check.** Follow the [install page](https://policymemo.ai/install/) exactly, from the download onwards. Note anything about the download or unzipping that would confuse someone new to it. Record
   whether the instructions saved whole, and on Copilot whether skills, knowledge
   upload, both or neither were available. On Gemini, record whether all 10 skills
   uploaded and are switched on.
2. **Smoke test.** Open with each of the 3 README openings, in fresh chats. Check the
   things the instructions carry directly: 1 question at a time, no document as a
   routine reply, no invented figure, no framework named, UK spelling, no em dashes.
3. **Knowledge reach.** The core rules are in the instructions, so the smoke test
   can't show whether the files are used. Use cases whose pass depends on a move
   that only a knowledge file holds:
   - `evals/wiki/prompts/system-map-trigger.md` (the `problem` file)
   - a request for a one-page PPC memo from a finished analysis. The section
     structure under "PPC memo mode" exists only in the `story` file. Don't use
     W4 or W5 for this: `core.md` now carries their rules too
   - `evals/wiki/prompts/stakeholder-sequencing.md` (the `stakeholders` file)

   Run each on an agent with the skills (Copilot) or knowledge files, and on one
   built from the instructions alone. If the runs don't differ, the method isn't
   being reached. On Copilot, also run a trade-offs case: it lives inside
   `policymemo-decide`, so it shows whether a supporting file is read at all.
   On Gemini, run each once with no slash and once with `/policymemo-<capability>`.
   If only the slash run reaches the method, Gemini is not picking skills up on its own.
4. **Regression.** Run `evals/tests/regression-problem-first-session.md` and
   `evals/tests/regression-writing-and-transfer.md` as written, changing only the
   surface.
5. **Real use.** Sessions from real work, reported through the session report.

## Recording

Record port runs in `evals/raw/alpha/` like any other session, with these fields added
to the header: surface (Copilot or Gemini), the build date and house-rules hash from
`0 Read me first.txt`, whether skills or knowledge files were present, and on Gemini
whether the skill was invoked with `/` or picked up on its own.

A finding that reproduces on Claude belongs to the skills. A finding that appears only
on a port belongs to `ports/core.md` or the build, and is fixed there, never by
editing `skills/` to suit a port.
