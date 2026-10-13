# Mailmate

## Product Requirements Document (PRD) v2.0

**Status:** Phase 1 planning
**Type:** Open-source, self-hostable AI email cleaner
**License:** MIT
**Replaces:** PRD v1.1 (still in git history). v1.1 planned a full "email command center" website. v2.0 drops that: **Gmail is the interface.**

---

# 1. Vision

> **Log in once. Your Gmail cleans itself.**

Mailmate does its work **inside Gmail**. The user never opens a Mailmate inbox. They sign in with Google, and from then on every email that arrives is read by an AI classifier and **sorted into Gmail labels**. The labels live in Gmail, the sorted mail lives in Gmail, and the user keeps using Gmail on web, phone or desktop exactly as before, only tidier.

The website is a doorway, not a destination:

| | Where it happens |
|---|---|
| Sign in, connect Gmail, turn it on/off, disconnect | Mailmate website (tiny) |
| Labels, sorted mail, reading, replying | **Gmail** |

---

# 2. Problem

A busy inbox mixes things that matter with newsletters, promotions, receipts, notifications and spam. Deciding what each email is costs attention. Gmail's own tabs are coarse and not personal. Mailmate does that first pass automatically and shows the result where the user already works.

---

# 3. Principles

1. **Gmail is the UI.** No inbox, list or reader on the website.
2. **Conservative on the mailbox.** Mailmate may *read* mail and *create/apply labels*. It never sends, never deletes, never empties spam, never unsubscribes. Anything it does must be reversible (a label can be removed in one click).
3. **Queue first.** Classification is asynchronous and survives restarts, retries and rate limits. Nothing waits on the website.
4. **Idempotent.** An email is classified once. Re-running the server never double-labels or double-charges.
5. **Self-hosted, you own the data.** The user runs the server. Bring your own AI key, or a local model.
6. **Model-agnostic, structured AI.** The classifier returns validated JSON, not free text.
7. **No telemetry.** The project never phones home.
8. **Email is sensitive.** Tokens encrypted at rest, minimal stored data, easy disconnect.

---

# 4. Phase 1: "Log in and your Gmail sorts itself" (this PRD's focus)

**Goal:** a person signs in with Google, starts the server, and new emails arriving in their Gmail are automatically labelled by an AI classifier. Nothing else.

## 4.1 The experience

```text
1. User runs the server (docker compose up, or the run command).
2. User opens the Mailmate site and clicks "Sign in with Google".
3. Google asks for permission to read mail and manage labels. User accepts.
4. Mailmate shows: "Connected. Mailmate is cleaning kevlar@gmail.com."
5. User goes back to Gmail. From now on, each new email arrives already labelled.
```

The user does nothing else. They never come back to the website unless they want to pause or disconnect.

## 4.2 The flow

```text
New email arrives in Gmail
        │
        ▼
Server detects it (poll Gmail for new mail every N seconds)
        │
        ▼
Job added to the QUEUE (one job per email, deduplicated)
        │
        ▼
Worker picks up the job
        │
        ▼
Fetch the email → clean it (strip HTML, quotes, tracking links)
        │
        ▼
AI classifier → returns one label + confidence + short reason (validated JSON)
        │
        ▼
Gmail: make sure the label exists (create if missing), apply it to the message
        │
        ▼
Job marked done; result recorded (so it is never processed again)
```

## 4.3 Labels

All Mailmate labels are created **in the user's Gmail**, grouped under a parent so they never clash with the user's own labels (Gmail shows them nested):

| Gmail label | What goes in it |
|---|---|
| `Mailmate/Important` | Needs the user's attention: personal or work mail from real people, deadlines, decisions |
| `Mailmate/Needs Reply` | Someone is waiting for an answer |
| `Mailmate/Action Required` | The user must do something (approve, pay, sign, submit) |
| `Mailmate/Updates` | Notifications and automated messages worth knowing (shipping, alerts, account notices) |
| `Mailmate/Receipts` | Receipts, invoices, payment confirmations |
| `Mailmate/Newsletters` | Recurring editorial content |
| `Mailmate/Promotions` | Marketing and sales offers |
| `Mailmate/Social` | Social network and community notifications |
| `Mailmate/Spam` | Likely junk or scams (label only, **never moved to Spam or deleted**) |

Rules:
* Each email gets **exactly one** primary label (the AI picks the best fit).
* The label set lives in one config list, so adding or renaming a label is a one-line change.
* If the AI is unsure (low confidence), the email gets `Mailmate/Important`: wrongly hiding something is worse than wrongly showing it.
* Mailmate only ever manages labels under `Mailmate/`. It never touches the user's other labels.
* **Cleaning** in Phase 1 means *sorted and labelled*. Mail stays in the inbox unless the user turns on the optional setting below.

**Optional setting (off by default):** "Skip the inbox" for `Newsletters`, `Promotions`, `Social` and `Receipts`: Mailmate removes the `INBOX` label so they sit only under their Mailmate label. This is reversible (the mail is still in All Mail and under its label) and never deletes anything.

## 4.4 Website (kept minimal)

Three screens only:

1. **Sign in with Google.** Google login is the only way in. No separate password.
2. **Status.** Shows the connected Gmail address, whether Mailmate is running, how many emails it labelled today, and the last error if any. Controls: **Pause / Resume**, **Skip-the-inbox toggle**, **Disconnect**.
3. **Disconnect** revokes Google access and deletes everything Mailmate stored about that mailbox. Labels already applied stay in Gmail (they belong to the user); an option offers to remove the `Mailmate/` labels too.

No email list, no email reader, no reply UI. Gmail does all of that.

## 4.5 Server and queue

* **One server process** runs the API (for the website), the new-mail poller and the queue worker. Single command to start.
* **Queue:** a persistent job table in the database (status: `queued`, `processing`, `done`, `failed`). Jobs are unique per email, so duplicates are impossible. On restart, interrupted jobs go back to `queued`.
* **Retries:** failed jobs retry with backoff up to 3 times, then stay `failed` with the error visible on the Status screen.
* **Rate limits:** the worker processes a limited number of emails per minute to respect Gmail and AI limits.
* **New mail detection:** polling Gmail's history API every ~60 seconds, starting from the moment the user connected. (Push notifications via Pub/Sub are a later phase because they need a public HTTPS endpoint.)
* **Only new mail.** Emails that were already in the inbox at connect time are **not** touched in Phase 1 (see Phase 2).
* **Scaling note:** one worker thread in the API process is enough for a person or a family. Moving to Celery/Redis is a later option.

## 4.6 AI classifier

* Input: sender, recipients, subject, cleaned body (truncated), and the user's own address.
* Output (validated before use):

```json
{
  "label": "needs_reply",
  "confidence": 0.86,
  "reason": "Sarah asks you to approve the proposal before Friday."
}
```

* Judges meaning, not keywords. Email content is treated as data, never as instructions to the model.
* **Provider is configurable** by environment variables: Anthropic, or any OpenAI-compatible endpoint (OpenAI, Ollama, LM Studio). The user supplies their own key or a local model.
* The model's token usage per email is recorded so cost can be shown later.

## 4.7 Data stored (minimum)

* The user and their encrypted Google tokens.
* Per processed email: Gmail message id, thread id, chosen label, confidence, reason, timestamps. **The email body is not stored** in Phase 1; it is fetched, classified and discarded.
* The job queue and token-usage records.

## 4.8 Permissions

Google OAuth scopes: `gmail.modify` (read mail and create/apply/remove labels, no delete-forever, no send). Because labelling needs `modify`, the consent screen must say so plainly. Mailmate does **not** request send permission.

## 4.9 Out of scope for Phase 1

Cleaning up the existing backlog, summaries, reply drafts, thread/"already handled" intelligence, a dashboard, a website email viewer, corrections/learning, Outlook, mobile apps, push notifications, multi-user teams, billing.

## 4.10 Phase 1 acceptance criteria

- [ ] User signs in with Google on the website and sees "Connected".
- [ ] Starting the server with one command starts the API, the poller and the queue worker.
- [ ] A new email sent to the connected Gmail is detected within about 2 minutes.
- [ ] That email gets exactly one `Mailmate/…` label applied **in Gmail**, visible in the Gmail app. The label was created automatically if it did not exist.
- [ ] Restarting the server mid-processing loses no email and labels no email twice.
- [ ] A failed AI call is retried and, after 3 failures, shown as failed on the Status screen without blocking other emails.
- [ ] Pause stops new processing; Resume continues from where it left off.
- [ ] Disconnect revokes Google access and deletes stored data.
- [ ] Mailmate has not sent, deleted or moved to Spam any email.
- [ ] AI provider and model are switchable through environment variables only.
- [ ] A new user can follow the README and have it working with Docker.

---

# 5. Later phases

## Phase 2: Clean the existing inbox
Process emails already in the mailbox: choose a scope (unread, last 7/30 days), show an **estimated AI cost**, require **explicit confirmation**, then run through the same queue with a visible progress count on the Status page. Optional daily processing limit to cap spend.

## Phase 3: Smarter than a label
Short AI summaries and suggested actions, importance and urgency, deadline detection, and **thread awareness** (if the user already replied or the other side said "thanks", the thread is marked done; if the user is waiting on someone, `Mailmate/Waiting`). Optional extra labels such as `Waiting` and `Done`.

## Phase 4: Reply buddy
Generate a reply (tone, length, intent) and **create a Gmail draft** in the thread. The user reviews and sends it from Gmail. Mailmate never sends. Requires the `gmail.compose` permission, requested only when this feature is enabled.

## Phase 5: Learns you
User corrections (the user moves an email to a different `Mailmate/` label in Gmail and Mailmate notices), per-sender rules, and personalization from past corrections.

## Phase 6: Real-time and scale
Gmail push notifications instead of polling, Celery/Redis workers, Outlook support via Microsoft Graph, a small optional digest ("6 emails need you today").

## Open source basics (grow alongside every phase)
Docker Compose, README with Google OAuth setup, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, MIT license, usage/cost tracking, no telemetry.

---

# 6. Technical outline (Phase 1)

```text
Browser ── Next.js site (login + status only)
              │
              ▼
        API server (FastAPI) ───────────────┐
              │                              │
   ┌──────────┼───────────┐                  │
   ▼          ▼           ▼                  │
 Google    Poller      Worker ──► AI ──►  Gmail API
 OAuth   (new mail)   (queue)   (classify)  (create/apply labels)
              │          │
              └──► Database (users, tokens, jobs, results, usage)
```

* **Reuse from the earlier build:** Google OAuth, encrypted token storage, Gmail fetching, the DB-backed job queue and the model-agnostic AI layer (kept in the git stash from the previous attempt). The email list/detail endpoints and most of the website are **not** reused.
* **Provider boundary:** Gmail calls (`list_new`, `get_message`, `ensure_label`, `apply_label`) sit behind one small module so Outlook can be added later without touching the queue or classifier.
* **Idempotency:** unique key on (mailbox, Gmail message id); the label is applied only when a job moves to `done`.

---

# 7. Decisions to confirm

1. **"jev":** this PRD reads it as the **AI classifier** that sorts each email. If it means something else, only section 4.6 changes.
2. **Sign-in:** Google login is the *only* account system (no separate email/password). Simpler, and matches "the user only logs in to Gmail".
3. **Cleaning = labels, inbox untouched by default.** Auto-skipping the inbox for newsletters, promotions, social and receipts is a switch the user turns on.
4. **Label list:** the 9 labels in 4.3 are a starting set; edit before building if you want different buckets.
5. **Backlog is Phase 2,** so Phase 1 only sorts mail that arrives after connecting.
