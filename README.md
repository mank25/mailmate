# Mailmate

**Mailmate is an AI-powered email manager that acts like a buddy for your inbox.**

Instead of simply showing users everything in their inbox, Mailmate helps them understand **what actually matters and what they need to do**.

### What Mailmate does

* Connects to your existing Gmail inbox
* Understands and organizes incoming emails
* Identifies important emails
* Detects emails that need a reply or action
* Summarizes important conversations
* Tracks whether conversations are still active or already handled
* Helps draft replies while keeping the user in control

### Vision

> **Your inbox, without the work.**

Mailmate is designed to reduce the mental effort of managing email by turning a noisy inbox into a clear list of things that actually need attention.

### Current Status

🚧 **Early development — Phase 1**

Phase 1 focuses on the foundation:

**User → Connect Gmail → Sync Emails → Store Emails → View Inbox**

AI processing, billing, and advanced automation will be added in later phases.

### Getting Started

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

**Backend**

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
