---
name: stakeholders
description: >
  Use when the work turns on who is involved: who holds a problem, who must
  authorise or fund or cooperate with a response, who would be affected
  differently, why an actor is resisting, what power someone actually has, or
  who has to be brought on board and in what order. Also use when a claim about
  someone's motives, influence or position is being asserted without evidence,
  or when an organisation is being treated as though it had a single mind.
license: "CC BY-NC 4.0. policymemo.ai by Jack Strachan, https://policymemo.ai"
metadata:
  version: 0.2.1
  status: written, exercised in 1 reported run and 1 tester note; no session of its own
---

<!--
Canonical method:
  reference/methods/capabilities/stakeholder-analysis-guidance.md
  - the Actor / Motivations / Beliefs / Resources worksheet, positions versus
    interests, the eight power types, arena, the network layer, the dynamic
    political readout, the required-support check, anti-patterns and the
    self-check rubric. That file carries the full provenance: Bardach
    (Appendices C and D), Weimer & Vining, Getting to Yes, Mandell et al. on
    types of power, and Reinikainen on network mapping.

  Stakeholder analysis is deliberately a separate capability. It is not one of
  Bardach's steps, and the canonical method says so. It is here because the job
  is distinct: folding it into the political-support question would lose the
  affected groups who hold no power, and folding it into problem definition
  would lose the actor system entirely.

Not grounded:
  - The 6-actor pressure on the required-support list is an authoring
    judgement about proportionality, not a claim from any source.
-->

# Stakeholders

Load `house-rules` before anything else here, and treat it as binding on
everything below. If it cannot be loaded, its two hardest rules still hold:
invent nothing, and the user decides.

## What this owns

The actor system around a problem or proposal: who is involved, what they are
trying to achieve or protect, what they believe, what they can actually bring to
bear, where they can bring it to bear, how they are connected, and how that
picture could change.

It does not own whether the required support is sufficient for the proposition
to proceed, which is the final viability judgement in `decide`. It does not own
which option is best (`options`, `trade-offs`, `decide`) or what counts as public
value (`criteria`).

## Anchor it to something specific

A stakeholder is not simply someone important to the topic. Anchor the analysis
to a named problem, proposal, decision, change or implementation challenge.

The same actor may support the goal and oppose the means, support one framing and
resist another, or move as the proposal moves. If the object is vague, every
position in the map will be vague too. Fix the object first.

## The central artefact

For each serious actor, build this. Four columns, kept distinct.

| Actor | Motivations | Beliefs | Resources |
|---|---|---|---|
| individual, group, organisation or faction | what they are trying to achieve, protect, avoid, preserve or be seen to do | what they appear to believe about the problem, the proposal, the consequences, feasibility, fairness or other actors | what they can actually bring to bear, and where |

Everything else is an overlay. Keep current position, intensity, arena and
evidence status as short annotations or a separate short view, not as more
columns.

Three rules make the table worth building.

**A position is not a motivation.** "They oppose it, therefore their motivation
is opposition" is circular. A position is what they currently say should happen.
An interest is the need, fear, constraint or constituency that makes that
position make sense to them. Where the stated position does not explain the
behaviour, ask: why would this position serve them? What do they think saying yes
would mean? What do they think saying no would mean? Why have they not already
done what we want? Treat the answers as hypotheses until evidenced.

**Beliefs belong in the analysis even when they are wrong.** Behaviour follows
what an actor believes, not what is true. Record what they appear to believe,
what supports that assessment, and separately whether the belief itself is well
founded. Understanding a point of view is not endorsing it.

**Most actors have several motivations at once.** An elected official may care
about the outcome, constituents, party, re-election, reputation and a future
career. A civil servant may care about professional standards, workload,
implementation risk and organisational resources. Where it matters, ask which
motivation is likely to dominate in this decision and under these conditions.
Writing "Motivation: protect budget" where the evidence shows several competing
considerations is a false simplification.

## Make "power" concrete

Never leave "high power" standing as a score. Ask what the actor can actually
do here, and where they can do it.

Useful distinctions when influence is vague: formal authority from a role; the
ability to convene others and set an agenda; a veto or the ability to delay;
room to shift between acceptable positions without prohibitive cost; moral
suasion that reframes what the alternatives mean; nuisance, attention and
reputational pressure without formal authority; momentum, where the perception
that something is advancing pulls others in; and coalitional power, the ability
to mobilise allies and direct their resources. Votes, money, expertise,
information, professional standing, relationships and procedural control all
count too.

Do not force every category onto every actor. Name the resource that matters
here and the arena where it can be used, then ask the harder question: do they
have this power in theory, or are they willing and able to use it in this case?

**Keep position, intensity and influence separate.** A strongly opposed actor
with no ability to affect the outcome is a different problem from a mildly
sceptical actor with a veto. Collapsing them into one power-interest score
destroys the distinction the analysis exists to make.

## Identify the arena

Influence is exercised somewhere. Where will this decision actually be made? Who
has formal standing there? What are the written rules, and what unwritten
practices matter? Who controls the agenda and the timing? What counts as a
decision here: a vote, ministerial approval, a budget settlement, a procurement
award, operational consent?

Then ask whether the issue can be moved. Actors who expect to lose in one arena
often try to shift it to another. A resource only matters if it can be exercised
in an arena that is actually in play.

## Split organisations when it changes the analysis

"The Treasury", "the union", "the department", "the public" can each conceal
differences that matter: professional factions, ideological divisions, leadership
against front line, centre against local units, formal authority against
informal influence, different constituencies. Split the actor where those
differences could change what you conclude. Leave it whole where they would not.

## Include the people who have to make it work

A policy can be formally adopted and still fail because the people who must
enact it, cooperate with it or work around it do not behave as assumed. Front-line
staff, managers, co-producers, vendors, local delivery bodies, holders of tacit
knowledge, and control functions such as finance, legal, audit and procurement
can quietly slow, reshape, reinterpret or enable implementation.

Mapping only the people who can say yes is one of the most common ways a
stakeholder analysis misses the thing that actually kills the policy.

## The required-support check

Run this once something is being proposed rather than understood.

From the wider map, pull out the subset whose **authorisation, funding, legal
permission, operational cooperation, legitimacy or non-opposition** the
proposition depends on. For each:

> `[actor]` supplies `[what]`. Without it, `[what fails]`. Position:
> `[supportive / conditional / uncommitted / opposed / unknown]`. Basis:
> `[evidence / inference / unknown]`.

Three things keep it honest. **Required is not the same as affected**: an
obscure control function may hold a decisive veto while a badly affected group
holds nothing, and both belong in the analysis for different reasons. Never let
a short required-support list justify dropping affected groups who lack power.
**Non-opposition counts**: some actors never have to say yes, only to refrain
from saying no, briefing against it, or withdrawing something it depends on.
**Endorsing the purpose is not endorsing the delivery model**: where support
rests on a cheaper, faster or easier version than the one proposed, mark it
fragile and say what would expose it.

Keep this to the consequential few. Past about 6 actors, either the proposition
genuinely depends on an unusual number of consents, which is a finding worth
stating plainly, or the list has drifted back into general mapping.

## Relationships, in proportion

Organisation charts describe formal structure. Ask what is actually happening:
who talks to whom, who is trusted, who people go to for expertise, who
influences decisions without formal authority, who connects groups that are
structurally separated, where information and resources flow, and which
important relationships are missing.

State which relationship you are mapping. Communication, influence, decision
flow, expertise, coalition and cross-boundary contact are different maps and
combining them produces something unreadable.

What a relationship view can show that an actor table cannot: **boundary
spanners** already connecting silos, **brokers** through whom access or
information passes, **clusters** more connected internally than outward,
**bottlenecks** where too much routes through one actor, **single points of
failure**, and **missing links** between groups that should interact. An actor
can matter because of where they sit rather than what their title is.

Keep this light. A dense diagram that changes no decision is worse than three
sentences that do. Never turn a stakeholder conversation into technical network
analysis unless the user asks for it.

## Treat the picture as dynamic

A map is a snapshot. Support and opposition develop.

**Distinguish supporters from allies.** A supporter favours it. An ally will do
something useful: recruit others, open access, supply expertise or legitimacy,
provide resources, mobilise a constituency, neutralise an opponent. Passive
approval is not coalition capacity, and counting it as such is how a political
strategy fails on contact.

**Keep uncommitted actors visible.** Undecided, conditionally supportive, weakly
attached, waiting for evidence, waiting to see whether it is viable, hostile but
not mobilised, or capable of being neutralised without becoming a supporter.
These often determine whether a coalition reaches enough support.

**Ask what could change the map:** new evidence, reframing, participation in
design, changing political conditions, visible momentum, coalition growth, a new
relationship, a different arena, opponent mobilisation, implementation
experience, concessions, shifts in attention.

**Sequence where relationships compound.** The most powerful actor is rarely the
right first conversation. Ask who changes the odds of reaching the next
important actor, by validating feasibility, lending legitimacy, opening access,
recruiting allies or surfacing hidden opposition. Political resources are
spendable and some are depletable, so ask when a resource has most value rather
than using everything now.

**Treat concessions as substantive choices.** A concession can win one actor and
damage something else. What objective is being given up? Who benefits? Which
existing allies feel weakened? Does it set a precedent? Does it meet the
underlying interest, or just split positions? Movement towards agreement is not
automatically good.

## Mark what you actually know

"The minister will oppose this", "staff mainly care about workload", "the
regulator has enough influence to block it", "A trusts B", "this person is the
key broker" are all analytical claims. For anything important, mark the basis:
observed, reported by a source, inferred, hypothesis, or unknown.

Plausible-sounding psychology is the characteristic failure of this capability.
Motives and relationships are exactly the material an agent can generate
fluently and wrongly. Where a claim matters and the basis is inference, say so
and say what would test it: direct contact, observed behaviour, documents,
previous decisions, an informed intermediary.

## Boundaries and handoffs

Continue the work; do not announce a handoff.

- The question has become whether the required support is enough to proceed, and
  why it is absent where it is absent, so that is the final viability judgement
  in `decide`.
- An important motive, belief or relationship claim is inference doing the work
  of evidence, so go to `evidence`.
- The map exposes that the problem itself is contested between actors, so go back
  to `problem`.
- Actor resistance suggests a different design, such as changing who bears cost
  or which body delivers, so go to `options`.

## Self-check

**Must pass:**

- anchored to a specific problem, proposal, decision or implementation challenge
- important actors analysed for motivations, beliefs and resources, not merely
  named
- positions not mistaken for interests
- claims about motives, beliefs, power and relationships marked as evidenced,
  inferred or uncertain
- vague power judgements translated into actual resources and an arena
- implementation actors included where their behaviour affects success
- supporters distinguished from active allies
- where something is proposed, the actors whose support is required identified
  separately from the wider map

**Should pass:**

- internal factions separated where treating the organisation as one actor would
  mislead
- multiple motivations considered for important actors
- the decision arena identified where feasibility matters
- routes of influence considered rather than formal structure alone
- uncommitted and conditional actors visible
- sequencing, timing and change conditions considered
- affected groups without power still present

## Failure modes

- **A list of names.** Actors identified without saying why they matter.
- **Inventing motives and relationships.** Fluent psychology presented as
  finding.
- **"High power" with no content.** A score standing in for what someone can do.
- **A 2x2 grid treated as the analysis.** Motivations, beliefs, authority,
  informal influence, relationships and dynamics collapsed into two axes.
- **One organisation, one mind.** "The department supports it."
- **Hierarchy read as influence.** Assuming the most senior person is the one
  others listen to.
- **Mapping approval but not delivery.**
- **Dropping the powerless.** Being affected and being influential are different
  reasons to be in the analysis.
- **A static map.** Current positions reported as permanent properties of
  people.
- **Every supporter counted as an ally.**
- **Over-engineering the network.** A hairball diagram that changes nothing.
