# ⚡ Power & EV Daily News Agent

Every morning it collects news **from LinkedIn posts and Google News** and
emails you a short digest (Gmail inbox), in **your priority order**:

1. 🚗 **EV & On-Board Charger Module Technology** — OBCs, traction inverters,
   e-axles, 800 V, SiC/GaN designed into EVs (business/policy noise filtered out)
2. 🔌 **Power Module Packaging & Efficiency** — module makers & their packaging
   tech: sintering, double-sided cooling, planar interconnects, new platforms
3. 🧱 **Packaging Materials Suppliers** — AMB/DCB/DPC substrates (Rogers-curamik,
   Ferrotec, NGK, Toshiba Materials, Denka, Maruwa…), bonding wires (Heraeus,
   Tanaka…), solder & sinter pastes (Indium Corp, Henkel, Kymera, Nihon
   Superior…), die-attach films, TIMs, lead frames, molding compounds

Research publications (journals, university studies) and market-report spam are
filtered out automatically. Duplicates are removed and remembered for 7 days.

---

## 📧 Cloud version — digest arrives in your Gmail inbox (free)

GitHub runs the agent daily on its servers (no computer of yours needed) and
emails you the digest. One-time setup ≈ 10 minutes:

**A. Get a Gmail "App Password"** (lets the agent send mail from your account)
1. Go to **myaccount.google.com/security** — turn on **2-Step Verification** if it's off
2. Go to **myaccount.google.com/apppasswords** → create one, name it e.g. `news` → **Create**
3. Copy the **16-letter password** it shows you (keep it for step C)

**B. Put the agent on GitHub**
1. Download & unzip `power-news-agent-github.zip`
2. On github.com click **+** (top right) → **New repository** → Name: `power-news` → choose **Public** → **Create**
3. On the new repo page click **Add file → Upload files**, drag in **everything** from the unzipped folder → **Commit changes**
   *(Mac: in Finder press* `Cmd+Shift+.` *to see the `.github` folder)*

**C. Add your email credentials**
1. In the repo: **Settings → Secrets and variables → Actions → New repository secret**
2. Add secret 1 — Name: `GMAIL_USER` → Value: *your gmail address* → Add secret
3. Add secret 2 — Name: `GMAIL_APP_PASS` → Value: *the 16-letter password from A.3* → Add secret

**D. Test it now** — repo tab **Actions** → **Daily Power & EV News Digest** →
**Run workflow** → after ~1 minute the digest should be in your Gmail inbox ✓

That's it. Every morning at 07:00/08:00 Berlin time the email arrives by
itself. (Gmail tip: if it ever lands in Spam, open it → **Report not spam**.)

---

## 💻 Optional: run it on your own PC instead

Needs only Python (python.org, tick "Add to PATH" on Windows):

- Windows: double-click `run_digest.bat` → digest generates and opens in browser
- Schedule daily: `schtasks /Create /SC DAILY /ST 07:30 /TN "PowerNewsDigest" /TR "C:\path\to\run_digest.bat"`
- Mac/Linux cron: `30 7 * * * cd /path/to/power-news-agent && ./run_digest.sh >> agent.log 2>&1`

## 💼 Optional: your private LinkedIn feed (PC only, ⚠️ ToS risk)

```bash
pip install playwright && playwright install chromium
python3 linkedin_reader.py     # first run: log in once when the window opens
python3 agent.py               # posts appear under "From your LinkedIn feed"
```
Cannot run in the cloud (needs your logged-in browser session).

---

## Tune it — `config.json`

| Key | Meaning |
|---|---|
| `google_news_queries` | the searches behind the news |
| `lookback_days` / per-tier `lookback_days` | how fresh items must be |
| `max_items` per tier | stories per section |
| `categories[].keywords` | `[regex, weight, label]` — the relevance brain |
| `llm_summary` | optional AI one-line summaries (needs OpenAI key) |

Flags: `--fresh` (ignore cross-day dedupe), `--keep-all` (debug).

## Files

```
agent.py              fetch → filter → score → dedupe → HTML digest
send_email.py         emails digests/latest.html via Gmail (used by GitHub)
linkedin_reader.py    optional private-feed capture (your PC)
config.json           sources + keywords + limits
digests/              digest-YYYY-MM-DD.html + latest.html + index.html
data/seen.json        7-day dedupe memory
.github/workflows/    the daily cloud schedule
```
