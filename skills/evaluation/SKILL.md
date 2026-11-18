---
name: evaluation
description: >
  Use when the subject is this agent rather than a policy problem: reviewing a
  saved session or transcript for what the agent did well and badly, synthesising
  findings across several sessions, designing test cases for a skill that is
  being written or changed, or checking whether a skill revision fixed what it
  was meant to fix without breaking something else. Also use when someone reports
  that the agent was unhelpful or confidently wrong and the finding needs
  classifying before anything gets edited. Not for evaluating whether a public
  policy worked.
license: "CC BY-NC 4.0. policymemo.ai by Jack Strachan, https://policymemo.ai"
metadata:
  version: 0.2.1
  status: written, behaviourally tested: it produced 3 debriefs and a tester report in evals/
---

<!--
Canonical method:
  reference/methods/capabilities/agent-evaluation-guidance.md
  - the 4 levels (session, skill, skill system, product), the 4 modes, cold
    versus warm runs, finding classification, severity separate from frequency,
    trigger and non-trigger cases, capability versus regression suites, the
    change-proposal format and the grading model. Provenance: this project's own
    transcripts and behaviour specification; Anthropic, "Demystifying evals for
    AI agents" (2026); OpenAI, "How evals drive the next chapter in AI for
    businesses" (2025).

Not grounded:
  - Nothing beyond that file.
-->

# Evaluation

Load `house-rules` before anything else here, and treat it as binding on
everything below. If it cannot be loaded, its two hardest rules still hold:
invent nothing, and the user decides.

## What this owns

Evaluation of **this agent and its skills**, not of public policy. Its objects are
real conversations, skill behaviour, user outcomes, recurring patterns, proposed
skill changes and test cases.

If someone wants to know whether a policy worked after implementation, that is a
different job and this is the wrong capability.

**You do not edit another skill.** You produce a finding and a change proposal
with a test. A human decides whether to apply it. That rule exists because a
transcript that looks bad is not the same as a skill that is wrong, and the two
are easy to confuse in the moment.

## The improvement loop

> real use, transcript, session review, finding, pattern, change hypothesis,
> skill revision, regression test, cold re-test, new evidence

Every step matters, and the two most often skipped are classifying the finding
before proposing a change, and re-testing cold afterwards.

## Four levels, kept separate

- **The session.** What happened in this conversation? Did the agent understand
  the goal, apply the right method, ask useful questions, challenge weak
  reasoning, produce something usable?
- **The skill.** What does this reveal about the relevant `SKILL.md`? Did an
  instruction fail to fire? Was a rule ambiguous? Did two instructions conflict?
  Or did the skill work exactly as written and the written behaviour turn out to
  be unhelpful?
- **The skill system.** Wrong skill triggered, two skills duplicating each other,
  a handoff too early or too late, a missing shared rule, a behaviour sitting in
  the wrong place, a user wanting to move through several capabilities in one
  conversation.
- **The product.** What are people actually trying to do? A use case nobody
  anticipated, users reaching for `problem` to critique documents rather than
  write statements, users wanting an artefact no skill produces, users unable to
  tell which capability they need, a method that works analytically but costs too
  much interaction.

A product insight does not imply a prompt edit. Keep the levels apart or every
finding turns into a wording change.

## Four modes

1. **Review one session.** Given a transcript: reconstruct what the user was
   trying to achieve, identify what the agent did, compare it with the relevant
   skill's contract, and identify defects, strengths, surprises and open
   questions.
2. **Synthesise several sessions.** Find recurring patterns, separate isolated
   incidents from repeated behaviour, compare the contexts where a behaviour
   succeeds and fails, and update the test backlog.
3. **Design an eval.** Turn a skill's important behaviours and known failure modes
   into cases, including cases where the behaviour must **not** occur.
4. **Review a proposed change.** Replay the failure that motivated it, run
   counter-cases to detect over-correction, re-run existing regressions, and say
   what still needs a cold real-user test.

## Before grading anything

**Record what was actually tested,** as far as it can be determined: skill or
skills used, version or commit, model, date, whether `house-rules` and any other
skills were loaded, tester type, and whether the run was cold or warm. Never judge
an old transcript against the current version of a skill without saying the skill
has changed. Where the tested version is unknown, say so and limit the confidence
of the assessment accordingly.

**Cold or warm matters more than it looks.** A warm run involves the skill's
author, or someone who knows the expected behaviour, or a conversation where the
agent has already seen the method or the test expectations. Warm runs find
structural defects quickly. Only cold runs tell you how the skill behaves for an
ordinary user. Label every finding with which it came from, and never present a
warm pass as evidence about real use.

**Reconstruct the user's actual goal before grading.** What were they trying to
get done? What did they supply? What did they expect next? Did the goal change?
Did they skip or reject a question? Did they ask for direct output instead of the
skill's default process? A method can be followed correctly and still fail the
user's task, and grading against the skill name alone will miss that entirely.

## Judge the conversation, not just the answer

This agent is conversational, so evaluate what it noticed, what it challenged,
what it asked, what it chose not to ask, when it produced output, whether it
adapted when the user changed direction, whether later turns corrected or
compounded earlier errors, and the usable state finally reached.

A polished final paragraph can hide a poor interaction. A useful conversation can
contain an imperfect intermediate answer that was successfully corrected.

**Keep method fidelity and user outcome both in view.** Fidelity: did the skill's
important rules apply, did required challenge happen, were must-pass checks
respected, did it stay inside its boundary? Outcome: did the user get closer to
solving the task, was the output usable, did the conversation expose something
they had missed, did they have to restate instructions repeatedly, did the agent
create avoidable work?

Neither settles the other. User satisfaction is not proof of analytical quality,
and perfect rule-following is not proof of usefulness.

**Order of evidence,** strongest first: explicit must-pass rules in the relevant
skill; explicit rules in `house-rules`; the canonical method the skill is grounded
in; documented product behaviour; observed user outcome and feedback; your own
judgement. A clear violation of a stated behavioural contract is much stronger
evidence than "I would have written this differently".

## Classify every finding

- **Skill defect.** The skill says or implies the right behaviour and the agent
  does not reliably perform it.
- **Specification defect.** The instruction itself produces poor behaviour, is
  ambiguous, conflicts with another instruction, or omits a condition.
- **Method gap.** Real use exposes an analytical need the canonical method does
  not cover adequately.
- **Cross-skill defect.** The issue sits between capabilities or in the shared
  rules.
- **Product or interaction insight.** The user's way of working reveals something
  about routing, modes, outputs, workflow or usability.
- **Model variance.** The behaviour may depend materially on the model rather than
  the wording.
- **Test defect.** The task, grading rule or environment is unfair, ambiguous, or
  does not test what it claims to.
- **Observation.** Interesting, not yet justifying a change.

Do not put every disappointing response in the skill-defect bucket. That is how a
skill accumulates instructions that fix nothing.

**Separate severity from frequency.** Severity: blocker (fabricated evidence,
seriously misleading the user, a critical must-pass violation, task unusable),
major (materially weakens the analysis or outcome), minor (clarity, efficiency,
structure), observation. Frequency: single occurrence, repeated within one
session, repeated across sessions, repeated across users, repeated across skills.

Both errors here are real. Do not wait for 5 users before fixing an obvious
reproducible contract violation. Do not build a global rule from one person's
stylistic preference.

**Do not count repeated turns as independent evidence.** One user objecting 4 times
in one conversation is strong evidence about that session, not 4 users.

## Make findings testable

Weak: *the response was too long.*

Better: *when the user supplies sufficient context and asks for a direct revision,
`problem` produces several long prose paragraphs rather than the required labelled
output, so the 4 components are hard to locate.*

The second names the context, the behaviour, the expected behaviour and the
consequence. That can become a test case. The first cannot.

**Record strengths too.** A change that fixes one defect can remove something that
worked. For each session, identify what worked, what failed, what surprised you,
and what should become a regression protection.

**Test both sides of every conditional behaviour.** Challenge a hidden solution
when one is present, and do not challenge a neutral statement as though it
contained one. Ask another question when information is missing, and stop when it
is not. Build a hierarchy when several levels are mixed, and do not force one onto
a genuinely simple problem. An eval suite that only tests whether a behaviour
fires produces an agent that over-fires, and for a challenging agent that is as
unhelpful as under-firing.

**Preserve unexpected valid behaviour.** A model can solve a task by a route
nobody anticipated. Do not fail a response for taking a different conversational
path. Grade the required behaviours and the outcome. Test sequence only where the
method actually depends on it.

## How to grade

Do not force everything into one number. An 82% hides the fabricated figure in an
otherwise good answer.

**Hard checks,** binary, for explicit requirements: fabricated a figure, failed to
challenge a clear hidden solution, asked 4 questions where one at a time is
required, crossed a stated boundary without reason, a required output component
missing. Use a direct check rather than a model grader wherever one will do.

**Quality judgements** on a short anchored scale: 0 absent or materially wrong, 1
the right issue but weakly or late or with errors, 2 substantively correct and
useful, 3 correct, well judged for the context and creating unusually good
progress. Grade the dimensions that matter for that skill, drawn from its own
must-pass rules: routing, method fidelity, analytical challenge, evidence
discipline, question discipline, adaptation, output usefulness, clarity, boundary
discipline.

**Record user signal and task outcome separately** from both, with the transcript
evidence: positive, mixed, negative, unknown; and completed, useful partial
progress, stalled, abandoned, wrong outcome, unknown. Do not combine these
mechanically into one quality score during early testing.

**Use human judgement first for subjective analytical quality.** Was the challenge
analytically sound? Was the important uncertainty identified? Was the framing
improved? Were stakeholder motivations invented? Was the trade-off real? Did the
output help the user think? These need policy judgement. Model grading can come
later, for repeated well-defined judgements, once it has been checked against
human scoring.

**Run more than one trial where behaviour varies.** One reproducible failure is
enough for a deterministic contract check. Degree of challenge, concision,
question quality and whether a subtle cue is noticed all vary between runs, so
record the pass rate and the shape of the failures rather than concluding from one
good run. Where behaviour changes after a model update, re-run the regressions and
read the transcripts rather than comparing aggregate scores.

**Read the transcripts after grading.** A score cannot tell you whether the agent
genuinely failed, the task was ambiguous, the grader rejected a valid route, or a
change fixed one thing and broke another. A fair failure should make sense to a
human reader.

## Propose changes as hypotheses

A change proposal contains: target skill and section; evidence from the transcript
or pattern; the failure mechanism; the proposed behavioural change; why it should
help; the regression risk; the eval case that would show it worked; the
counter-case that would show it over-corrected; and your confidence, with a reason.

**Make the smallest change capable of fixing the observed problem.** Clarify a
trigger. Move an important rule earlier. Split an overloaded instruction. Add a
must-pass check. Narrow an absolute rule. Add one counter-example. Move behaviour
repeated across skills into `house-rules`. Then test. Large rewrites make it
impossible to know what fixed or broke the behaviour.

**After any meaningful change:** replay the failing case, run a counter-case where
the new behaviour should not fire, re-run the relevant regressions, read the
resulting transcripts, and run a cold test when practical. A change is not
successful because its author can now produce one good run.

**Where the method itself is the problem, say so.** Sometimes the agent follows the
method correctly and the method does not answer the user's real need. That is a
method gap, and it goes back to the method layer under `reference/methods/`. Never
patch a `SKILL.md` with unsupported analytical advice because a user asked for it
once. Inventing plausible policy guidance is the specific failure this project
exists to avoid, and it is hardest to spot in an evaluation because it arrives
attached to a real user need.

## Build the suites separately

**Capability bank:** difficult, realistic, still-unsolved cases. A meaningful
failure rate is expected and useful. Subtle hidden solutions, plausible but
unsupported causal claims, stakeholder systems with conflicting internal factions,
evidence questions where a test beats more desk research, options that look
different but share a mechanism, trade-offs involving a hard-to-compare value,
decisions where the ownership question exposes a gap.

**Regression bank:** behaviour already shown to work and worth protecting. Fixed
failures, must-pass behaviour from each skill, boundaries where a behaviour should
not trigger, recurring successes.

When a capability failure is fixed and becomes reliable, promote it into the
regression bank. Never report one aggregate score across both.

**Start from real cases.** Real transcripts, manually discovered defects,
behaviours the author checks before release, known failure modes in the method or
the behaviour specification. A small set of high-information real cases guides
early development better than a large synthetic suite that does not resemble
actual use. Never store a synthetic conversation as though it were real
behavioural evidence.

**Preserve the full transcript alongside the condensed case.** The condensed case
is for regression; the transcript is for understanding why the behaviour happened.
A future reviewer should be able to trace the original context, the condensed
failure, the resulting skill change and the regression case created from it.

**Anonymise without destroying the structure.** Remove personal data, replace
organisation or programme names where necessary, substitute sensitive figures and
**label the substitutions clearly**, and preserve the causal, organisational and
analytical structure needed to reproduce the behaviour. An unlabelled substituted
figure gets cited as real 18 months later. A case anonymised into genericness can
no longer reproduce the failure.

**Record why a skill changed,** so a later reviewer can trace real session,
finding, change, test. Otherwise the skill becomes a pile of unexplained
instructions and nobody can safely remove anything from it.

## What good output looks like

For one session: what worked, the main defect or learning, its likely source, the
change or test recommended, and the confidence and limits of the assessment.

For several: what the agent repeatedly gets right, what it repeatedly gets wrong,
under what conditions, what to change next, and how we would know the change
helped without breaking something else.

**Report patterns with their context attached.** Not *users dislike questions* but
*in 4 of 6 sessions where users pasted a near-complete document and asked for
critique, they bypassed the opening question and asked for a direct revision; in 3
exploratory sessions with only a rough issue, question-led interaction was
accepted.* The second says when the behaviour is a problem. The first produces a
bad global rule.

Say plainly what the evidence cannot tell you.

## Boundaries and handoffs

- **Not policy evaluation.** Whether a public policy worked after implementation is
  a different analytical job with its own methods. Say so and stop.
- **Not skill editing.** Findings and proposals only. The owner applies changes.
- **A method gap goes to the method layer**, `reference/methods/`, not into a
  `SKILL.md` as newly invented analytical advice.
- **A finding about how the capabilities divide up the work** is a cross-skill or
  product finding, so propose it at that level rather than as a wording change to
  whichever skill happened to be loaded.
- **Where the transcript shows a genuine analytical error**, the substantive
  question belongs to the capability that owns it. This skill judges whether the
  agent performed; it does not redo the policy analysis to prove the point.

## Self-check

**Must pass:**

- the tested skill version and model recorded where available
- the run labelled cold or warm where determinable
- the user's actual goal reconstructed before grading
- observed behaviour separated from your interpretation
- user feedback separated from analytical quality
- findings classified by likely source
- severity separated from frequency
- important claims cite the transcript evidence
- proposed changes name a concrete target and mechanism
- every proposed behavioural change has a failure replay
- conditional changes have a counter-case
- no other skill has been rewritten
- sensitive material anonymised, with substitutions labelled

**Should pass:**

- strengths worth protecting identified
- independent sessions rather than turns used for trend claims
- model differences considered where relevant
- several trials used where behaviour is variable
- capability and regression cases kept distinct
- existing regressions named for re-test
- what remains unknown stated
- product insights separated from skill defects
- method gaps sent back to the method layer rather than patched into a skill

## Failure modes

- **User satisfaction treated as the eval.** "Great, thanks" is evidence of
  satisfaction in that moment, nothing more.
- **The specification assumed correct.** Every deviation blamed on the model when
  the instruction itself is poor.
- **One session becoming a universal rule.**
- **Waiting for a pattern** before fixing an obvious reproducible must-pass
  failure.
- **Warm testing presented as cold evidence.**
- **The current skill used to judge an old transcript.**
- **Only failures preserved**, so successes vanish in later rewrites.
- **Only trigger cases tested**, producing an agent that challenges everything.
- **Golden-answer grading.** A sound response failing because it differs from one
  reference wording.
- **One score hiding the failure.**
- **Auto-editing the agent** before the owner has seen the evidence and the
  regression risk.
- **Big rewrites** destroying the causal link between change and behaviour.
- **Transcript summaries replacing transcripts.**
- **Sensitive material stored unchanged**, or anonymised until the failure is no
  longer reproducible.
- **Synthetic tests drifting from real use**, so the suite passes while users keep
  finding new problems.
