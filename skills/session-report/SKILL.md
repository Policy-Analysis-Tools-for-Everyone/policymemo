---
name: session-report
description: >
  Use when the user wants to send this conversation, or feedback about it, to
  the people who maintain policymemo.ai: "report this session", "send this to
  Jack", "this went wrong and I want to tell someone", "submit feedback",
  "file a session report". Drafts the report from the conversation, redacts it
  with the user, and gives them a link to send it as a GitHub issue or a
  private email. Only when the user asks. Not for writing a policy report,
  briefing or memo for their own work, and not for grading how well the agent
  performed, which the maintainers do afterwards.
license: "CC BY-NC 4.0. policymemo.ai by Jack Strachan, https://policymemo.ai"
metadata:
  version: 0.2.1
  status: written, not behaviourally tested
---

<!--
Canonical sources:
  [P] Product decision by the project owner, 2026-11: testers should be able to
      ask for a session report at any point and send it with one click, to a
      public GitHub issue or a private email, their choice.
  [P] evals/README.md - the 3 report channels, the 4 kinds of evidence, and
      why a debrief (the agent grading itself) is never cited where a
      transcript exists. This skill therefore reports and does not grade.
  [P] .github/ISSUE_TEMPLATE/session-report.yml - the field ids the GitHub link
      pre-fills. If a field id changes there, change it here.
  [P] site/beta/config.json - the support address, jack@civicworks.co.

Not grounded:
  - The length limits (about 7,000 characters for the GitHub link, about 1,800
    for the email link) are practical browser and mail-client limits, not
    documented guarantees. Revise them if links are seen to break.
  - Nothing analytical. This skill carries no policy method.
-->

# Session report

Load `house-rules` before anything else here, and treat it as binding on
everything below. If it cannot be loaded, its two hardest rules still hold:
invent nothing, and the user decides.

## What this owns

Turning the current conversation into a report the user can send to the people
who maintain policymemo.ai, and handing them the link that sends it. Nothing more.

**Only when asked.** Never offer this skill, suggest a report, or mention that
one is possible unless the user raises it. An agent that asks to be reviewed
changes the session it is in.

**Nothing is sent by you.** You have no way to send anything, and must never say
or imply that a report has gone. The user sends it by pressing Submit on GitHub or
Send in their email. Until they do, nothing has left the conversation.

**You report; you do not grade.** Do not assess whether the agent did well, say
what it should have done, or soften what it did. A model reviewing its own
session is the weakest evidence the maintainers get, and they grade from the
transcript afterwards. Your job is an accurate copy and the user's own words.

## The moves

### 1. Draft from the conversation

From what is already in the conversation, draft these without asking:

- **Goal.** What the user was trying to do, in a sentence or two, in their terms.
- **Where they got to.** The state reached: finished, part-way, stuck, abandoned,
  or somewhere unexpected. Describe the state, not whether it was good.
- **Skills seen to load.** Which policymemo.ai skills you loaded in this
  conversation, in order, as far as you can tell. Say "not sure" rather than
  guess. This is the one thing the chat surface does not show the maintainers.
- **Version.** The `metadata.version` of this skill, which is the installed
  release.
- **Model.** The model you are running as, if you know it. Otherwise "not sure".
- **The exchange.** The turns needed to understand what happened, **copied
  verbatim** from the conversation, each marked `**User:**` or `**Agent:**`. Never
  summarise, tidy or paraphrase a turn. Where a turn is too long, cut it with
  `[…]` and keep the part that matters. If the user has not said which part
  matters, take the turns around the point they are reporting, or the whole
  conversation if it is short.

Do not draft what surprised them, what they expected or what they think was
wrong. Those must be the user's own words.

**Transition:** the draft exists. Go straight to 2 in the same reply.

### 2. Redact with the user

Everything sent to GitHub is public. Before showing the draft, go through it and
substitute:

- names of people, and of organisations, teams and programmes
- figures, dates and places that could identify the work
- anything that reads as pre-decision, commercially or politically sensitive

Substitute with equivalents that keep the shape of the reasoning: a smaller
figure stays smaller, a ministry stays a ministry. Mark every substitution in the
text with square brackets, for example `[Department A]` or `[£2.1m, substituted]`,
and list them all after the draft. An unlabelled substitution later gets cited as
real.

Then show the user the draft and the substitution list, and ask one thing: what
surprised or frustrated them, and whether anything it told them was wrong. Say
they can skip it. Say plainly that the GitHub route is public, and that they
should change or cut anything else before sending.

**Transition:** the user has answered, skipped, or corrected the draft. If they
change the draft, apply it exactly and do not re-argue it.

### 3. Give them the two links

Produce both, each as a clearly labelled markdown link the user can click:

- **Public, on GitHub.** Opens the session-report form already filled in.
- **Private, by email.** Opens an email to jack@civicworks.co already filled in.
  For anything they would rather not make public. It may carry less redaction if
  they choose, but say that the maintainers only publish an emailed report with
  their consent.

Then one line each:

- On GitHub they still need to tick the box confirming they removed anything
  sensitive, then press **Submit new issue**.
- They can also attach the full conversation with Claude's own **Share** link,
  but only in the email. A share link shows the whole conversation unredacted, so
  it must never go in a GitHub issue.

Stop there. Do not resume the policy work unless the user does.

## Building the links

Use a code tool to build both URLs if one is available, with standard percent
encoding (in Python, `urllib.parse.quote(text, safe="")` for every value). If not,
encode by hand, and at least encode space as `%20`, newline as `%0A`, and `#`, `&`,
`%`, `+`, `?`, `=`, `"` and `'`. A link that breaks on the first `&` in the
transcript sends half a report.

**GitHub.** Base:
`https://github.com/Policy-Analysis-Tools-for-Everyone/policymemo/issues/new?template=session-report.yml`

Append `&<field>=<encoded value>` for each of these field ids:

| Field id | Value |
|---|---|
| `title` | `[Session] ` and a few words on what it was about, redacted |
| `goal` | Goal |
| `outcome` | Where they got to |
| `friction` | What surprised or frustrated them, their words, or leave out |
| `wrong` | What they think was wrong, their words, or leave out |
| `excerpt` | The redacted exchange, then the substitution list |
| `skills` | Skills seen to load |
| `version` | Version |
| `model` | Model |
| `install` | Leave out unless the user said how they installed it; then use the exact option text from the form |
| `first` | Leave out unless the user said; then `Yes, my first session` or `No, I'd used it before` |

Keep the whole URL under about 7,000 characters. If the excerpt would push it
over, leave `excerpt` out of the URL, say so, and give the redacted exchange in a
single code block for the user to paste into the form's *The exchange, redacted*
box.

**Email.** `mailto:jack@civicworks.co?subject=<encoded>&body=<encoded>`, subject
`policymemo.ai session report`, and the body the same fields as plain labelled
paragraphs. Keep it under about 1,800 characters. If it would be longer, put
everything except the exchange in the link, and give the exchange in a code block
to paste into the email.

## Self-check

**Must pass:**

- triggered by the user, never offered
- every turn in the excerpt copied verbatim, or cut with `[…]`, never paraphrased
- every substitution bracketed and listed
- the user told the GitHub route is public before any link is given
- the user's own words used for what was wrong; none supplied for them
- no assessment of the agent's own performance
- no claim that anything has been sent
- both links built, encoded, and within their limits, or the overflow given to
  paste
- version recorded from this skill's metadata; model and skills "not sure"
  rather than guessed

**Should pass:**

- one question, asked once, in move 2
- the draft fits on one screen before the excerpt
- the policy work is not resumed unprompted

## Failure modes

- **The self-review.** "In this session I could have asked fewer questions…" That
  is a debrief nobody asked for, and it colours what the maintainers read.
- **The tidied transcript.** A paraphrased exchange looks like evidence and isn't.
- **The quiet redaction.** A figure changed without a bracket.
- **The leaked share link.** A full, unredacted conversation pasted into a public
  issue.
- **"I've sent it."** You cannot, and saying so means the report never arrives.
- **The broken link.** Unencoded text that cuts the URL at the first `&` or `#`.
- **The sales pitch.** Mentioning reports, feedback or this skill when the user
  did not.
