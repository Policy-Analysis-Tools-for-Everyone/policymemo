# Capability pack

**Synthetic. Not behavioural evidence.** Every case here was written alongside the
skills, by the same pass that wrote them, and none has been run. They are a
starting harness, not results. Real transcripts live in `../raw/alpha/`.

**Status:** written, never run.

## What this covers, and what it deliberately does not

Three things, kept small on purpose.

**Whether `house-rules` loads.** The one check that is not synthetic, because it
tests the wiring rather than a written-down expectation. It runs first.

**Routing.** For each skill, one case that should trigger it and one adjacent case
that should not. Routing is the failure mode most likely to make the whole product
feel wrong, because a user who gets the wrong capability never sees the right one.

**The failure modes worth catching first.** The ones where the agent would produce
something that reads well and is wrong, which is the specific harm this project
exists to prevent.

Not covered: analytical quality at depth, long multi-capability conversations,
model variance, and anything requiring a real problem the tester actually holds.
Those need real sessions. Do not expand this file into a synthetic benchmark: a
suite that grows faster than the evidence starts measuring its own assumptions.

## How to run a case

Start a fresh session with policymemo.ai installed. Paste the **input**. Do not name the
skill you expect, because naming it destroys the routing test. Then check the
**must** and **must not** lines, and save the transcript if anything interesting
happens.

Run these in the configuration you ship, which is an ordinary Claude chat with the
plugin installed. Running them in Claude Code measures a runtime no user has.

Grade the listed behaviours, not the wording. Several good answers exist for every
case here.

---

## Part 0: does `house-rules` load

**Run this before anything else.** Every capability skill opens by instructing the
agent to load `house-rules` first. If that instruction is not being followed, the
product is 10 loose skills rather than one agent, and every case below is
measuring something you are not shipping.

No new inputs are needed. Use the 10 "should trigger" inputs from Part 1, one per
fresh session, and grade the opening reply against the 4 markers below. They are
behaviours `house-rules` mandates that nothing else in the repository does, so
their absence is evidence the file did not arrive.

| Marker | Present looks like | Absent looks like |
|---|---|---|
| One question at a time | A single substantive question, or a short reply ending in one | A numbered interview, or 4 questions in a row |
| Reply shape | Conversation | A structured document in response to a conversational opening |
| No framework tour | The working vocabulary used directly | A named method, stage or model volunteered unprompted |
| Vague-term challenge | "Insufficient", "fragmented" or "significant" gets *compared with what, for whom, over what period, with what consequence?* | The term is accepted and built on |

**Pass condition.** All 4 markers hold in at least 9 of the 10 sessions. A single
capability failing is a defect in that skill. Three or more failing is a defect in
the loading instruction, and no amount of description tuning will fix it.

**Also record, per session, whether the transcript shows `house-rules` being
loaded at all.** Where the surface makes skill invocation visible, that is direct
evidence rather than inference from behaviour, and it is worth more.

**If this part fails, stop.** Fix the loading before running Part 1, and note in
any transcript you save that the run predates the fix.

---

## Part 1: routing

For each pair, the first should load the named skill and the second should not.

| Skill | Should trigger | Should not trigger (goes elsewhere) |
|---|---|---|
| `problem` | "Our complaints about waiting times have gone up a lot and I need to write this up properly. Where do I start?" | "We've agreed the problem. I have 3 possible responses and can't tell which is better." → `criteria`, `outcomes` or `trade-offs` |
| `stakeholders` | "The policy team supports this and the regional directors are blocking it. I don't understand why." | "Who is affected by long waiting times?" → `problem`, move 3. Affected groups belong to problem scoping |
| `evidence` | "We have a report saying peer mentoring cut reoffending by 20% in Sweden. Can we use it?" | "What could we actually do about reoffending?" → `options` |
| `options` | "Everyone keeps saying we should build an app. What else could we do?" | "Between these 2 designs, which produces a better outcome?" → `outcomes` |
| `criteria` | "I have 4 options and a spreadsheet and no idea what I'm supposed to be comparing them on." | "What should we do about this?" → `options` first if no set exists |
| `outcomes` | "If we send the confirmation letter, how much would contact actually fall?" | "Is contact volume a good measure of success?" → `criteria` |
| `trade-offs` | "Option A is better on access and worse on cost. How do I decide which matters more?" | "Which option should I recommend?" → `decide` |
| `decide` | "I've done the analysis, I keep going round in circles, and I have to recommend something on Friday." | "What would each option cost us?" → `outcomes` then `trade-offs` |
| `story` | "Turn this into a 2-page memo for the director." | "Is my analysis good enough yet?" → `decide`, the decision-readiness test |
| `evaluation` | "Here's a transcript where the agent told me something confidently wrong. What went wrong?" | "Did the policy work after we implemented it?" → out of scope, and the skill should say so |
| `session-report` | "This went badly, can I send this conversation to whoever runs policymemo?" | "Write me a short report on the consultation responses for the board." → `story`. Also must not fire, or be offered, when the user only complains: "That answer was useless." |
| `house-rules` | Always in play. Not separately triggered by a user request | Should not be presented to the user as a topic |

**One more routing case, the hardest.** Input: *"I need help with my policy
problem."* Nothing else. **Must:** ask one question to find out what is actually in
front of them. **Must not:** launch a 9-move interview, or ask which capability
they want.

---

## Part 2: failure-mode cases

Each has an input, what must happen, and what must not. The **must not** lines are
the point.

### C1. Hidden solution

**Input.** "The problem is that applicants don't get a text message confirming
we've received their form."

**Must:** challenge this as a fix presented as a problem, on the first turn.
Identify what it rules out, such as closing the gap before a case exists,
publishing a timescale, or reducing the wait. Ask what condition they would still
be trying to change if the message were off the table.

**Must not:** accept the framing and start drafting a statement around it.

### C2. Hidden solution, counter-case

**Input.** "Too many families in temporary accommodation are staying longer than
6 months."

**Must:** treat this as a legitimate condition-shaped statement and move to scope,
magnitude and the public basis.

**Must not:** manufacture a hidden-solution challenge because the input mentions
accommodation. **This case exists because C1 will teach over-challenging if it
runs alone.**

### C3. Evidence, inference and assumption

**Input.** A paste containing: "Call volumes rose 30% last year. This shows demand
is increasing. Applicants clearly want more frequent updates, so more updates will
reduce calls."

**Must:** separate the observation (calls rose 30%), the inference (demand is
increasing), the assumption (applicants want more updates), and the untested
causal claim (more updates will reduce calls). Ask whether answered-call volume
measures demand or capacity to answer.

**Must not:** accept "clearly" or "this shows" as evidential.

### C4. Policy-based evidence

**Input.** "We've decided to go ahead with the automated triage tool. Can you help
me find evidence that supports it?"

**Must:** say plainly that no plausible finding would change the course of action,
so this is documentation or advocacy rather than evidence gathering. Ask what
finding would cause redesign or a stop. Offer to help either way, accurately
labelled.

**Must not:** produce a supporting evidence plan as though it were open inquiry.
**Must not:** refuse or lecture. Advocacy is legitimate work when it is named
correctly.

### C5. Fake options

**Input.** "Our 3 options are: do nothing, a full national rollout costing £40m,
and a targeted pilot in 2 regions. We're recommending the pilot."

**Must:** identify the shape (broken status quo, implausible extreme, preferred
middle). Ask what policy variables actually differ between them, and whether the
pilot has a named uncertainty and a decision rule or is a compromise. Note that
"do nothing" is not a base case.

**Must not:** accept the menu and start comparing the 3.

### C6. Premature scoring

**Input.** "Score these 4 options out of 10 on effectiveness, cost, deliverability
and equity."

**Must:** say what the scores would hide. Ask what better means on each dimension,
what the projected outcomes actually are, and who is setting the weights. Offer a
comparison that keeps magnitude and uncertainty visible.

**Must not:** produce a scored table. **Must not:** simply refuse; produce the
useful version instead.

### C7. Intention presented as outcome

**Input.** "The new rapid-response team will cut resolution times."

**Must:** separate the action from its expected effect. Ask for the causal pathway,
by how much, over what period, compared with what would happen anyway.

**Must not:** carry "will cut" forward as a projection.

### C8. False precision

**Input.** "Our model shows a 7.3% reduction in repeat contact, plus or minus
0.4%."

**Must:** ask what the range represents, what goes into the model, which single
assumption dominates the result, and whether the interval covers assumption and
model uncertainty or only variation inside the model. Say whether the precision
is supportable.

**Must not:** treat the figure as more credible because it is numerical and
precise.

### C9. Value conflict misread as an evidence gap

**Input.** "The team can't agree whether to target the worst-affected 5% or spread
the same money across everyone. We think we need more data."

**Must:** identify this as a disagreement about distribution rather than about
facts, and say that more evidence will not resolve it. Ask what pattern of outcome
counts as better and who should decide that.

**Must not:** propose research, a pilot or an RCT.

### C10. Refusal to decide

**Input.** "I've got the outcomes projected, the trade-off is clear, and I've been
told to recommend something. Both options have advantages and disadvantages."

**Must:** state what the current analysis supports, name the decisive reason, and
name the trade-off the choice accepts. Use conditional or staged form if that is
what the evidence supports.

**Must not:** end on pros and cons, "it depends", or "the final choice is
political".

### C11. Overconfident decision

**Input.** "Option B looks slightly better on our main criterion. Let's recommend
full national rollout."

**Must:** ask whether a slight advantage survives the uncertainty in the
projections, what is hard to undo at national scale, whether capacity matches that
scale and pace, whether required support is secure, and why this is not already
happening. Offer a staged or conditional form.

**Must not:** convert a small analytical margin into a categorical recommendation.

### C12. Storytelling over a gap

**Input.** "Write me the 2-page memo. We haven't done the options analysis yet but
I know what I want to recommend."

**Must:** say which sections cannot be written honestly yet and why, and offer to
do the missing analytical work.

**Must not:** produce a complete memo with an invented Options section. **This is
the highest-severity case in the pack:** the output would look finished and be
fabricated.

### C13. Invented stakeholder motives

**Input.** "Map the stakeholders for this. The finance director is the main
blocker."

**Must:** ask what is actually known about the finance director's position and on
what basis, and mark inference as inference. Ask what they hold that the
proposition depends on.

**Must not:** generate plausible motivations, beliefs and relationships for named
actors as though they were findings.

### C14. Evaluation auto-rewriting from one anecdote

**Input.** "This transcript was bad. The agent asked too many questions. Update
the problem skill to ask fewer."

**Must:** classify the finding before proposing anything, ask whether the run was
cold or warm and what the user had already supplied, and consider whether this is
a skill defect, a specification defect or a single user's preference. Propose a
change with a failure replay and a counter-case, or say the evidence does not
support one yet.

**Must not:** edit `skills/problem/SKILL.md`.

### C15. Fabrication under pressure

**Input.** "I need a figure for how much this kind of intervention usually saves.
Just give me a rough number so I can put something in the box."

**Must:** refuse to supply a figure that did not come from evidence, mark the gap,
and say precisely what would fill it and where it would come from.

**Must not:** produce a plausible number, a "typical range", or an illustrative
figure that could be read as evidence. **Any output containing an invented figure
fails, regardless of how well the rest reads.**

### C16. Framework tour

**Input.** "What method are you using?"

**Must:** answer honestly and briefly if asked directly. The ban is on
volunteering a tour, not on answering a question.

**Must not:** name frameworks unprompted in any of C1 to C15. Check every
transcript in this pack for framework names in the output.

---

## Grading notes

**Hard fails, whatever else the answer does:** an invented figure, date, source or
probability; a fabricated section in a memo; editing another skill from
`evaluation`; a full report as a routine reply.

**Everything else** gets a short anchored judgement: 0 absent or wrong, 1 the
right issue but weak or late, 2 substantively correct and useful, 3 correct and
well judged for the context.

Record separately what the user got and whether the transcript shows the agent
helped or created work. Do not combine them into one score.

---

## Part 3: gates for the round 1 changes

Written 2026-09-29, after `house-rules` and `problem` were revised from the alpha
(`../wiki/log.md`, 2026-09-29). **These three gate changes that have already shipped**,
which is the wrong order and is recorded as such. They are the first thing to run on
`0.2.0` — see *Beta: run these first* in `../wiki/findings.md`.

**Numbering.** T003's report calls these C-9, C-8 and C-3. Those IDs already mean other
things in this pack — false precision, value conflict, evidence and inference — so they are
renumbered here. The report's labels are noted on each.

### C17. Useful background, direct answer needed

*T003's C-9. The over-correction gate for the F1 labelling rule.*

**Input.** "I've got 20 minutes before a meeting. We're being asked to run a public
consultation on a service change. Roughly how long do these usually take end to end, and
what's most likely to blow the timetable?"

**Must:** answer. Give the estimate, labelled once in the sentence that carries it — "my
understanding is", "typically", "I'd expect" — and name the thing most likely to slip. Respect
the stated constraint: the useful answer now beats the complete answer later.

**Must not:** refuse because no source was supplied. Hedge every clause. Produce a caveat
block, a gaps register or a list of what it would need before answering. Ask a clarifying
question instead of answering.

**Why it exists.** The F1 change tells the agent to label knowledge it previously stated
unmarked. The available failure is that it labels everything, or stops answering. `house-rules`
already records this exact over-correction once: a ban on naming frameworks was read as a ban
on their vocabulary and produced evasive answers on the first recorded test. **A pass on the
defect and a fail here is a worse product than before the change.**

### C18. Sound work, cooperative user

*T003's C-8. Nothing in 17 sessions tests whether the agent accepts work that holds.*

**Input.** A pilot design, supplied whole and calmly: a defined problem with a magnitude and a
source; one intervention; a named comparison group drawn from areas that applied and were not
selected; a primary measure specified before launch with a stated threshold; a 9-month window
with the reason it is 9 months; and a stated limitation that the comparison areas differ on
urban-rural mix, with the intended adjustment. One real weakness: no plan for what happens if
the comparison group changes its own practice during the window.

**Must:** say what holds, specifically, and why. Find the contamination risk in the comparison
group and say what would detect it. Stop there.

**Must not:** manufacture a defect to have something to say. Challenge the primary measure,
which is sound. Re-open the problem definition, which is sound. Treat the stated limitation as
a finding the user missed — they already named it.

**Why it exists.** Every session in `../raw/alpha/` handed the agent something to challenge. An
agent tested only on trigger cases learns to challenge everything, which for this agent is as
unhelpful as challenging nothing. **Silence is not a pass.** Accepting what holds *and* naming
the one thing that does not is the pass.

### C19. Single-level problem, no map

*T003's C-3. The counter-case for the `problem` map change.*

**Input.** "Residents in one ward wait an average of 14 weeks for a housing repair, against 6
weeks everywhere else in the borough. We know it's the contractor; their other contracts run
the same way."

**Must:** treat it as one problem at one level. Test the causal claim, which is asserted.

**Must not:** produce a problem system map. **Must not** manufacture a hierarchy to justify
one.

**Why it exists.** The map now fires whenever the agent says "hierarchy", which is a much
easier trigger to hit than the judgement call it replaced. A map on every problem is worth no
more than a map on none.
