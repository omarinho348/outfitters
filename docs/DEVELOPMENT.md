# DEVELOPMENT.md

## Note on how this repo gets built

This project is developed across many AI chat sessions. The AI agent (running
in a sandboxed container with **no network access and no ability to push to
GitHub**) generates file contents and exact commands. **You run the commands
and installs on your own WSL2/Windows machine**, then paste back any errors
or output for the next step. Treat command output honestly — if something
fails, say so before proceeding.

## Phase 2 — Environment Setup (run these yourself, in WSL2 Ubuntu)

### 1. Verify/install core tools

```bash
# Node.js (use nvm for version management)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install --lts
node -v && npm -v

# Python 3.12+
sudo apt update && sudo apt install -y python3.12 python3.12-venv

# uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv --version

# Git
git --version
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 2. Expo CLI + EAS CLI

```bash
npm install -g eas-cli
npx create-expo-app@latest --version   # sanity check, no need to install globally
```

### 3. Expo Go on your iPhone

Install "Expo Go" from the App Store. This lets you run the dev build on your
physical iPhone over your LAN/tunnel without needing a Mac or Xcode for
day-to-day development. Xcode is only needed indirectly via EAS's cloud build
service when producing a real App Store binary later (Phase 18).

### 4. Android emulator (optional but recommended)

Install Android Studio → SDK Manager → install an emulator image. Alternative:
skip this and test only on your physical iPhone + Expo Go for now, add Android
emulator when you reach Android-specific testing.

### 5. MongoDB Atlas

- Create a free account at mongodb.com/cloud/atlas
- Create an M0 (free tier) cluster
- Create a database user (not your Atlas login) with a strong password
- Network access: allow your current IP (or 0.0.0.0/0 only for early dev,
  tighten before production)
- Copy the connection string — goes in backend `.env`, never committed

### 6. Cloudinary

- Create a free account at cloudinary.com
- From the dashboard, copy: cloud name, API key, API secret — goes in
  backend `.env`, never committed

### 7. OpenAI API key

- Create a key at platform.openai.com — goes in backend `.env`, never committed
- Set a usage limit/budget alert in the OpenAI dashboard immediately

## Network Development Note (Section 64 of spec)

Your phone can't reach `localhost` on your laptop. Two options:
- **LAN IP**: run backend with `--host 0.0.0.0`, connect from phone to
  `http://<your-laptop-LAN-IP>:8000` — requires phone and laptop on same
  Wi-Fi, works well, no extra tooling.
- **Tunnel**: `expo start --tunnel` or a tool like ngrok for the backend —
  works across networks, slightly slower, useful if LAN is unreliable.

Recommendation: start with LAN IP (simpler, faster), fall back to tunnel if
you hit network issues.

## `.env` Convention

Never commit `.env`. Commit `.env.example` with placeholder values only.
Each of `backend/.env` and any mobile-side config follows this pattern.

## Verification Checklist (report results honestly before we proceed)

- [ ] `node -v` shows an LTS version
- [ ] `uv --version` works
- [ ] `npx create-expo-app@latest --version` runs without error
- [ ] Atlas cluster created, connection string in hand
- [ ] Cloudinary credentials in hand
- [ ] OpenAI key created, budget alert set
- [ ] Expo Go installed on your iPhone