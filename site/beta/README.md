# Beta access

How people get into the policymemo.ai private beta, and how one person runs it.

The website is the front door. It explains the beta and offers three routes:
UCL students use the study's Microsoft Form; other participating universities and
practitioners email `support_email`, with a prefilled request (subject and
questions are set in `build_beta` in `tools/build-site.py`). Add a practitioner
form later by setting `practitioner_form_url`. Nobody gets access by submitting a form. Jack reviews each request and
invites people in waves. The only thing that sends set-up instructions is
changing someone's status to `Invited`.

```
Microsoft Form (student or practitioner)
  → Power Automate flow 1: add a row to the beta list, send a "we've received it" email
  → Jack reviews the list and picks a wave
  → Jack sets Status to Invited
  → Power Automate flow 2: send the invite email once, record the date
```

This is a soft gate. The install page and the GitHub repository are public, so
anyone determined can install policymemo.ai without asking. The gate controls who
is invited, supported and asked for feedback, and how many people that is at once.

## What's in this folder

| File | What it is |
| --- | --- |
| `body.html` | The `/beta` page. Hand-written HTML, published by `tools/build-site.py` |
| `beta.css` | Styles for that page only |
| `config.json` | The links and contact details the page uses (below) |
| `README.md` | This guide |

## Configuration

Edit `site/beta/config.json` and push to `main`. The "Build site" workflow republishes
`/beta`.

| Key | Used for | If empty |
| --- | --- | --- |
| `student_form_url` | The UCL student card's Request access button | The card shows "Opening soon" |
| `practitioner_form_url` | Replaces the practitioner card's email button with a form | The card uses the prefilled email |
| `access_instructions_url` | "Already invited? Set-up instructions" on `/beta`. Use the same link in the invite emails | Not allowed |
| `support_email` | "Questions?" on `/beta`, and the address the university and practitioner email buttons write to. Use the same address as the reply-to in the emails | Not allowed |
| `privacy_url` | "How we use your information" on `/beta` | The link is left out |

URLs must start with `https://`. A Forms link comes from the form's **Collect
responses** button. The emails live in Power Automate, not in this repository. If
you change the instructions URL or the support email, change them in the flows too.

## Where to build it

Build the form, list and flows in one Microsoft 365 account, and decide which
account before you start:

- **UCL account.** Students sign in with it, so the student form can be
  restricted to UCL. Check two things first: that UCL lets your forms accept
  responses from anyone (practitioners need this), and that UCL is content to
  hold practitioners' details.
- **Your own Microsoft 365 account.** This keeps practitioners separate from the
  university. Student research data must still stay on UCL systems, so the student
  form would then sit in UCL and the practitioner form in your account. That means
  two lists. It's workable, but it doubles the setup.

The connectors used here (Forms, SharePoint, Outlook) are standard ones,
included in Microsoft 365 work and university licences. Nothing needs a premium
licence.

## The list

Use a **Microsoft List**, not an Excel workbook. Power Automate can act when a
List item changes. Its Excel connector has no trigger for a changed row, so
"set Invited, then send the email" can't be built on Excel. A List still has a
spreadsheet-style grid view for editing many rows at once.

Create one list, `policymemo beta`, with these columns. Create each column with
the name in the first column of this table, no spaces, then rename its display
name if you like. Power Automate refers to columns by the name they were created
with, and spaces become `_x0020_`.

| Column | Type | Set by | Notes |
| --- | --- | --- | --- |
| `Title` | Text (built in) | Flow 1 | The applicant's name. Lists requires this column |
| `Email` | Text | Flow 1 | |
| `Route` | Choice: `Student`, `Practitioner` | Flow 1 | Fixed per form |
| `Organisation` | Text | Flow 1 | University for students |
| `Role` | Text | Flow 1 | Role or type of policy work. Course for students |
| `UseCase` | Multiple lines | Flow 1 | What they'd like to try policymemo.ai on |
| `UpdatesOptIn` | Yes/No | Flow 1 | Only from the optional tick box. Default No |
| `Status` | Choice (below) | Flow 1, then Jack | Default `Applied` |
| `Wave` | Text | Jack | For example `Wave 1` |
| `AppliedOn` | Date | Flow 1 | |
| `InvitedOn` | Date | Flow 2 | Empty until the invite is sent. This stops it being sent twice |
| `Notes` | Multiple lines | Jack | Private |
| `ResponseId` | Text | Flow 1 | Links the row back to the form response |

**Statuses**

| Status | Meaning | Set by | Sends an email? |
| --- | --- | --- | --- |
| `Applied` | Request received | Flow 1 | Confirmation, from flow 1 |
| `Review` | Shortlisted, or being considered for the next wave | Jack | No |
| `Invited` | Invited in a wave | Jack | Invite, once, from flow 2 |
| `Active` | Set up and using it | Jack | No |
| `Feedback received` | Has sent at least one session report | Jack | No |
| `Declined / Not now` | Not in this round | Jack | No. Write personally if you want to |

Add two views: **To review** (Status is Applied or Review, oldest first) and
**This wave** (filtered on `Wave`).

**Keep research data out of the list.** For students the list holds operational
details only. Consent records stay in the student form's responses, and research
data is handled as the ethics approval says. The list is not the consent record.

## Forms

**Practitioner form** (Anyone can respond):

1. Name (required)
2. Email (required)
3. Organisation (required)
4. Your role, or the type of policy work you do (required)
5. What would you like to try policymemo.ai on? (required)
6. Keep me updated about policymemo.ai releases, research findings and future
   testing. (optional, one tick box)

Put this under the title: "We invite people in small groups. Sending this form
doesn't give you access straight away. We use your details to manage your beta
access, and only send other updates if you tick the last box."

**Student form** (only people in UCL can respond): the same operational
questions, plus whatever the ethics approval requires. Its consent design is out
of scope here. Keep question 6 separate from research consent, because agreeing
to take part in the study is not agreeing to receive product news.

## Flow 1: request received

Build one per form, because a flow has one trigger. Name them `Beta: practitioner
request` and `Beta: student request`.

1. **Trigger:** Microsoft Forms, *When a new response is submitted*. Choose the form.
2. **Microsoft Forms, Get response details.** Same form, with the trigger's Response Id.
3. **SharePoint, Create item.** Your site and the `policymemo beta` list.
   - Title, Email, Organisation, Role, UseCase: map from the answers
   - Route: `Practitioner` (or `Student` in the student flow)
   - UpdatesOptIn: `Yes` if the tick-box answer isn't empty, otherwise `No`
   - Status: `Applied`
   - AppliedOn: `utcNow()`
   - ResponseId: the trigger's Response Id
4. **Office 365 Outlook, Send an email (V2).** To: the Email answer. Use the
   confirmation template below.

## Flow 2: send the invite

One flow covers both routes. Name it `Beta: send invite`.

1. **Trigger:** SharePoint, *When an item is created or modified*, on `policymemo beta`.
   In the trigger's **Settings**, add two trigger conditions. Both must be true:
   ```
   @equals(triggerOutputs()?['body/Status/Value'], 'Invited')
   @empty(triggerOutputs()?['body/InvitedOn'])
   ```
   Without these, the flow runs on every edit and sends the invite repeatedly.
2. **Condition:** `Route Value` is equal to `Student`.
   - Yes: **Send an email (V2)** with the student invite.
   - No: **Send an email (V2)** with the practitioner invite.
3. **SharePoint, Update item.** Id: the trigger's ID. Title: the trigger's Title,
   which Lists requires. InvitedOn: `utcNow()`. Setting this date edits the item
   again, but the second trigger condition then stops the flow, so it can't loop.

**To resend an invite,** clear `InvitedOn` while Status is still `Invited`. That
edit runs flow 2 again.

## Running a wave

1. Open **To review**. Move the people you're considering to `Review`, and add notes.
2. Choose this wave. Size it by how many people you can support, not by demand.
3. In grid view, set `Wave` for those rows, then set Status to `Invited`. Flow 2
   sends each invite within a few minutes.
4. Check the flow's run history for failures.
5. Move people to `Active` and `Feedback received` as you hear from them. Use
   `Declined / Not now` for everyone else in this round.

Students usually go as one cohort. Set the whole group to `Invited` once their
consent is in place.

## The mailing list later

Beta access is not consent to a newsletter. Only rows where `UpdatesOptIn` is Yes
can go on a future policymemo.ai mailing list. Filter on that column, export to
CSV and import into whatever you choose then. Everyone else gets only operational
email about their access.

## Email templates

Plain text. Replace the `{…}` placeholders with dynamic content in Power Automate.

**Confirmation: practitioner**

> Subject: We've received your request for the policymemo.ai beta
>
> Hi {Title},
>
> Thanks for asking to try policymemo.ai. We've received your request.
>
> We're inviting people in small groups this autumn, so it may be a few weeks before
> you hear from us. If we can invite you, we'll email you set-up instructions.
> You don't need to do anything else.
>
> If you have a question, reply to this email.
>
> Jack Strachan
> policymemo.ai

**Confirmation: student**

> Subject: We've received your policymemo.ai beta form
>
> Hi {Title},
>
> Thanks for signing up. We've received your form.
>
> You'll be invited with the rest of your course group, and we'll email you
> set-up instructions then. You don't need to do anything else.
>
> If you have a question, reply to this email.
>
> Jack Strachan
> policymemo.ai

**Invite: practitioner**

> Subject: You're invited to the policymemo.ai beta
>
> Hi {Title},
>
> You're in. Set-up instructions are here: {access_instructions_url}
> It takes between 2 and 10 minutes, in Claude, Copilot or Gemini.
>
> Try it on what you told us about: "{UseCase}". It works best on something real.
>
> The most useful thing you can send us is a conversation where it was
> confidently wrong. Reply to this email, or use the session report:
> https://github.com/Policy-Analysis-Tools-for-Everyone/policymemo/issues/new?template=session-report.yml
>
> It's a beta, so expect rough edges. policymemo.ai runs inside your AI tool, under
> that tool's own terms, so don't put anything into it that you wouldn't put into
> the tool itself.
>
> Jack Strachan
> policymemo.ai

**Invite: student**

> Subject: Your policymemo.ai set-up instructions
>
> Hi {Title},
>
> You can now set up policymemo.ai: {access_instructions_url}
> It takes between 2 and 10 minutes, in Claude, Copilot or Gemini.
>
> To tell us how it went, use the study feedback form: {student feedback form URL}.
> Please use that form, not GitHub, so your feedback stays within the study.
>
> policymemo.ai runs inside your AI tool, under that tool's own terms, so don't
> enter personal or sensitive information.
>
> Jack Strachan
> policymemo.ai
