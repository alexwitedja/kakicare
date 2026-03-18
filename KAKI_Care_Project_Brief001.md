# KAKI Care — Project Brief

> A companion app for patients with **chronic diseases**. Helps users track their medical condition easily and exports doctor-ready summaries.

**Note:** The system is disease-agnostic — it can support any chronic condition (CHF, diabetes, COPD, hypertension, etc.) through configurable disease profiles. **Congestive Heart Failure (CHF) is our golden case for the demo** because it has well-researched signals, validated thresholds, and a compelling narrative (25% 30-day readmission rate).

---

## Competition Context

**NUS-Synapxe-IMDA AI Innovation Challenge 2026**

- **Focus:** Healthcare AI solutions for patient care, clinical workflows, or health system efficiency in Singapore
- **Team:** 2-5 members (at least 1 NUS student required)
- **Timeline:** Registration by May 15 → Proposal by May 30 → Finals July 18
- **Prizes:** S$15K (1st), S$8K (2nd), S$5K (3rd) + potential pilot with Synapxe

**Judging Criteria:**
1. Innovation & technical merit (30%)
2. Clinical relevance & impact (25%)
3. Feasibility & scalability (20%)
4. Data privacy & safety (15%)
5. Presentation quality (10%)

---

## Problem Statement (General)

Patients with **chronic diseases** (heart failure, diabetes, COPD, etc.) often decompensate gradually over days before a crisis. Warning signs are present but frequently go unnoticed or are not communicated to physicians in time.

**The gap:** No easy way for patients to:
1. Track relevant health metrics consistently
2. Get alerted when something is off
3. Share meaningful summaries with their doctors

KAKI Care closes this gap with AI-powered monitoring and proactive engagement.

---

## Solution: KAKI Care

A **context-aware patient monitoring agent** for chronic disease patients that:
1. Passively monitors health signals (wearables, smart scale)
2. Proactively asks targeted questions only when anomalies detected
3. Extracts notable events from conversations
4. Generates doctor-ready summaries before appointments

### Disease-Agnostic Design
The system works for **any chronic condition** — the `disease_profile` in the database stores:
- Disease name
- Relevant metrics to track
- Thresholds (as text, AI interprets)
- Common symptoms

Swap CHF for diabetes or COPD, configure the profile, and the same workflows apply.

### Core Value Proposition
**"Catch decompensation before crisis"** — passive monitoring → smart alerts → doctor summary.

---

## Golden Case for Demo: Congestive Heart Failure (CHF)

> **Why CHF?** Well-researched, measurable signals, validated clinical thresholds, and a compelling problem (25% 30-day readmission rate). Everything below in this section is CHF-specific research for the demo.

### What is CHF?

Congestive Heart Failure is a chronic condition where the heart cannot pump blood efficiently. Patients move through severity stages (NYHA Class I-IV) and experience episodes of acute decompensation.

**The critical gap:** Patients slowly decompensate over days before a crisis. Warning signs are present but often go unnoticed or not communicated to physicians.

**Key statistic:** ~25% of CHF patients are readmitted to hospital within 30 days of discharge — largely due to missed early warning signals.

### Pros & Challenges of CHF as Demo Case

### Pros
- Well-defined, measurable clinical signals (weight, HR, SpO2)
- Strong passive data capture via wearables and smart scales
- Episodic nature — decompensation is gradual, making longitudinal tracking high-value
- Clinically validated thresholds already exist (NYHA classification, ACC/AHA guidelines)
- Clear readmission problem — 30-day hospital readmission rate is a known pain point
- Compelling demo story: detect early decompensation before a crisis occurs
- Fewer direct AI competitors compared to diabetes

### Challenges
- Target patients are often elderly — UX must be simple
- Agent needs clinical profile baseline at onboarding to calibrate relevance
- Doctor trust — summaries must be traceable back to raw data
- Compliance drop-off with daily active engagement; rely on passive triggers
- Regulatory framing: must position as decision support, not diagnostic tool

---

### CHF Signals to Collect (Demo-Specific)

| Signal | Collection Method | Clinical Threshold / Relevance |
|--------|-------------------|-------------------------------|
| Daily Weight | Smart scale (passive) | Gain >2kg in 2 days = escalation trigger |
| Heart Rate | Smartwatch/wearable (passive) | Resting HR elevation above baseline |
| SpO2 (Blood Oxygen) | Smartwatch/pulse oximeter (passive) | Drop below 94% warrants attention |
| Breathlessness (Dyspnea) | Active: agent asks patient | Worsening on exertion or at rest |
| Ankle/Leg Swelling | Active: agent asks patient | Sign of fluid retention (edema) |
| Orthopnea | Active: agent asks patient | Difficulty lying flat — classic CHF signal |
| Fatigue Level | Active: agent asks (daily check-in) | Declining energy = early decompensation |
| Medication Adherence | Active: agent confirms | Missed diuretics can trigger fluid buildup |
| Activity Level | Smartwatch step count (passive) | Sudden drop may indicate worsening status |

---

### Context-Awareness Design (CHF Example)

The agent does NOT ask every patient the same questions every day. It calibrates based on three layers:

### 1. Patient Clinical Profile (Onboarding Context)
At setup, agent ingests baseline profile: NYHA class, current medications, ejection fraction, comorbidities. A NYHA Class II patient has different alert thresholds than a Class IV patient.

### 2. Signal-Triggered Inquiry
Active prompts are triggered by passive anomalies:
- Smart scale shows +2kg in 48 hours → agent asks about breathlessness, ankle swelling, sleep position
- Resting HR elevated above 7-day baseline → agent asks about fatigue and activity tolerance
- SpO2 drops below 94% → agent asks about chest tightness, prompts patient to rest and recheck

### 3. Pre-Visit Synthesis
Before scheduled doctor visits, agent compiles a SOAP-format summary:
- **Subjective** — patient-reported symptoms and check-in responses
- **Objective** — passive wearable data trends (weight curve, HR, SpO2)
- **Assessment** — agent-flagged anomalies and alert events
- **Plan** — recommended discussion points for physician

Every claim in the summary is traceable to raw data.

---

## Tech Stack

- **Database:** Supabase (Postgres)
- **Backend/Workflows:** n8n
- **Frontend:** Streamlit (for demo speed)
- **AI:** Claude (via Anthropic API)

---

## Database Schema (6 Tables)

### 1. Users
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  age INTEGER,
  disease_profile JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**disease_profile JSONB structure:**
```json
{
  "diseases": [
    {
      "name": "CHF",
      "nyha_class": "II",
      "ejection_fraction": "40%",
      "comorbidities": ["hypertension", "diabetes"],
      "metrics": ["daily_weight", "heart_rate", "spo2", "bp_systolic", "bp_diastolic"],
      "thresholds": {
        "daily_weight": "gain >2kg in 2 days",
        "spo2": "below 94%",
        "heart_rate": "resting HR >20% above baseline",
        "bp_systolic": "above 180 or below 90",
        "bp_diastolic": "above 120 or below 60"
      },
      "symptom_options": ["shortness_of_breath", "ankle_swelling", "fatigue", "chest_discomfort", "dizziness", "night_coughing"],
      "mood_options": ["great", "good", "okay", "bad", "struggling"]
    }
  ],
  "medications": [
    {"name": "Lisinopril", "dosage": "10mg", "times": ["08:00"]},
    {"name": "Carvedilol", "dosage": "25mg", "times": ["08:00"]},
    {"name": "Furosemide", "dosage": "40mg", "times": ["08:00", "14:00", "20:00"]}
  ]
}
```

**Key fields:**
- `metrics` — What to track (required, system depends on this)
- `thresholds` — When to alert, stored as text, AI interprets (required)
- `nyha_class`, `ejection_fraction`, `comorbidities` — Context for AI reasoning (optional but recommended)
- `symptom_options` — AI-generated during onboarding based on disease, shown as checklist in Track tab
- `mood_options` — Fixed options for mood tracking, shown as dropdown in Track tab
- `medications` — Extracted from documents during onboarding

---

### 2. Metrics (Daily User-Inputted Vitals)
```sql
CREATE TABLE metrics (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  readings JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, date)
);
```

**readings JSONB example:**
```json
{
  "weight": 75.5,
  "bp_systolic": 131,
  "bp_diastolic": 80,
  "mood": "okay",
  "symptoms": ["fatigue", "my jaw feels tight"]
}
```

**Notes:**
- One row per user per day
- User inputs via Track tab in frontend
- `mood` — Fixed enum: `["great", "good", "okay", "bad", "struggling"]`
- `symptoms` — Array, mix of preset options (from `disease_profile.symptom_options`) + custom user input

---

### 3. Documents (OCR-Extracted PDFs)
```sql
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  document_name TEXT NOT NULL,
  content TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Notes:**
- `document_name` — AI-generated descriptive name (e.g., "EHR - Discharge Summary (Jan 2024)")
- `content` — AI-processed string representation optimized for future AI context
- AI can browse by `document_name` first, then read `content` when needed
- Typically 2 rows per user: EHR + Doctor transcript

---

### 4. Personal Info (AI-Extracted Notable Events from Chat)
```sql
CREATE TABLE personal_info (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  extracted_info TEXT
);
```

**Example rows:**
| id | user_id | timestamp | extracted_info |
|----|---------|-----------|----------------|
| 1 | 1 | 2026-03-17 03:12:00 | "Felt bloated, couldn't sleep" |
| 2 | 1 | 2026-03-17 14:30:00 | "Headache after taking medication" |
| 3 | 1 | 2026-03-18 09:00:00 | "Felt better after rest, swelling reduced" |

**Notes:**
- AI extracts notable events from chat conversations
- Used by Health Check workflow to detect patterns
- Used by Export workflow for Subjective section of SOAP summary

---

### 5. Medications (Daily Adherence Tracking)
```sql
CREATE TABLE medications (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  taken JSONB,
  UNIQUE(user_id, date)
);
```

**taken JSONB example:**
```json
{
  "Lisinopril": {"08:00": true},
  "Carvedilol": {"08:00": true},
  "Furosemide": {"08:00": true, "14:00": false, "20:00": true}
}
```

**Notes:**
- One row per user per day (same pattern as Metrics)
- Med list and schedule stored in `users.disease_profile.medications`
- This table only tracks adherence (taken/not taken per time slot)

---

### 6. Wearables (Raw Device Data)
```sql
CREATE TABLE wearables (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  raw_data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**raw_data JSONB example (mimics real wearable API response):**
```json
{
  "heart_rate": {
    "value": 72,
    "unit": "bpm",
    "timestamp": "2026-03-17T14:30:00Z"
  },
  "spo2": {
    "value": 96,
    "unit": "%",
    "timestamp": "2026-03-17T14:30:00Z"
  },
  "steps": {
    "value": 3200,
    "timestamp": "2026-03-17T00:00:00Z"
  }
}
```

**Notes:**
- Store raw API response as-is, AI parses when needed
- Multiple entries per day possible (passive, device-pushed)
- For demo: pre-populated with mock data

---

### Auto-Created by n8n: Chat History
n8n's **Postgres Chat Memory** node auto-creates `n8n_chat_histories` table:

| Column | Type | Description |
|--------|------|-------------|
| session_id | VARCHAR | Unique identifier for each conversation |
| message | JSONB | The message content in JSON format |
| created_at | TIMESTAMP | When the message was stored |

No need to manually define this table.

---

## Data Population

| Table | How It Gets Populated |
|-------|----------------------|
| `users` | Onboarding workflow: AI extracts from uploaded PDF |
| `metrics` | Frontend Track tab: user inputs daily |
| `documents` | Onboarding workflow: OCR extracts PDF text |
| `personal_info` | Chatbot workflow: AI extracts notable events from conversation |
| `medications` | Frontend Track tab: user confirms meds taken |
| `wearables` | Mock data pre-populated for demo (simulates device API) |
| `n8n_chat_histories` | Auto-managed by n8n Postgres Chat Memory node |

---

## n8n Workflows (4 Total)

### Workflow 1: Onboarding

**Trigger:** Webhook (called from frontend when user uploads PDF)

**Input:**
```json
{
  "user_name": "Marcus",
  "age": 67,
  "pdf_base64": "<base64 encoded PDF>"
}
```

**Flow:**
```
Webhook
  → Extract PDF text (OCR node or PDF parser)
  → AI Agent: Extract structured info from text
      - Prompt: "Extract disease name, NYHA class, ejection fraction, 
        comorbidities, medications (name, dosage, schedule), 
        recommended metrics to track, thresholds, common symptoms"
  → Insert into `users` table (name, age, disease_profile JSONB)
  → Insert into `documents` table (content = raw OCR text)
  → Insert into `medications` table (initial row with empty taken JSONB)
  → Return success + user_id
```

**Output:**
```json
{
  "success": true,
  "user_id": 1
}
```

---

### Workflow 2: Health Check (Cron + Tool)

**Trigger:** 
- Cron (every 6 hours)
- OR callable as tool from Chatbot workflow (on-demand)

**Input (if tool):**
```json
{
  "user_id": 1
}
```

**Flow:**
```
Trigger (Cron or Tool)
  → Query `users` table (get disease_profile, thresholds)
  → Query `metrics` table (last 7 days)
  → Query `wearables` table (last 48 hours)
  → Query `medications` table (last 3 days)
  → Query `personal_info` table (last 7 days)
  → AI Agent: Analyze all data against thresholds
      - Prompt: "Given this patient profile and data, 
        check for anomalies. If any threshold breached 
        or notable pattern, return alert message. 
        If nothing notable, return null."
  → IF alert exists:
      → Return alert message (for chatbot to send)
  → ELSE:
      → Return null (no action)
```

**Output:**
```json
{
  "alert": "Your weight increased 2.5kg in 2 days. How are you feeling? Any swelling or breathlessness?"
}
// OR
{
  "alert": null
}
```

---

### Workflow 3: Chatbot

**Trigger:** Chat Trigger (n8n chat interface / webhook from frontend)

**Input:**
```json
{
  "user_id": 1,
  "message": "I feel bloated and can't sleep"
}
```

**Flow:**
```
Chat Trigger
  → Postgres Chat Memory (auto-handles history)
  → AI Agent with tools:
      
      Tool 1: health_check
        - Calls Workflow 2 on-demand
        - Returns alert or null
      
      Tool 2: get_patient_context
        - Queries users, metrics, wearables, medications, documents
        - Returns summary for AI to reference
      
      Tool 3: log_notable_event
        - Inserts into personal_info table
        - Input: extracted_info text
      
  → AI responds to user
  → IF notable symptom mentioned:
      → Call log_notable_event tool
  → Return response
```

**Output:**
```json
{
  "response": "I'm sorry you're feeling bloated and having trouble sleeping. This could be related to fluid retention. Have you noticed any swelling in your ankles? Also, did you take your Furosemide today?"
}
```

**Chatbot Constraints:**
- Does NOT accept file uploads
- Does NOT let user input vitals directly in chat
- CAN remind user: "Go to Track tab to log your weight"
- CAN answer questions, provide support
- CAN extract notable info → save to Personal_Info

---

### Workflow 4: Export (Doctor Summary)

**Trigger:** Webhook (called from frontend Doctor tab)

**Input:**
```json
{
  "user_id": 1,
  "days": 14
}
```

**Flow:**
```
Webhook
  → Query `users` table (profile)
  → Query `metrics` table (last N days)
  → Query `wearables` table (last N days)
  → Query `medications` table (last N days)
  → Query `personal_info` table (last N days)
  → Query `n8n_chat_histories` (last N days, filtered by session)
  → AI Agent: Generate SOAP summary
      - Prompt: "Generate a clinical summary in SOAP format:
        - Subjective: patient-reported symptoms from chat/personal_info
        - Objective: vitals trends from metrics/wearables
        - Assessment: flagged anomalies, patterns
        - Plan: recommended discussion points
        Keep it concise, traceable to data."
  → Format as Markdown
  → Return summary
```

**Output:**
```json
{
  "summary_markdown": "## Patient Summary: Marcus...",
  "flagged_items": [
    "Weight gain 2.1kg over 3 days (Mar 12-15)",
    "Missed PM Furosemide on Mar 13, 14",
    "Reported ankle swelling on Mar 14"
  ]
}
```

---

## Frontend Overview (Streamlit for Demo)

**4 Tabs:**

### 1. Home Tab
- Greeting with user name, day count
- Status banner (overall health status, streak)
- Today's vitals (4 cards: BP, Weight, HR, SpO2 with status indicators)
- Medications list with taken/due status
- KAKI's Insight (AI-generated pattern observation)
- 7-day BP trend chart

### 2. KAKI (Chat) Tab
- Chat interface with AI companion
- Quick suggestion buttons
- Emergency detection (mental crisis → 988, vitals crisis → 911)

### 3. Track Tab
- **Log Today:** BP, Weight, Mood (5-point emoji), Symptoms (checklist + custom), Save button
- **Goals (optional):** Milestone cards (streak tracking)

### 4. Doctor Tab
- Doctor info, appointment countdown
- AI-generated SOAP summary
- 7-day trend charts (BP, Weight)
- Flagged items for discussion
- Share button

---

## Demo Scope

**MVP demonstrates the full loop for one CHF patient scenario:**
1. Passive signal anomaly (weight +2kg in wearables)
2. Triggered inquiry (chatbot asks about symptoms)
3. User reports symptoms in chat
4. AI extracts and logs notable events
5. Pre-visit summary generated in SOAP format
6. Doctor can see traceable summary

**Demo Patient:** Marcus, 67, CHF NYHA Class II

---

## Key Design Decisions

1. **Thresholds as text, AI interprets** — Flexible, no hardcoded logic in cron job
2. **One reusable Health Check workflow** — Called by cron (scheduled) and chatbot (on-demand)
3. **Symptoms: preset + custom** — AI generates common symptoms during onboarding, user can add custom
4. **Mood: fixed enum** — `["great", "good", "okay", "bad", "struggling"]`
5. **Wearables: store raw API response** — Mimic real device output, AI parses when needed
6. **Chat history: auto-managed by n8n** — Uses Postgres Chat Memory node with Supabase
7. **Personal Info: AI-extracted from chat** — Only notable events, not every message
8. **Medications: schedule in users table, adherence in medications table** — Separation of concerns

---

## Next Steps

1. ✅ Database schema designed
2. ⬜ Create schema in Supabase
3. ⬜ Create mock data for Marcus
4. ⬜ Build n8n workflows (Onboarding → Health Check → Chatbot → Export)
5. ⬜ Build Streamlit frontend
6. ⬜ End-to-end testing
7. ⬜ Prepare demo narrative for judges

---

## Reminders

- **OCR-based onboarding** for documents
- All IDs use `SERIAL` (auto-increment integer), not UUID
- n8n + Supabase connection uses Postgres Chat Memory node
- For demo: wearables data is pre-populated mock data
