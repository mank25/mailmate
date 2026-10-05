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

**User → Connect Gmail → Sync Emails → Store Emails → View Inbox**

AI processing and further automation come in later phases. See `_Docs/PRD.md`.

Mailmate is open source ([MIT](LICENSE)) and meant to be self-hosted: you run it, you own your data, and (later) you bring your own AI API key.

### Setup

**1. Google OAuth credentials** (each self-hoster creates their own)

1. In [Google Cloud Console](https://console.cloud.google.com), create a project and enable the **Gmail API**.
2. **OAuth consent screen**: choose External, add the scope `gmail.readonly`, and add your Gmail address(es) under **Test users**.
3. **Credentials → Create OAuth client ID → Web application**, with the redirect URI `http://localhost:8000/auth/gmail/callback`.
4. Copy the client ID and secret into `backend/.env`.

> While the consent screen is in *Testing*, Google expires refresh tokens after 7 days and you must reconnect. For personal use you can set the app to *In production* (you'll see an "unverified app" warning, which is fine for your own accounts).

**2. Backend**

```bash
cd backend
cp .env.example .env        # fill in the values; the app refuses to start with placeholder secrets
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head        # needs an existing MySQL database named "mailmate"
uvicorn app.main:app --reload
```

**3. Frontend**

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000, sign up (the first account can always sign up; set `ALLOW_SIGNUP=true` to allow more), then connect Gmail. Multiple Gmail accounts can be connected per user.

### Running on a LAN / home server

Google only allows `http://` OAuth redirects for `localhost`, so a LAN IP like `http://192.168.1.20:8000/...` will not work for connecting Gmail. Options:

* **Easiest:** connect Gmail from the host machine via `localhost`. Other devices can use the app afterwards, since tokens are stored server-side.
* **Proper:** serve over HTTPS on a real domain (e.g. Tailscale `*.ts.net`, or Caddy with a domain you own) and set `GOOGLE_REDIRECT_URI` and `FRONTEND_URL` to those URLs.
* If you serve over plain HTTP on a non-localhost address, set `COOKIE_SECURE=false`.

### Security notes

* Gmail tokens are encrypted at rest and never sent to the browser.
* Don't expose an instance to the internet without HTTPS and `ALLOW_SIGNUP=false`.
