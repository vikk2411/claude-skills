---
name: germany-job-finder
description: >
  Automates Vikas Verma's daily Germany job search workflow. Use this skill whenever the user says
  "find jobs", "search jobs", "run job search", "daily job search", "find me jobs in Germany",
  or anything related to finding, searching or hunting for engineering jobs in Germany.
  This skill searches Indeed (via MCP), LinkedIn (via Apify), and Xing (via Apify) for
  Ruby on Rails / Node.js / Senior Backend Engineer / Principal Engineer / Architect roles in Germany,
  generates a tailored cover letter for each relevant job, saves each letter as a Google Doc
  in the cover letters folder, and appends all new jobs to the master tracker spreadsheet.
  Trigger this skill even if the user only says "find jobs" or "run the search" without
  specifying Germany — Germany is always the target.
---

# Germany Job Finder — Vikas Verma

Automates the full daily job search pipeline:
1. Search Indeed, LinkedIn (Apify), Xing (Apify)
2. Filter for relevant, recent, on-site Germany roles
3. Generate a tailored cover letter per job
4. Save each letter as a Google Doc in the cover letters folder
5. Append new rows to the master tracker sheet

---

## Hardcoded Constants

```
SHEET_TITLE      = "Germany Job Applications — Vikas Verma 2026"
SHEET_ID         = 15-_0wlPsJa6hUXMpmq4n0u1zCgxE4XrDtTiLWigGPHw
SHEET_URL        = https://docs.google.com/spreadsheets/d/15-_0wlPsJa6hUXMpmq4n0u1zCgxE4XrDtTiLWigGPHw

FOLDER_NAME      = "Germany Job Applications — Cover Letters 2026"
FOLDER_ID        = 1ogxey1qNJ-byW3YqA2QnY_n8QwpSX3h-
FOLDER_URL       = https://drive.google.com/drive/folders/1ogxey1qNJ-byW3YqA2QnY_n8QwpSX3h-
```

**NEVER create a new sheet or folder.** Always append to SHEET_ID and always upload letters to FOLDER_ID.

---

## Candidate Profile (for cover letter generation)

```
Name:          Vikas Verma
Location:      New Delhi, India (relocating to Germany — handles visa & relocation
               independently at own expense, no company sponsorship needed)
Current role:  Architect, Persistent Systems (Jul 2025–present), Gurugram
Experience:    12+ years

Key achievements:
- Persistent Systems: real-time AI donor suggestion engine for US nonprofit SaaS;
  PCI DSS compliance; cut CI build time 50% and cost 25%; migrated 3 products to Auth0
- Builder.ai (Oct 2020–May 2025, Principal Engineer): architected & led Builder Whiteboard
  — real-time multi-user collaboration tool with sub-100ms MEASURED production latency;
  built Builder UI Workspace (design-to-code, RoR+Node.js); led teams of 4–5 engineers;
  Figma integration
- Coral Mango (2016–2020): built LotusPay fintech (Y Combinator 2017);
  6+ modules of PayReview for 10K+ employees (RoR + React)
- Libserv (2015–2016): 4 HR modules in RoR; -20% LOC via refactor
- Dell (2013–2015): administered 500+ Linux servers

Stack: Ruby on Rails, PostgreSQL, Redis, Sidekiq, AWS (RDS S3 SNS SQS Lambda),
       Node.js, React.js, Docker, Kubernetes, GitLab CI/CD
Education: B.Tech IT, Maharaja Surajmal Institute of Technology, 2009–2013
Languages: English (professional), Hindi (native), German (beginner, learning)
AI tools:  Claude Code, Cursor
```

---

## Target Job Titles

Search for these roles — in order of priority:

**Ruby on Rails (primary stack):**
1. Ruby on Rails developer / engineer / Entwickler
2. Senior Software Engineer (Ruby / backend)
3. Principal Engineer (backend / Ruby)
4. Software Architect (Ruby / backend)
5. Fullstack Engineer (Ruby on Rails + React)

**Node.js / Backend (secondary stack — Vikas has real production Node.js experience):**
6. Senior Node.js developer / engineer
7. Backend Engineer Node.js
8. Senior Backend Engineer (Node.js / TypeScript)
9. Principal Engineer Node.js

**Generalized backend (broad net):**
10. Senior Backend Engineer (tech-agnostic — filter OUT Java-only, C++-only, Python-only after retrieval)
11. Staff Engineer / Principal Engineer backend
12. Software Architect backend

**Location:** Germany on-site only. No remote-only roles.

---

## Step 1 — Search Indeed (via Indeed MCP)

Use the Indeed MCP tool `search_jobs` with `country_code: DE`.

Run these searches:

**Ruby searches:**
```
1. "Ruby on Rails developer senior"         location: Germany
2. "Principal Engineer backend Ruby"        location: Germany
3. "Senior Software Engineer Ruby"          location: Germany
4. "Software Architect Ruby Rails"          location: Germany
```

**Node.js / Backend searches:**
```
5. "Senior Node.js developer backend"       location: Germany
6. "Backend Engineer Node.js TypeScript"    location: Germany
7. "Senior Backend Engineer"                location: Germany
8. "Staff Engineer backend"                 location: Germany
```

Collect all results. Deduplicate by job title + company name.

---

## Step 2 — Search LinkedIn (via Apify)

Actor: `curious_coder/linkedin-jobs-scraper`

**Always use the `f_TPR=r172800` URL parameter** — this filters to jobs posted in the last 2 days only.

Pass these URLs:

```
https://www.linkedin.com/jobs/search/?keywords=Ruby+on+Rails+developer&location=Germany&f_TPR=r172800&sortBy=DD
https://www.linkedin.com/jobs/search/?keywords=Principal+Engineer+Ruby&location=Germany&f_TPR=r172800&sortBy=DD
https://www.linkedin.com/jobs/search/?keywords=Senior+Software+Engineer+Ruby+Rails&location=Germany&f_TPR=r172800&sortBy=DD
https://www.linkedin.com/jobs/search/?keywords=Software+Architect+Ruby&location=Germany&f_TPR=r172800&sortBy=DD
https://www.linkedin.com/jobs/search/?keywords=Senior+Node.js+developer+backend&location=Germany&f_TPR=r172800&sortBy=DD
https://www.linkedin.com/jobs/search/?keywords=Backend+Engineer+Node.js&location=Germany&f_TPR=r172800&sortBy=DD
https://www.linkedin.com/jobs/search/?keywords=Senior+Backend+Engineer&location=Germany&f_TPR=r172800&sortBy=DD
https://www.linkedin.com/jobs/search/?keywords=Staff+Engineer+backend&location=Germany&f_TPR=r172800&sortBy=DD
```

Input schema:
```json
{
  "urls": ["<list of URLs above>"],
  "count": 20,
  "scrapeCompany": false
}
```

---

## Step 3 — Search Xing (via Apify)

Actor: `shahidirfan/Xing-Jobs-Scraper`

Run these separate calls (one keyword per call):
```json
{ "keyword": "Ruby on Rails developer", "location": "Deutschland" }
{ "keyword": "Principal Engineer Ruby", "location": "Deutschland" }
{ "keyword": "Senior Software Engineer Ruby", "location": "Deutschland" }
{ "keyword": "Software Architect Ruby Rails", "location": "Deutschland" }
{ "keyword": "Senior Node.js Entwickler", "location": "Deutschland" }
{ "keyword": "Backend Engineer Node.js", "location": "Deutschland" }
{ "keyword": "Senior Backend Engineer", "location": "Deutschland" }
```

---

## Step 4 — Filter Results

After collecting all results across all 3 sources, filter OUT:

- `job_type` is Part-time or Student/Intern
- Title contains: Junior, Intern, Working Student, Werkstudent, Praktikum
- Role is clearly not backend/fullstack:
  - Mobile-only (iOS, Android, Flutter, React Native)
  - Java-only, C++-only, Python-only, Go-only with no backend JS/Ruby mention
  - DevOps-only, SRE-only, Data Scientist, ML Engineer (unless full-stack adjacent)
- Already exists in the sheet (check by company name + job title match)
- **For Xing and Indeed:** posted more than 30 days ago
- **For LinkedIn:** always filtered to last 2 days via URL parameter

**For generalized "Senior Backend Engineer" results:** keep only if job description mentions
Node.js, Ruby, TypeScript, PostgreSQL, Redis, or similar backend tech Vikas knows.

Deduplicate across sources (same company + similar title = same job).

---

## Step 5 — Generate Cover Letters

For each qualifying job, generate a cover letter using the candidate profile above.

### Cover Letter Rules
- Max 220 words
- 4 short paragraphs:
  1. What role, why this company/domain specifically (1–2 sentences)
  2. 2–3 specific achievements with numbers from the profile
  3. Stack/culture alignment — reference the job's specific tech if known
  4. Closing
- Always end with: `"I will handle the entire visa and relocation process independently at my own expense — no sponsorship required from your side."`
- Sign off: `"Mit freundlichen Grüßen,\nVikas Verma"`
- No flattery. No filler phrases. Direct and factual.
- If the job has a named contact person, address them directly (e.g. "Dear Ms. Nixdorf")
- If no contact known, use "Dear Hiring Team,"
- Special cases:
  - Cargo/aviation roles: mention willingness to complete Luftsicherheitsüberprüfung
  - Fintech roles: lead with LotusPay (YC 2017) and PCI DSS experience
  - Real-time/collaboration roles: lead with Builder Whiteboard sub-100ms latency
  - AI/ML adjacent roles: mention Persistent Systems AI donor engine + Claude Code/Cursor usage
  - Node.js roles: lead with Builder UI Workspace (Node.js + RoR) and real-time system work

---

## Step 6 — Save Cover Letters to Google Drive

For each job, create a Google Doc in **FOLDER_ID** (`1ogxey1qNJ-byW3YqA2QnY_n8QwpSX3h-`):

```
Google Drive: create_file
  parentId:        1ogxey1qNJ-byW3YqA2QnY_n8QwpSX3h-
  contentMimeType: text/plain
  title:           YYYY-MM-DD — {Company} — {Short Job Title}
  textContent:     <cover letter text>
```

Save the returned Google Doc ID for use in the sheet.

---

## Step 7 — Append to Master Sheet

**The SHEET_ID is fixed and permanent: `15-_0wlPsJa6hUXMpmq4n0u1zCgxE4XrDtTiLWigGPHw`**
**NEVER create a new sheet. Always read + rewrite the same file.**

### 7a — Read existing rows (for deduplication)

```
Google Drive: download_file_content
  fileId:         15-_0wlPsJa6hUXMpmq4n0u1zCgxE4XrDtTiLWigGPHw
  exportMimeType: text/csv
```

Decode the base64 content. Parse the CSV to extract existing (Company, Job Title) pairs for deduplication.

### 7b — Rewrite the sheet with new rows appended

Build the full CSV: existing rows + new rows (do NOT duplicate the header).

Then update the file using:
```
Google Drive: create_file
  fileId:         15-_0wlPsJa6hUXMpmq4n0u1zCgxE4XrDtTiLWigGPHw
  contentMimeType: text/csv
  title:           Germany Job Applications — Vikas Verma 2026
  textContent:     <full CSV with headers + all rows>
```

**The Drive MCP `create_file` always creates a NEW file — it cannot update in place.**
After uploading, the tool returns a new file ID. This is the new SHEET_ID for this session.
Immediately tell the user:
- ✅ New sheet ID: `{new_id}`
- 🗑️ Please trash old sheet: `https://docs.google.com/spreadsheets/d/15-_0wlPsJa6hUXMpmq4n0u1zCgxE4XrDtTiLWigGPHw`
- 📊 New sheet URL: `https://docs.google.com/spreadsheets/d/{new_id}`

### Sheet columns (in order):
```
Date Found | Source | Job Title | Company | Location | Date Posted | Job URL | Cover Letter (Google Doc) | Status
```

- **Date Found**: today's date DD/MM/YYYY
- **Source**: Indeed / LinkedIn / Xing
- **Status**: "To Apply" for all new rows

---

## Step 8 — Report to User

After completing the full pipeline, report:

```
✅ Pipeline complete — {date}

Sources searched: Indeed, LinkedIn, Xing
New jobs found:   {n}
Letters created:  {n}
Skipped (filtered/duplicate): {n}

📊 New Sheet: https://docs.google.com/spreadsheets/d/{NEW_SHEET_ID}
📁 Letters:   https://drive.google.com/drive/folders/1ogxey1qNJ-byW3YqA2QnY_n8QwpSX3h-

🗑️ Please trash old sheet: https://docs.google.com/spreadsheets/d/15-_0wlPsJa6hUXMpmq4n0u1zCgxE4XrDtTiLWigGPHw

New jobs today:
| # | Title | Company | City | Source | Posted | Stack Match |
...

⭐ Top picks: {1-2 best matches by recency + stack fit}
```

---

## Error Handling

- If Indeed MCP returns 0 results for a query — log it, continue with other queries
- If Apify LinkedIn actor fails — log error, skip LinkedIn, continue with Xing
- If Apify Xing actor fails — log error, skip Xing, continue with available results
- If a cover letter generation fails — log the job as "Letter failed", still add to sheet with empty cover letter column
- If sheet download fails — start fresh with headers only, add all today's jobs
- Never stop the pipeline mid-way due to a single source failure

---

## Notes

- The Drive MCP does not support in-place file updates — it always creates a new file.
  Always update SHEET_ID in memory after each run and remind the user to trash the old one.
- Xing actor input takes ONE keyword per call — run separate calls per keyword.
- LinkedIn scraper uses `urls` array with `f_TPR=r172800` for last-2-days filter.
- Always deduplicate across sources before generating letters.
- Global Changer (Berlin) is a known company already in the sheet — skip if seen again
  unless it's a different role.
- Node.js roles are fully valid targets — Vikas has real production Node.js experience
  from Builder.ai (Builder UI Workspace, Builder Whiteboard backend).
