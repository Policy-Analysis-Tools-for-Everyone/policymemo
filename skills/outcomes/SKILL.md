---
name: outcomes
description: >
  Use when the question is what would actually happen: projecting the likely
  effects of a course of action, working out how large an effect would be and
  how quickly, comparing an option against what would happen anyway, or testing
  whether a forecast holds up. Also use when a proposal is being described in
  terms of its intentions rather than its consequences, when "will reduce
  demand" appears with no magnitude or timescale, when a precise-looking figure
  rests on a guess, when the base case is today frozen in time, or when everyone
  else in the system is assumed to carry on behaving exactly as before.
license: "CC BY-NC 4.0. policymemo.ai by Jack Strachan, https://policymemo.ai"
metadata:
  version: 0.2.1
  status: written, exercised inside other sessions and in 1 reported run; no session of its own
---

<!--
Canonical method:
  reference/methods/capabilities/outcomes-guidance.md
  - projection rather than intention, causal pathways, initial conditions, base
    cases, direction, magnitude, ranges, break-even and switchpoints,
    sensitivity, adverse implementation scenarios, foreseeable side effects and
    the outcomes matrix. Provenance: Bardach Step Five.

Distilled shared behaviour carried here:
  reference/methods/shared/risk-opportunity-appraisal-guidance.md - the outside
    view and reference classes, systematic optimism, the distinction between
    estimate uncertainty and model uncertainty, false precision, feedbacks, path
    dependence, pace and accumulation, option interaction. The rest of the
    appraisal method, including the appraisal gate and the decision record,
    stays in the file and belongs to `criteria` and `decide`.
  reference/methods/shared/uncertainty-and-learning-guidance.md - one rule
    only: turn a decision-sensitive forecast that cannot responsibly be made
    into a learning question. Designing the learning move belongs to `evidence`.

Not grounded:
  - Nothing beyond the files above.
-->

# Outcomes

Load `house-rules` before anything else here, and treat it as binding on
everything below. If it cannot be loaded, its two hardest rules still hold:
invent nothing, and the user decides.

## What this owns

What each serious option is expected to cause: compared with what, through what
mechanism, in what direction, at what magnitude and pace, with what uncertainty.

The job is to make the future **explicit enough to challenge**. It stops before
deciding how competing outcomes should be traded.

## Project outcomes, not intentions

For every serious option, the question is: **if we did this, what would probably
happen?**

None of the following is an answer: a description of the programme, a statement of
the objective, evidence that the problem exists, evidence that a similar
intervention exists somewhere, or a positive label.

A rapid-response service does not establish rapid response. A prevention
programme does not establish fewer future cases. Strip the intended success out of
the option's name, then project the effect.

**Treat every statement about the future as a claim.** Mark what is observed,
inferred, assumed, estimated and uncertain. Being marginally more likely than not
does not justify writing "will".

## Write the causal pathway

A projection has to answer: what has to happen between the intervention and the
outcome?

> Confirmation message sent, user sees it, uncertainty about receipt falls, fewer
> reassurance contacts, contact demand falls.

Then ask which links are evidenced, which are assumptions, and which actor
responses could break the chain. A projection with no visible pathway cannot be
challenged, which is the whole point of writing one.

Use whichever model the consequence requires: behaviour, organisational process,
incentives, markets, political response, implementation, technology. Do not
protect analytical neatness by ignoring a material effect.

## Anchor it in reality

**Record the starting conditions.** The same intervention behaves differently
under different baseline demand, staffing, institutional rules, current behaviour,
political support, technical capability, existing trends, relationships and
capacity. Never transplant an effect from another setting without asking where
this setting differs.

**Project the base case.** Business-as-usual is not today frozen in time. Project
current policy, existing trends, known external change and likely ongoing
implementation, then isolate what changes because of the alternative. Comparing an
option against today rather than against the likely future without it is one of
the most common ways a projection overstates the effect.

**State direction, magnitude and time for each decision-relevant outcome.**
Direction: increase, decrease, no material change, unclear. Magnitude: how much.
Time: when the effect appears and over what period. For structural change, also
pace: two options can reach similar end states while only one moves fast enough to
matter.

**Use a range where a point estimate overstates knowledge:** best current
estimate, plausible range, and the assumptions driving the range. Do not use a
huge range to avoid judgement, and do not use one precise number because a
spreadsheet wants one.

## Challenge the forecast

**Take the outside view.** Where a credible reference class exists, ask what
actually happened in comparable interventions: cost, duration, uptake, delivery,
benefit, failure. Then ask why this case should differ. A detailed plan is not
evidence that this team is exceptional. Never invent a reference class, and say
why the chosen cases are comparable.

**Look for systematic optimism.** Have similar forecasts historically been too
optimistic? Does approval depend on favourable numbers? Is the forecaster invested
in the option? Is there independent challenge? Accuse nobody of misrepresentation
without evidence, but do not ignore the incentives around the forecast. Systematic
bias compounds where random error partly cancels, so a wider symmetric error bar
is not the fix for a one-directional problem.

**Separate estimate uncertainty from model uncertainty.** A statistical range
describes variation inside a model. It says nothing about whether the causal model
is wrong, whether the context changes, whether behaviour adapts, whether a
feedback appears, or whether the policy alters the system it is forecasting. State
what the range actually represents.

**Match precision to knowledge.** Do not report a precise-looking forecast where
key inputs are guesses, one assumption dominates, comparable cases vary widely, or
the model is fragile. A calibrated range or an explicit qualitative statement is
more honest and more useful.

## Project dynamic effects where they matter

**Feedbacks.** What reinforces the effect, and what counteracts it? Does success
make further success easier? Does demand rise as the service improves? Does scale
reduce unit cost? Does opposition grow as impact becomes visible? Do not assume
linear effects where the mechanism suggests feedback, and do not assume doubling
an intervention doubles the effect.

**Path dependence and lock-in.** What becomes easier later if we choose this, and
what becomes harder? Does it lock in a technology, supplier, institution or
behaviour? Does it preserve future choices? These are outcomes too, and for a
long-lived decision they can matter more than the first-year effect.

**Option interaction.** Where policies are complementary or conflicting, project
each alone, the relevant package, and the sequence if order matters. The total
effect of A plus B is not the sum of their isolated effects.

**Systemic effects,** where the policy changes wider relationships or
capabilities: spillovers, crowding out, new capability, dependencies, resilience,
wider adoption. Keep only those with a plausible mechanism. "Systemic" is not
decoration.

**Thresholds.** Sometimes a large intervention has little effect and a small one
has a large effect. Is there a threshold, bottleneck or sensitive point? Does this
option need a minimum scale before the feedbacks change? Is it below the level
required to alter how the system behaves?

## Test uncertainty and failure

**Break-even reasoning** converts an unanswerable question into an answerable
one. Instead of *will it work?*, ask **how well does it need to work before it is
worth doing?** What minimum effect would make this worthwhile, what would have to
happen to reach that effect, and how plausible is that level?

**Switchpoints.** Where one uncertain quantity drives the choice, find the value
at which the preferred option changes: uptake, unit cost, participation, duration,
effect size. Then ask whether reality is plausibly above or below it.

**Sensitivity.** How wrong could this assumption be before the conclusion changes?
Prioritise the assumptions with the smallest margin for error, and do not spend
equal effort refining uncertainties that cannot change the answer. Where several
uncertain assumptions matter together, one-at-a-time testing misses the
interaction: use scenarios or combined sensitivity, without adding technical
modelling for appearance.

**Write an adverse implementation scenario.** Imagine it is several years later
and the policy has underperformed. Work backwards. Delay, cost growth, lower
uptake, administrative complexity, capture, weak compliance, political erosion,
capacity overload, fraud, standard procedures quietly defeating the design. This
exposes the assumptions the main forecast treats too kindly.

**Project foreseeable side effects.** Gaming, moral hazard, substitution,
displacement, benefit capture, burden shifting, workarounds, changed incentives.
Include material harms in the projection. An effect that was foreseeable is not
"unanticipated" when it arrives.

**Put yourself in other actors' position.** The policy changes constraints and
incentives, so people may comply, resist, substitute, avoid, game, adapt or
reorganise. Never forecast as though everyone else stays static.

## When projection becomes a learning problem

If the most decision-sensitive projection rests on a weak assumption that could
realistically be tested, stop and ask whether we need to learn before pretending
to forecast this. Unclear user behaviour, unknown uptake, uncertain operational
feasibility, an untested mechanism, transfer from a very different context.

Then say what the learning question is, rather than inventing a central estimate.
Some uncertainty is best represented as a range. Some can be cheaply reduced
through observation, interviews, a prototype, a live test or administrative
analysis. Some cannot be resolved before acting. **Turning an ungrounded
decision-sensitive forecast into a learning question is a result, not a failure to
deliver.** Inventing the number to fill the cell is the failure.

## What good output looks like

> `[option]` is expected to produce `[outcome]` of roughly `[magnitude or range]`
> over `[time]` compared with `[base case]`, because `[mechanism]`. The estimate
> rests on `[evidence or reference class]`, depends most on `[assumption]`, and
> would change materially if `[switchpoint or uncertainty]`.

Where several options and criteria are in play, an outcomes matrix with
alternatives as rows and criteria as columns can help. Two rules make it worth
having. Each cell holds the projected outcome, not a symbol: *8 to 12% reduction
in repeat contact over 12 months, high uncertainty from uptake* beats `++`. And
column labels are directional: *increase successful access among eligible
households*, not *access*. Order criteria by importance where exact weights are
unjustified, so one column each does not imply equal weight.

The matrix is a working tool, not the analysis. Revise it when evidence, options,
criteria or forecasts change.

## Boundaries and handoffs

Continue the work; do not announce a handoff.

- A decision-sensitive assumption could be reduced through evidence or a test, so
  the next move is a learning question, which belongs to `evidence`.
- The evidentiary basis of a projection is weak or disputed, or assumptions are
  being treated as facts, so go to `evidence`.
- The projections are good enough, so the next question is what is gained and given
  up, which is `trade-offs`.
- Projection shows every option performs poorly, so go back to `options`. Do not
  keep projecting a menu that cannot produce an acceptable outcome.
- A criterion turns out to be unmeasurable or wrongly specified, so go back to
  `criteria`.

## Self-check

**Must pass:**

- serious alternatives have projected consequences, not only intentions
- the base case is explicit and is not today frozen in time
- important projections have a visible causal pathway
- evidence and assumptions are distinguishable
- direction, magnitude and time stated where reasonably possible
- precision does not exceed the knowledge
- material uncertainty remains visible
- foreseeable implementation failure and side effects considered
- the preferred option has not been given systematically kinder assumptions
- a decision-sensitive projection that is too weak has become a learning question
  rather than an invented estimate

**Should pass:**

- a relevant reference class used where one exists
- feedbacks and path dependence considered where material
- option interaction considered
- break-even or switchpoint analysis used where useful
- sensitivity has identified the assumptions that matter most
- the matrix, where used, carries informative projections rather than symbols

## Failure modes

- **Intervention equals outcome.** "Create service" becoming "service improves
  outcome".
- **Direction without magnitude.** "Will reduce demand."
- **Precise forecast from weak assumptions.**
- **Inside view only.** The forecast resting entirely on the current plan.
- **Frozen base case.**
- **Linear forecast of a dynamic system.**
- **Passive actors.** Incentives changed, behaviour assumed unchanged.
- **Foreseeable harm arriving later as a surprise.**
- **Uncertainty disappearing into the matrix**, where a wide range becomes one
  score.
- **Guessing instead of learning**, where a small test could resolve the critical
  uncertainty.
- **Deciding.** Projecting the outcomes is not choosing between them.
