# AI Email Manager

## Product Requirements Document (PRD) & Project Scope

**Version:** 1.1
**Status:** MVP Planning
**Project Type:** Open-source, self-hostable AI email management tool
**License:** MIT
**Primary Goal:** Keep a user's inbox clean, organized, actionable, and mentally manageable.

---

# 1. Product Overview

## 1.1 Vision

Build an open-source, self-hostable AI email manager that connects to a user's existing mailbox and continuously manages their email.

The project should act like an:

> **AI buddy for your inbox.**

The system should understand incoming emails, determine what matters, identify what the user needs to do, surface emails requiring replies, summarize important conversations, and reduce the mental workload associated with managing email.

The fundamental product philosophy is:

> **The inbox should show the user what needs attention, not simply everything that has arrived.**

Traditional email clients answer:

> "What emails do you have?"

This project should answer:

> "What do you need to do?"

---

# 2. Problem Statement

Modern inboxes contain a mixture of:

* Important conversations
* Work requests
* Personal conversations
* Newsletters
* Marketing emails
* Receipts
* Notifications
* Automated messages
* Meeting invitations
* Emails requiring replies
* Emails requiring actions
* Spam
* Information-only emails
* Completed conversations
* Emails that no longer require attention

The problem is not simply the number of emails.

The real problem is the cognitive workload required to process every email.

A user receiving 100 emails per day may need to manually determine:

1. Is this important?
2. Do I need to reply?
3. Do I need to take action?
4. Is there a deadline?
5. Is this just information?
6. Is this a newsletter?
7. Is this spam?
8. Has this conversation already been handled?
9. Should I archive it?
10. Should I remember to do something later?

The project should automate this mental classification.

---

# 3. Product Goal

The system should transform:

```text
100 raw emails
        ↓
AI processing
        ↓
10 emails requiring attention
15 emails requiring replies
20 informational emails
25 newsletters/promotions
30 completed/low-value emails
```

The user should be able to open the application and immediately understand:

* What matters
* What requires a response
* What requires an action
* What can be ignored
* What has already been handled

---

# 4. Target Users

## 4.1 Primary Users

The initial target audience is developers and professionals who receive significant amounts of email.

Examples:

* Founders
* Entrepreneurs
* Developers
* Managers
* Salespeople
* Consultants
* Freelancers
* Executives
* Agency owners
* Students
* Knowledge workers

---

## 4.2 Ideal Early User

The ideal initial user is comfortable self-hosting (or running locally with Docker), cares about owning their email data, and receives approximately:

**50–200+ emails per day**

and frequently thinks:

> "I have too many emails and I don't know what actually needs my attention."

---

# 5. Project Positioning

Do NOT position the project simply as:

> "AI email sorting."

That is too generic.

The stronger positioning is:

> **An open-source AI buddy for your inbox.**

Potential messaging:

* "Your inbox, without the work."
* "Know what matters in your inbox."
* "Your inbox should tell you what to do."
* "Open-source, self-hosted, you own your data."

The central differentiators are:

> **Email becomes actionable information.**
>
> **You host it, you own the data, you choose the AI model.**

---

# 6. Open-Source Model

There is no paid tier, subscription, or payment processing. The project is free to use, modify, and self-host.

## 6.1 Self-Hosting First

* Runs locally or on the user's own server via Docker Compose.
* One user or a small group (family/team) per instance is the expected scale.
* Each deployment uses its own Google OAuth credentials and database.

## 6.2 Bring Your Own AI Key

* The user supplies their own AI provider API key (or points to a local model, e.g. Ollama).
* The AI layer is model-agnostic (see Technical Principles).
* The app shows estimated AI cost per email so users understand their own spend.

## 6.3 Backlog and Continuous Processing

Both modes remain, but are controlled by the user instead of billing:

* **Continuous:** every new email is processed automatically once a mailbox is connected.
* **Backlog:** user selects existing emails to process:
  * Selected emails
  * All unread emails
  * Last 7 / 30 days
  * A date range

Optional safeguards: configurable daily/total processing limits to cap AI spend.

## 6.4 Community & Sustainability

* Public repository, issue tracker, and discussions.
* `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`.
* Optional donations/sponsorship (GitHub Sponsors). No monetization is required for the project to succeed.

---

# 7. Core Philosophy

## 7.1 Do Not Aggressively Modify the User's Mailbox

Trust is critical, especially for a project that handles personal email.

The AI should initially be conservative.

### V1 AI CAN:

* Read emails
* Analyze emails
* Classify emails
* Summarize emails
* Determine importance
* Determine whether a reply is needed
* Determine whether an action is needed
* Generate reply suggestions
* Create email drafts
* Apply labels/categories if enabled
* Mark internal processing status

### V1 AI SHOULD NOT AUTOMATICALLY:

* Permanently delete emails
* Send emails
* Unsubscribe users
* Empty spam
* Delete conversations
* Perform irreversible actions

without explicit user permission.

---

# 8. Core Product Concept

Do not design the backend around physical Gmail folders such as:

```text
Inbox
Draft
Spam
Reply
```

Instead, build an internal **Email Intelligence Layer**.

Every email should have intelligence associated with it.

Example:

```json
{
  "email_id": "123",
  "category": "work",
  "intent": "reply_needed",
  "importance_score": 0.92,
  "urgency": "high",
  "requires_reply": true,
  "requires_action": false,
  "spam_probability": 0.01,
  "newsletter": false,
  "status": "active",
  "summary": "John is asking for approval of the Q3 proposal."
}
```

The UI can then create different views from this information.

---

# 9. Email Views

The application should expose intelligent views.

## 9.1 Needs Attention

Emails that require the user's attention.

Examples:

* Urgent requests
* Important decisions
* Deadlines
* Critical conversations

---

## 9.2 Needs Reply

Emails where the user likely needs to respond.

Examples:

* Questions
* Requests
* Follow-ups
* Approvals

---

## 9.3 Action Required

Emails where the user needs to perform an action.

Examples:

* Review document
* Approve invoice
* Complete application
* Submit information
* Sign document

---

## 9.4 Waiting

Emails where the user is waiting for another person.

Example:

```text
You → John:
"Can you send the report?"

John has not responded.

Status:
Waiting for John
```

---

## 9.5 FYI

Informational emails that don't require action.

---

## 9.6 Newsletters

Newsletters and recurring informational content.

---

## 9.7 Promotions

Marketing and promotional messages.

---

## 9.8 Spam

Emails that are highly likely to be unwanted.

---

## 9.9 Done

Emails/conversations that no longer require attention.

---

# 10. AI Email Intelligence

The AI should analyze each email and determine:

## Sender

Who sent it?

## Intent

Why did they send it?

## Importance

How important is it?

## Urgency

How urgently does the user need to respond?

## Action

Does the user need to do something?

## Reply

Does the user need to respond?

## Status

Is the conversation active, waiting, or completed?

## Category

What type of email is this?

## Summary

What does the email mean?

---

# 11. Email Intent Taxonomy

The initial intent taxonomy should include:

| Intent          | Description                     |
| --------------- | ------------------------------- |
| `reply_needed`  | User should respond             |
| `action_needed` | User must perform an action     |
| `meeting`       | Meeting or calendar-related     |
| `approval`      | User needs to approve something |
| `payment`       | Payment/invoice-related         |
| `information`   | Informational                   |
| `notification`  | Automated notification          |
| `newsletter`    | Newsletter                      |
| `promotion`     | Marketing/promotional           |
| `receipt`       | Purchase/payment receipt        |
| `personal`      | Personal conversation           |
| `spam`          | Likely spam                     |
| `completed`     | Conversation appears finished   |

The taxonomy should remain extensible.

---

# 12. AI Classification Output

The AI should return structured data rather than unstructured text.

Example:

```json
{
  "category": "work",
  "intent": "reply_needed",
  "importance_score": 0.91,
  "urgency": "high",
  "requires_reply": true,
  "requires_action": true,
  "spam_probability": 0.01,
  "newsletter": false,
  "status": "active",
  "summary": "John is asking you to review and approve the Q3 proposal before Friday.",
  "suggested_action": "Review and approve the Q3 proposal",
  "deadline": "2026-09-11"
}
```

The schema should be validated before being stored.

---

# 13. Importance Scoring

Every email should receive an importance score.

Example:

```text
0.00 – 0.20 = Very Low
0.20 – 0.40 = Low
0.40 – 0.60 = Normal
0.60 – 0.80 = Important
0.80 – 1.00 = Critical
```

The score should consider:

* Sender
* Relationship
* Email content
* Urgency
* Deadline
* Required action
* Conversation history
* Previous user behavior
* User corrections
* Thread status

Do not rely solely on keywords.

---

# 14. Urgency

Possible values:

```text
low
normal
high
critical
```

Examples:

### Low

"Here is this week's newsletter."

### Normal

"Here is the monthly report."

### High

"Can you approve this by tomorrow?"

### Critical

"Production is down. We need your approval immediately."

---

# 15. AI Summary

Important emails should receive a short summary.

Example:

### Original Email

A long 1,200-word message.

### AI Summary

> John wants approval for the revised Q3 marketing budget before Friday.

### Action

> Review and approve the proposal.

### Reply Required

> Yes.

### Deadline

> Friday.

The goal is to minimize reading time.

---

# 16. Reply Buddy

The product should identify emails requiring responses.

The workflow:

```text
Email
 ↓
Understand conversation
 ↓
Determine expected response
 ↓
Generate reply
 ↓
User reviews
 ↓
User edits if necessary
 ↓
Create draft
```

---

# 17. Reply Generation

The AI should support:

## Tone

* Professional
* Friendly
* Casual
* Direct
* Formal

## Length

* Short
* Medium
* Detailed

## Intent

* Accept
* Decline
* Ask clarification
* Provide information
* Acknowledge
* Schedule
* Follow up

Example:

Incoming:

> "Can you send the latest numbers?"

Suggested reply:

> "Sure, I'll send over the latest numbers shortly."

The user should be able to modify the response before it becomes a draft.

---

# 18. Important V1 Decision

The AI should **create drafts rather than automatically send emails**.

The user remains in control.

Workflow:

```text
AI generates reply
        ↓
User reviews
        ↓
User edits
        ↓
Create Draft
        ↓
User sends from Gmail
```

Autonomous sending can be introduced later as an advanced feature with explicit permission.

---

# 19. "Already Handled" Intelligence

This should be one of the product's major differentiators.

The system should determine whether an email/conversation still requires attention.

Example:

```text
John:
"Can you send the document?"

User:
"Sure, I'll send it."

User sends document.

John:
"Thanks, received it."
```

The system should identify:

```text
Conversation Status:
COMPLETED
```

It should no longer appear under:

```text
Needs Attention
```

---

# 20. Thread Intelligence

The system should eventually reason over entire email threads.

Example:

```text
Thread

John:
Can you review the proposal?

You:
I'll review it today.

John:
Thanks.

You:
Done. Looks good.

AI Status:
COMPLETED
```

Another example:

```text
John:
Can you review the proposal?

You:
I'll review it today.

AI Status:
WAITING / USER ACTION
```

The AI needs to understand conversation state, not just individual messages.

---

# 21. Dashboard

The dashboard should not look like a traditional email client.

It should feel like an **email command center**.

Example:

```text
=================================================
                 EMAIL MANAGER
=================================================

  NEEDS ATTENTION                         7

  NEEDS REPLY                            12

  ACTION REQUIRED                         5

  WAITING                                18

  FYI                                     32

  NEWSLETTERS                             41

  DONE                                   126

=================================================
```

The user should immediately see:

> **What do I need to deal with?**

rather than:

> **How many emails do I have?**

---

# 22. Dashboard Example

A user opens the application.

The system might show:

```text
Good morning.

You have 6 emails that actually need your attention.

-------------------------------------------------

1. Sarah needs approval
   Approve the proposal before 2 PM.

   [View] [Draft Reply]

-------------------------------------------------

2. John is waiting for you
   You promised to send the Q3 report.

   [View]

-------------------------------------------------

3. Amazon receipt
   No action required.

-------------------------------------------------

4. Weekly newsletter
   Informational.

-------------------------------------------------
```

This should be the core user experience.

---

# 23. Email Detail Page

Example:

```text
-------------------------------------------------

John Smith

Re: Q3 Marketing Budget

-------------------------------------------------

AI SUMMARY

John wants approval for the revised Q3
marketing budget before Friday.

-------------------------------------------------

ACTION

Review and approve proposal

-------------------------------------------------

URGENCY

High

-------------------------------------------------

REPLY REQUIRED

Yes

-------------------------------------------------

SUGGESTED REPLY

"Looks good. Approved from my side."

[ Edit ]
[ Create Draft ]

-------------------------------------------------

ORIGINAL EMAIL

...
```

---

# 24. Mailbox Integration

The initial provider should be:

## Gmail

Use Gmail OAuth and Gmail APIs.

The system should eventually support:

## Microsoft Outlook

Using Microsoft Graph.

---

# 25. Provider Architecture

Do not tightly couple the entire application to Gmail.

Create an abstraction layer.

Example:

```text
                    Email Provider Interface
                            │
                 ┌──────────┴──────────┐
                 ↓                     ↓
              Gmail                 Outlook
```

The application should work with a common internal interface.

Example operations:

```text
get_messages()
get_thread()
get_message()
create_draft()
mark_read()
apply_label()
archive()
```

Each provider implements the interface.

---

# 26. Authentication Flow

```text
User
 ↓
Create Account
 ↓
Connect Gmail
 ↓
Google OAuth
 ↓
Grant Permissions
 ↓
OAuth Callback
 ↓
Store Encrypted Credentials
 ↓
Create Mailbox
 ↓
Start Initial Sync
```

Security requirements:

* Encrypt OAuth credentials
* Never expose provider tokens to frontend
* Use server-side OAuth
* Use least-privilege scopes where possible
* Provide disconnect/revoke functionality

---

# 27. Email Ingestion

The ingestion system should support two paths.

## Historical Emails

```text
Gmail
 ↓
Sync
 ↓
Fetch messages
 ↓
Normalize
 ↓
Database
 ↓
Processing queue
```

## New Emails

```text
New email
 ↓
Provider event/webhook
 ↓
Email ingestion service
 ↓
Queue
 ↓
AI processing
```

---

# 28. Queue Architecture

AI processing should be asynchronous.

Do not process emails synchronously through the frontend request.

Bad architecture:

```text
User
 ↓
API
 ↓
AI
 ↓
Response
```

Preferred architecture:

```text
User / Gmail
      ↓
Email Ingestion
      ↓
Processing Queue
      ↓
Worker
      ↓
AI
      ↓
Database
      ↓
Frontend
```

This allows:

* Retries
* Concurrency
* Rate limiting
* Provider API limits
* AI failures
* Large inbox processing
* Horizontal scaling

---

# 29. Processing Pipeline

Each email should move through a pipeline.

```text
EMAIL RECEIVED
      ↓
NORMALIZE
      ↓
DEDUPLICATE
      ↓
THREAD RESOLUTION
      ↓
CONTENT CLEANING
      ↓
CLASSIFICATION
      ↓
INTENT DETECTION
      ↓
IMPORTANCE
      ↓
URGENCY
      ↓
ACTION DETECTION
      ↓
REPLY DETECTION
      ↓
SUMMARY
      ↓
THREAD STATUS
      ↓
STORE INTELLIGENCE
      ↓
UPDATE DASHBOARD
```

---

# 30. Email Content Processing

Before sending content to an AI model:

* Remove unnecessary HTML
* Extract readable text
* Remove tracking elements where possible
* Normalize whitespace
* Detect quoted previous messages
* Separate signature
* Identify sender/recipient information
* Identify thread context

Do not blindly send the entire raw HTML email to the model.

---

# 31. Thread Processing

For thread-level intelligence:

```text
Thread
 ↓
Collect relevant messages
 ↓
Order chronologically
 ↓
Separate user messages
 ↓
Separate external messages
 ↓
AI analyzes conversation
 ↓
Determine current state
```

Possible thread states:

```text
active
waiting_for_user
waiting_for_other_party
completed
archived
unknown
```

---

# 32. Database Design

A possible initial schema:

## Users

```text
users
--------------------------------
id
email
name
created_at
updated_at
```

---

## Mailboxes

```text
mailboxes
--------------------------------
id
user_id
provider
provider_account_id
encrypted_access_token
encrypted_refresh_token
status
created_at
updated_at
```

---

## Emails

```text
emails
--------------------------------
id
mailbox_id
provider_message_id
provider_thread_id
sender
recipients
cc
bcc
subject
body_text
body_html
received_at
is_read
created_at
updated_at
```

---

## Email Intelligence

```text
email_intelligence
--------------------------------
id
email_id
category
intent
importance_score
urgency
requires_reply
requires_action
spam_probability
newsletter
status
summary
suggested_action
deadline
model
model_version
created_at
updated_at
```

---

## Reply Suggestions

```text
reply_suggestions
--------------------------------
id
email_id
draft
tone
length
model
created_at
updated_at
```

---

## Processing Jobs

```text
processing_jobs
--------------------------------
id
email_id
job_type
status
attempts
error
created_at
started_at
completed_at
```

Possible job types:

```text
sync
classify
summarize
reply
thread_analysis
```

---

## Usage

Tracks AI cost per email (for transparency, not billing).

```text
usage
--------------------------------
id
user_id
email_id
processing_type
model
tokens_in
tokens_out
estimated_cost
created_at
```

---

# 33. Usage & Cost Tracking

There is no billing. Keep an internal usage ledger so users can see and cap their own AI spend.

```text
usage_id
user_id
email_id
operation
model
tokens_in / tokens_out
estimated_cost
timestamp
status
```

This provides:

* Cost transparency
* Spend limits
* Debugging
* Model comparison

---

# 34. Continuous Processing

```text
Mailbox connected & continuous mode on
        ↓
New Email
        ↓
Check limits (if configured)
        ↓
Process Email
        ↓
Record Usage
```

If the user turns continuous mode off or a limit is reached:

```text
Stop continuous processing
        ↓
Existing processed data remains available
```

---

# 35. Backlog Processing

```text
User selects 237 emails
        ↓
Show estimated AI cost
        ↓
User confirms
        ↓
Create processing job
        ↓
Process emails
```

The system must never process a backlog without explicit user confirmation.

---

# 36. Processing Status

Users should be able to see processing progress.

Example:

```text
Processing inbox...

████████████████░░░░ 78%

183 / 237 emails processed
```

Possible statuses:

```text
queued
processing
completed
failed
cancelled
```

---

# 37. User Corrections

The user should be able to correct the AI.

Example:

AI:

> Newsletter

User:

> Not a newsletter.

The system records:

```text
AI classification:
newsletter

User correction:
work
```

This information can eventually be used for personalized classification.

---

# 38. Personalization

Over time, the AI should learn user preferences.

Examples:

User consistently marks:

```text
GitHub notifications → low priority
```

System learns:

```text
GitHub notifications = low importance
```

User consistently marks:

```text
CEO emails → important
```

System learns:

```text
CEO → high importance
```

This should be introduced after the basic classifier is stable.

---

# 39. User Rules

Eventually allow explicit rules.

Example:

```text
Always mark emails from:
john@company.com

as:

Important
```

Or:

```text
Emails containing:
invoice

→ Finance
```

Rules should work alongside AI rather than replacing it.

---

# 40. Security & Privacy

Email is highly sensitive.

Security must be a first-class product requirement.

## Requirements

* Encrypt data in transit
* Encrypt sensitive data at rest
* Encrypt OAuth tokens
* Never expose tokens to frontend
* Strict database access controls
* User-level authorization checks
* Audit processing activity
* Allow account deletion
* Allow mailbox disconnection
* Allow email data deletion
* Minimize stored data where possible
* Do not use users' emails for model training without explicit policy/consent
* Log security-sensitive events

---

# 41. User Trust

The application should clearly communicate:

> AI is assisting you, not silently controlling your mailbox.

Every automated action should be understandable.

Example:

```text
Why is this important?

Because:
- Sender is in your frequent contacts
- Email asks for approval
- Deadline detected
```

This makes AI decisions explainable.

---

# 42. MVP Feature Set

The first production MVP MUST include:

## Account

* Signup/login
* User profile

## Gmail

* Gmail OAuth
* Gmail mailbox connection
* Initial email sync
* New email detection

## Email

* Email ingestion
* Thread association
* Email storage
* Email normalization

## AI

* Classification
* Intent detection
* Importance
* Urgency
* Reply detection
* Action detection
* Spam/newsletter detection
* Summary generation
* Thread status

## Dashboard

* Needs Attention
* Needs Reply
* Action Required
* Waiting
* FYI
* Newsletters
* Done

## Reply

* Generate reply
* Edit reply
* Create Gmail draft

## Open-Source Basics

* Docker Compose setup
* README with setup and Google OAuth instructions
* Bring-your-own AI key configuration
* Usage/cost tracking
* LICENSE, CONTRIBUTING, SECURITY

---

# 43. Explicitly Out of Scope for MVP

Do NOT build these in V1.

## Email actions

* Automatic deletion
* Automatic unsubscribe
* Automatic sending
* Automatic permanent archival

## Integrations

* Slack
* WhatsApp
* CRM
* Calendar automation
* Notion
* Teams

## Platforms

* Native iOS app
* Native Android app

## AI

* Custom ML model
* Complex autonomous agents
* Multi-agent architecture
* Voice assistant

## Other

* Billing, subscriptions, payments
* Hosted multi-tenant SaaS
* Full Gmail replacement
* Email marketing
* Mass email sending
* CRM functionality

---

# 44. V1.5

After MVP validation:

## Smart Actions

```text
Archive
Mark Done
Remind Me
Create Task
Snooze
```

## Attachment Intelligence

Detect:

```text
Invoice
Contract
Resume
Report
Spreadsheet
Proposal
Receipt
```

## Better Thread Intelligence

```text
Waiting for you
Waiting for them
Completed
Needs follow-up
```

## Better Reply Generation

```text
Reply
Reply + explain
Reply + negotiate
Reply + ask clarification
```

---

# 45. V2 — AI Email Buddy

The long-term product should behave like a personal email assistant.

Every morning:

```text
Good morning.

You have 6 emails that need your attention today.

1. Sarah needs approval
   Deadline: 2 PM

2. John is waiting for the report
   You promised to send it.

3. Client asked for pricing
   Reply recommended.

4. Invoice received
   No action required.
```

The user should not need to manually inspect hundreds of emails.

---

# 46. Long-Term Product Vision

Eventually the product should understand:

```text
People
 ↓
Conversations
 ↓
Intent
 ↓
Tasks
 ↓
Deadlines
 ↓
Commitments
 ↓
Follow-ups
```

The email becomes merely the input.

The actual product becomes:

> **A personal communication and task intelligence layer.**

---

# 47. Architecture

Recommended high-level architecture:

```text
                         FRONTEND
                            │
                            ↓
                       API SERVER
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
     AUTH SERVICE      EMAIL SERVICE      USAGE 
          │                 │                 │
          │                 ↓                 │
          │            INGESTION             │
          │                 │                 │
          │                 ↓                 │
          │              QUEUE                │
          │                 │                 │
          │                 ↓                 │
          │              WORKERS              │
          │                 │                 │
          │        ┌────────┼────────┐        │
          │        ↓        ↓        ↓        │
          │    CLASSIFIER SUMMARY REPLY AI    │
          │        │        │        │        │
          └────────┴────────┼────────┴────────┘
                            ↓
                         DATABASE
                            │
                            ↓
                       DASHBOARD
```

---

# 48. Core Components

The initial backend should contain:

## API

Responsible for:

* Authentication
* Dashboard requests
* Email queries
* Reply generation
* Usage/cost queries
* User preferences

## Email Service

Responsible for:

* Gmail integration
* Email synchronization
* Email normalization
* Thread handling

## Queue

Responsible for:

* AI processing
* Retry
* Rate limiting
* Background jobs

## AI Service

Responsible for:

* Classification
* Intent
* Importance
* Summary
* Reply generation
* Thread intelligence

## Usage Service

Responsible for:

* Usage ledger
* Cost estimates
* Optional spend limits

## Database

Stores:

* Users
* Mailboxes
* Emails
* Intelligence
* Threads
* Jobs
* Usage

---

# 49. Development Phases

## Phase 1 — Foundation

Goal:

> Connect Gmail and display emails.

Build:

```text
Authentication
 ↓
Gmail OAuth
 ↓
Mailbox connection
 ↓
Email sync
 ↓
Database
 ↓
Basic inbox UI
```

Do not add complex AI yet.

---

# 50. Phase 2 — AI Brain

Goal:

> Understand emails.

Build:

```text
Email
 ↓
Queue
 ↓
Classifier
 ↓
Intent
 ↓
Importance
 ↓
Urgency
 ↓
Summary
```

Now the application has basic email intelligence.

---

# 51. Phase 3 — Email Buddy

Goal:

> Help the user act on email.

Build:

```text
Reply detection
Action detection
Reply generation
Thread status
Done detection
```

This is where the product starts feeling like an AI assistant.

---

# 52. Phase 4 — Open-Source Readiness

Implement:

* Docker Compose / one-command setup
* Bring-your-own AI key + model config
* Usage tracking and optional spend limits
* Docs, LICENSE, CONTRIBUTING, SECURITY
* Backlog processing with cost estimate and confirmation

---

# 53. Phase 5 — Continuous Automation

Goal:

> Make the product work automatically.

Final continuous flow:

```text
New Email
    ↓
Webhook/Event
    ↓
Ingestion
    ↓
Queue
    ↓
AI Processing
    ↓
Classification
    ↓
Thread Intelligence
    ↓
Dashboard Update
```

The user does nothing.

The inbox stays organized automatically.

---

# 54. MVP User Journey

## Step 1

User self-hosts the app (or runs it locally) and opens it.

---

## Step 2

User creates account.

---

## Step 3

User sees:

> Connect your inbox.

---

## Step 4

User connects Gmail.

---

## Step 5

System displays:

```text
Your inbox contains:

1,247 emails
342 unread
87 potentially important
54 may require replies
32 require actions
```

---

## Step 6

User chooses:

> Clean my inbox.

System shows:

```text
342 emails selected

Estimated AI cost:
~$X.XX (your API key)

[ Process Emails ]
```

---

## Step 7

User confirms.

---

## Step 8

Processing begins.

```text
Processing...

234 / 342
```

---

## Step 9

Dashboard becomes:

```text
NEEDS ATTENTION       18

NEEDS REPLY           31

ACTION REQUIRED       14

WAITING               23

FYI                   96

NEWSLETTERS           87

DONE                  73
```

---

## Step 10

User opens:

> Needs Reply

AI shows:

```text
Sarah

Can you approve the proposal?

AI suggested:

"Yes, looks good. Approved from my side."

[Edit]
[Create Draft]
```

---

# 55. Success Metrics

## Product Metrics

Track:

* Emails processed
* Processing success rate
* AI classification accuracy
* Classification correction rate
* Average processing time
* AI cost per email (user-visible)

## User Metrics

Track:

* Emails processed per user
* Emails marked done
* Reply suggestions accepted
* Reply suggestions edited
* AI classifications corrected
* Inbox reduction

## Community Metrics

Track:

* GitHub stars and forks
* Contributors
* Issues opened/closed
* Successful self-host installs (via issues/feedback, no telemetry by default)

---

# 56. Most Important Product Metric

The most important conceptual metric is:

> **How many emails did the AI successfully remove from the user's mental workload?**

A successful system should make users feel:

> "I don't need to check every email anymore."

---

# 57. Technical Principles

The implementation should follow these principles:

### 1. Provider Agnostic

Do not hard-code Gmail into business logic.

### 2. Queue First

AI processing must be asynchronous.

### 3. Idempotent

The same email should never accidentally be processed multiple times (wasting the user's AI spend).

### 4. Auditable

Every AI decision should be traceable.

### 5. Reversible

Automated mailbox actions should be reversible.

### 6. Human in the Loop

Users should approve important actions.

### 7. Structured AI

AI should return validated structured JSON.

### 8. Model Agnostic

The AI provider/model should be replaceable.

### 9. Cost Aware

Track AI token/model costs per email.

### 10. Security First

Email data must be treated as sensitive.

### 11. Self-Hostable

Everything must run locally with minimal setup. No required external paid service besides the user's AI key.

### 12. No Telemetry by Default

The project must not phone home. Any analytics must be opt-in.

---

# 58. MVP Acceptance Criteria

The MVP should be considered functional when:

### Gmail

* User can connect Gmail.
* User can disconnect Gmail.
* System can retrieve emails.
* System can identify threads.
* System can detect new emails.

### AI

* Every processed email receives classification.
* Every important email receives a summary.
* Reply-required emails are identified.
* Action-required emails are identified.
* Importance is calculated.
* Thread status is calculated.

### Dashboard

* User can view intelligent categories.
* User can open individual emails.
* User can view AI summary.
* User can see suggested action.
* User can see suggested reply.

### Reply

* User can generate a reply.
* User can edit the reply.
* User can create a Gmail draft.

### Open Source

* A new user can set up the project from the README using Docker.
* AI provider/model is configurable via environment variables.
* System tracks processed emails and estimated cost.
* System does not process a backlog without user confirmation.

---

# 59. What NOT to Optimize Too Early

Do not spend excessive time initially on:

* Fancy UI animations
* Mobile apps
* Custom AI models
* Complex automation
* Multiple providers
* Advanced analytics
* Hosted/SaaS infrastructure and monetization
* Autonomous agents

The first question is:

> **Will users trust the AI to understand their inbox, and does it genuinely save them time?**

Validate this (with early contributors and users) before expanding the system.

---

# 60. First Technical Milestone

The first engineering milestone should be:

> **Connect Gmail → synchronize emails → store them → display them.**

The second:

> **Process a single email through the AI pipeline and return structured intelligence.**

The third:

> **Process an entire inbox asynchronously.**

The fourth:

> **Build the intelligent dashboard.**

The fifth:

> **Generate and create Gmail drafts.**

The sixth:

> **Add usage tracking and open-source packaging (Docker, docs, license).**

The seventh:

> **Turn on continuous processing.**

---

# 61. Recommended Build Order

```text
01. Project setup
        ↓
02. Database
        ↓
03. Authentication
        ↓
04. Gmail OAuth
        ↓
05. Gmail API integration
        ↓
06. Email synchronization
        ↓
07. Email normalization
        ↓
08. Thread resolution
        ↓
09. Queue system
        ↓
10. AI classification
        ↓
11. AI summary
        ↓
12. Intent detection
        ↓
13. Importance scoring
        ↓
14. Reply detection
        ↓
15. Action detection
        ↓
16. Thread status
        ↓
17. Dashboard
        ↓
18. Email detail page
        ↓
19. Reply generation
        ↓
20. Gmail draft creation
        ↓
21. Usage & cost tracking
        ↓
22. Docker Compose setup
        ↓
23. README, LICENSE, CONTRIBUTING
        ↓
24. New-email automation
        ↓
25. Monitoring & error handling
        ↓
26. Public release (v0.1)
```

---

# 62. Final MVP Definition

The MVP is:

> **An open-source, self-hostable web application that connects to Gmail, understands existing and incoming emails using AI (user-provided API key), organizes them into actionable views, summarizes important conversations, identifies emails requiring replies/actions, generates reply drafts, and supports both continuous processing and backlog cleanup.**

The MVP should NOT attempt to replace Gmail.

It should sit **on top of Gmail** and provide an intelligence layer.

---

# 63. Long-Term Vision

The long-term product should evolve from:

```text
Email Classifier
```

to:

```text
Email Manager
```

to:

```text
AI Email Assistant
```

to:

```text
Personal Communication Agent
```

The ultimate system understands:

```text
Emails
 ↓
People
 ↓
Conversations
 ↓
Intent
 ↓
Tasks
 ↓
Deadlines
 ↓
Commitments
 ↓
Follow-ups
 ↓
Actions
```

At that point, email is no longer the focus.

**The project is an open-source AI layer that manages the user's communication workload.**

---

# 64. North Star

The simplest way to define success is:

> **If the user opens the app and immediately knows what they need to do, what can wait, and what can be ignored, the project has succeeded.**

The product should make the user's inbox feel less like a mailbox and more like a **personal assistant that has already done the first pass for them.**
