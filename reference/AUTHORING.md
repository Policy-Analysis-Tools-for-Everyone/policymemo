# Authoring a skill

How to write or revise one skill, so that 12 separately-authored files read as one
agent rather than 12 documents.

**Status: beta.** Revised as skills are tested, which is the point. Anything here
that turns out to be wrong in practice should be changed, not worked around.

---

## 1. Two layers, and the difference between them

**The method layer** is `reference/methods/`. Ten capability methods and 3 shared
methods, canonical, deliberately rich: provenance, distinctions, source synthesis,
worked examples, anti-patterns, scaffolds, boundaries and self-check rubrics. They
are written for maintainers and for future revisions.

**The skill layer** is `skills/`. Twelve runtime files containing only the
behaviour that changes what the agent does in a live conversation.

**Method completeness is not skill completeness.** The most common way to write a
bad skill in this repository is to compress the method faithfully. A method file
of 5,000 words does not become a good 5,000-word skill; it becomes a document the
agent reads instead of acting.

### The extraction test

A source insight belongs in a skill only if it changes what the agent:

- recognises
- asks
- challenges
- distinguishes
- produces
- refuses to invent
- hands off
- or uses to decide that enough work has been done

Everything else stays in the method layer. When revising, the useful question is
not "is this in the method?" but "what would the agent do differently if this line
were deleted?" If the answer is nothing, delete it.

### What to extract, per capability

1. **Trigger.** When should the agent recognise this capability is needed?
2. **Ownership.** What job does it own, and what does it explicitly not own?
3. **Attention.** What should it notice, challenge or distinguish?
4. **Questions.** What might it need to ask?
5. **Question discipline.** When should it stop asking?
6. **Moves.** The smallest useful reasoning sequence.
7. **Transitions.** What must be true before moving on.
8. **Output behaviour.** What a useful conversational result looks like.
9. **Handoffs.** What kind of gap belongs to a neighbour.
10. **Failure modes.** What should never happen.
11. **Self-check.** What must be true before the turn is returned.

---

## 2. The library

Method paths below are relative to `reference/methods/`.

| Skill | Canonical method |
|---|---|
| `house-rules` | no single method; see its sourcing header |
| `problem` | `capabilities/problem-definition-guidance.md` |
| `stakeholders` | `capabilities/stakeholder-analysis-guidance.md` |
| `evidence` | `capabilities/evidence-guidance.md` |
| `options` | `capabilities/alternatives-guidance.md` |
| `criteria` | `capabilities/criteria-guidance.md` |
| `outcomes` | `capabilities/outcomes-guidance.md` |
| `trade-offs` | `capabilities/trade-offs-guidance.md` |
| `decide` | `capabilities/decision-guidance.md` |
| `story` | `capabilities/storytelling-guidance.md` |
| `evaluation` | `capabilities/agent-evaluation-guidance.md` |

Three runtime names differ from their method filenames: `options`, `decide` and
`story`. Product language and source language differ, and forcing either to match
the other would lose something.

**No numeric prefixes.** They encoded a sequence the product does not have. A
skill name may begin with a digit, so this is a product decision rather than a
platform constraint, and reintroducing numbering would reintroduce the claim that
the capabilities are stages.

**Directory name is the identity.** In Claude Code the command comes from the
directory; frontmatter `name` is the display label. Keep them identical.

---

## 3. Frontmatter

Restrict frontmatter to the 6 fields the Agent Skills spec allows, because
anything else fails validation when the skill is uploaded to claude.ai or through
the Skills API:

```yaml
---
name: problem
description: >
  Use when the user brings a public problem that is not yet defined: messy
  notes, a concern, a complaint, an inherited proposal, a draft problem
  statement, or a solution presented as if it were a problem. ...
metadata:
  version: 0.2.0
  status: written, not behaviourally tested
---
```

Allowed: `name`, `description`, `license`, `compatibility`, `metadata`,
`allowed-tools`. Claude Code accepts more (`when_to_use`, `model`, `paths`,
`argument-hint` and others), and those work in Claude Code only. Anything outside
the 6 produces `Unexpected key(s) in SKILL.md frontmatter` on the other surfaces,
so keep per-skill status inside `metadata`, which is a free-form map, rather than
as a top-level `status:` key.

`metadata.version` is the release version, so a loaded skill can say which
version it is. Never edit it by hand: `tools/build-zips.py` stamps it into every
skill from `marketplace.json`. A new skill needs a `metadata:` block for the stamp
to land in.

Every skill carries the same `license` line, so the credit travels with each file
however it is copied:

```yaml
license: "CC BY-NC 4.0. policymemo.ai by Jack Strachan, https://policymemo.ai"
```

Give a new skill the same line. `LICENSE-CONTENT.md` has the terms.

Constraints worth checking mechanically: `name` is at most 64 characters and only
lowercase letters, digits and hyphens; `description` is non-empty and at most
1,024 characters; neither may contain XML tags or the words "claude" or
"anthropic".

### The description is the most important line in the file

It is what the agent matches against to decide the skill is relevant. Write it as
a **recognition rule**, not a course title.

The user will not say "use criteria". They will say the options are hard to
compare and they do not know what they are supposed to be measuring. The
description has to catch that.

What works: start with "Use when", then the situations in the user's own terms,
then the symptoms that should also trigger it, then any adjacent case it should
**not** take. `criteria` and `trade-offs` overlap enough that both need the
boundary stated, or one will swallow the other.

A skill that never triggers is a skill that does not exist. Test descriptions with
the routing pairs in `evals/tests/capability-pack.md`.

---

## 4. Sourcing header

Immediately after the frontmatter, an HTML comment naming the canonical method
first:

```html
<!--
Canonical method:
  reference/methods/capabilities/problem-definition-guidance.md
  - what it supplies. That file carries the underlying provenance.

Distilled shared behaviour carried here:
  reference/methods/shared/uncertainty-and-learning-guidance.md - which part,
    and what deliberately stays in the file.

Not grounded: <anything asserted without a source, and why>
-->
```

**Point at the canonical method, not the original sources.** The method file
already carries its own citations. A skill re-listing every paper and PDF is
maintaining a second copy of provenance that will drift. List an original source
only where a claim bypasses the method layer entirely.

Keep 4 kinds of grounding distinguishable, using the keys in
[BEHAVIOUR_SPEC.md](./BEHAVIOUR_SPEC.md): canonical method, project-owner
product decisions, material the owner authored directly, and behavioural
evidence from testing.

**The "not grounded" line matters more than the rest.** A skill with an empty one
is either very well sourced or not being honest. Where a skill genuinely adds
nothing beyond its method file, say that explicitly rather than leaving the line
off.

Record revisions in the header too, with what the evidence was. A skill whose
instructions cannot be traced to a reason becomes impossible to safely remove
anything from.

---

## 5. Body

The 5-part shape still works and most skills use it:

1. **What this owns, and when it applies.** Written as recognition, not
   permission. Include what it does **not** own.
2. **The moves**, each with an explicit transition condition.
3. **What strong output looks like.** Concrete enough to test against.
4. **Self-check.** Must-pass and should-pass.
5. **Failure modes.** Recognisable descriptions of going wrong.

Do not preserve the shape mechanically. `house-rules` has no moves. `stakeholders`
is organised around an artefact rather than a sequence. Behavioural completeness
beats format symmetry.

**Write standing instructions, not one-time steps.** An invoked skill's content
enters the conversation once and stays for the session; the file is not re-read on
later turns. Anything that should apply throughout has to read as a standing
habit. This is not theoretical: the first real test failed on exactly this, twice,
because two instructions were buried inside a numbered move and never fired.

**Every multi-move skill needs stopping or transition conditions.** They are what
stop a sequence becoming a march, and their absence is a named failure mode in the
behaviour specification.

**Size.** Roughly 1,000 to 2,500 words is useful pressure, not a limit. Keep the
file under 500 lines. A skill materially longer than its neighbours should have a
reason.

---

## 6. Constraints every skill must satisfy

1. **No document-shaped replies.** Never a title, an executive summary or a filed
   report as a routine answer. This bans a report, not structure: labelled parts,
   short lists and bold labels are often exactly right. Burying a 4-part answer in
   continuous prose to avoid looking like a document is the same failure from the
   other side, and it is the one the first real test actually hit.
2. **Do not restate the house rules.** Tone, question discipline, evidence
   discipline, competing framings, the vague-term challenge, the three standing
   considerations and the writing rules live in `house-rules` only. Twelve copies
   drift; one does not.
3. **Never name the method or framework in output, but use its vocabulary
   freely.** No "using the third step", no explaining the method instead of
   applying it. *Public value*, *operational capacity*, *political support*,
   *deficit*, *excess*, *mechanism*, *symptom*, *constraint* are plain English and
   should be used directly. Reading this as a ban on the terms produces evasive
   answers, which is what happened on the first test.
4. **Every move carries a transition condition.**
5. **Load `house-rules` first, and do not depend on it for safety.** Each
   capability skill opens by instructing the agent to load `house-rules` before
   anything else and treat it as binding, then carries the two rules that would be
   catastrophic if it were absent: invent nothing, and the user decides. The
   instruction is load-bearing rather than decorative. Claude chat has no always-on
   instruction layer that ships with a plugin, so this line is the only thing
   making the persona reach a capability. Copy it verbatim into any new skill.
6. **UK spelling**, concise, critical rather than affirming.
7. **Never invent facts, figures, dates or sources.** Marked placeholders and a
   statement of what would close the gap.
8. **No mandatory sequence.** No skill may require the user to have completed
   another one first.

---

## 7. How shared methods reach the runtime

The conceptual design is settled: strategic alignment, uncertainty and learning,
and risk-opportunity appraisal are shared, and they are not stages.

**The mechanical rule: a capability skill carries the minimum distilled shared
behaviour it needs, and names in its sourcing header what it deliberately left
behind.**

Worked examples of the size of "minimum":

- `outcomes` needs the outside view, feedback and path-dependence triggers, and a
  rule turning an ungrounded decision-sensitive forecast into a learning question.
  It does not need the rest of the appraisal method.
- `criteria` needs the appraisal gate: marginality, heterogeneity, quantifiable
  versus fundamental uncertainty. Not the full dynamic appraisal method.
- `stakeholders` needs the required-support check. Not a strategic alignment
  tutorial.
- `decide` needs a compact value, capacity and support check plus reversibility,
  lock-in and review conditions. Not a restatement of every shared source.

**Four things this rule exists to prevent:** 3 new mandatory sequential skills;
the full shared methods pasted into every capability; all shared theory dumped
into `house-rules`; and relying on a file being loaded automatically at runtime.

### Why not runtime file loading

Skills compose. Multiple skills can be active in one conversation, and an invoked
skill's content stays in context for the session, so `house-rules` and a
capability coexist without difficulty. A skill can also bundle supporting files in
its own directory that the agent reads on demand.

Neither is a reliable substitute for distillation here. Nothing guarantees
`house-rules` was loaded, and a skill uploaded on its own to claude.ai has no
`reference/` directory at all, so a path into the repository resolves to nothing.
Hence: distil what is needed, and point at the canonical path for the full
version, so both environments work.

`story` is the exception worth noting. It carries the operative writing rules
inline and bundles the full catalogue as `writing.md` in its own folder, because
that file is long, it is worth reading before drafting a document, and the inline
subset has to work when it is not read. Bundling it is what makes it available at
runtime; the old copy under `reference/` never was.

---

## 8. Routing and handoffs

Skills should recognise adjacent gaps without turning the conversation into
framework navigation.

Never say:

> Now invoke the evidence skill.

Say what the analysis turns on, and continue:

> The choice currently turns on whether uptake would actually change, and we do
> not have enough evidence for that yet.

Useful adjacent boundaries, none of them compulsory:

- `problem` to `evidence` when the frame depends on an untested factual or causal
  claim
- `stakeholders` to the support question when a proposal depends on a specific
  authoriser, funder or enabler
- `evidence` to a learning question when a critical unknown can be reduced
- `options` to `criteria` when the serious choice set is ready
- `criteria` to `outcomes` when the standards are clear enough to project against
- `outcomes` to `evidence` when a decision-sensitive projection is ungrounded
- `outcomes` to `trade-offs` when the projections are good enough
- `trade-offs` to `criteria` when the real disagreement is a missing or hidden
  value
- `trade-offs` to `decide` when the exchange is explicit
- `decide` back to `options` or `evidence` when the case is not decision-ready
- `story` to any upstream capability when the narrative exposes unfinished
  reasoning

Do not force this sequence when the user entered somewhere else.

---

## 9. The loop, per skill

1. **Read the canonical method.** If a behaviour has no method behind it, do not
   invent one. Plausible policy-textbook content written from general model
   knowledge is the specific failure this project exists to avoid, and it is hard
   to spot afterwards because it reads well.
2. **Draft `SKILL.md`** against the extraction test in section 1.
3. **Use it on real work.** Not a test case; an actual problem you have.
4. **Save the conversation** into `evals/raw/alpha/`.
5. **Revise.** Most of the value is here, not in the first draft.
6. **Re-test cold**, with `house-rules` loaded, ideally by someone who did not
   write it. Authoring and testing in the same session catches structural faults
   and not much else, because the author already knows what the file says.
7. **Write the regression case** from anything you fixed.
8. **Mark it done** against section 11.

Skill changes go through `evaluation`, which produces a change proposal with a
failure replay and a counter-case rather than editing another skill directly. The
counter-case is not optional: a fix for under-triggering reliably produces
over-triggering.

---

## 10. Choosing a model

Three different jobs that do not want the same model.

**Authoring: the strongest available.** Reading dense sources, separating what
they support from what they do not, and resisting the pull towards plausible
filler is the work that most rewards capability.

**Testing: whatever the product will actually run on.** This is the one people get
wrong. The agent's value is challenge quality, which is exactly the judgement that
varies most between models. A method validated only on the strongest model has a
floor you have not measured.

**Mechanical checking: the cheapest thing that works.** Counting questions per
reply, spotting framework name-drops, flagging digits that did not come from the
user. Regex, no model at all.

**These skills pin no model.** Anyone installing them runs whatever they already
use, which is correct for a skills library with no API key and no bill of its own.
The consequence is that challenge quality varies with the reader's model and this
repository cannot control that, so testing across models matters more here than it
would for a hosted product. Transcripts must always record the model.

---

## 11. Definition of done, per skill

- [ ] Grounded in its canonical method, with the sourcing header filled in
      including the *not grounded* line
- [ ] Description written as a recognition rule, with the adjacent non-trigger
      stated
- [ ] Frontmatter restricted to the 6 spec fields and validating
- [ ] Every multi-move section has a transition or stopping condition
- [ ] Distilled shared behaviour only, with what was left behind named
- [ ] All 8 constraints in section 6 satisfied
- [ ] Nothing restated that belongs to `house-rules`
- [ ] Listed in the relevant plugin entry in `.claude-plugin/marketplace.json`
- [ ] `python3 tools/build-zips.py` re-run and the result committed
- [ ] Used on a real problem, not a test case
- [ ] At least one conversation saved
- [ ] Tested cold, by someone who did not author it
- [ ] Regression cases written for anything fixed

Only the first 7 are true of any skill in this repository today.


---

## 12. Distribution packaging

The canonical skills live in `skills/`, one directory per skill, each containing a
`SKILL.md`. That is the only copy. Everything below is generated from it or points
at it, so a change to a skill is a change everywhere.

**Why `skills/` and not `.claude/skills/`.** It is where Claude's plugin
specification looks by default, so nothing needs a path override. It is also
platform-neutral, which matters if these ever go to another tool that supports
Agent Skills. Nothing about the format is Claude-specific.

**The marketplace.** `.claude-plugin/marketplace.json` is a catalogue that lets
someone install policymemo.ai from inside normal Claude by naming this repository. It
lists 2 plugin entries, both drawing from the same `skills/` folder:

- `mdee`, carrying `house-rules`, the 10 policy capabilities and
  `session-report`. What the public installs. `session-report` is not a policy
  capability: it turns the current conversation into a report the tester sends
  with one click, so it has to ship where testers are. It only runs when asked.
- `mdee-evaluation`, carrying `house-rules` and `evaluation`. A maintainer tool,
  kept out of the public product so policy users do not carry a capability aimed
  at whoever is working on the agent.

Both use `"source": "./skills"`, so the plugin is the `skills/` folder rather than
the repository, and both name their skills explicitly as paths relative to it:
`"./problem"`, not `"./skills/problem"`. A new skill that is not listed will not
ship. The default scan looks for a `skills/` folder *inside* the source, which
does not exist here, so the listed paths are the whole set for that entry.

**The source is deliberately not `"./"`.** A marketplace-root source makes the
whole repository the plugin payload, which was 61 files and 3.9 MB, 90% of it
`reference/` that nothing reads at runtime. Claude Code clones and does not care.
claude.ai fetches plugin content file by file over the GitHub API, and that
payload failed to install with `Failed to fetch content: 403`. Scoped to
`skills/` the payload is 11 files and 177 KB. Keep it that way: if a plugin ever
needs a file, move the file under `skills/`, rather than widening the source.

Bump `version` on both entries for every release. Testers cannot report which
version they ran otherwise, and `evaluation` asks them for exactly that.

**If a claude.ai install ever fails on the 2-entry layout**, collapse it to one
entry listing all 12 skills. That is the lower-risk configuration and it costs
only the `evaluation` separation.

**The zips.** `tools/build-zips.py` builds both kinds, and they must never be
edited by hand. Re-run it after any change to `skills/`, `marketplace.json` or the
licences, and commit the result. The build is deterministic, so an unchanged
source produces a byte-identical zip and does not churn in git. CI
(`.github/workflows/build-zips.yml`) reruns it on the same paths.

- `dist/skills/*.zip`, one per skill, for people on the Free plan who upload
  skills one at a time instead of installing a plugin.
- `dist/download/policymemo-ai-claude.zip`, what the Download button on the
  install page serves, for Upload local plugin when the marketplace install
  fails. It is the `mdee` plugin plus `LICENSE` and `LICENSE-CONTENT.md`, keeping
  the plugin name `mdee` so it is the same plugin whichever route installed it.

**Contributors** load the skills without installing anything by running
`claude --plugin-dir .` from the repository root.
