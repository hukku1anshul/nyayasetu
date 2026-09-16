# NyayaSetu (Adhikar AI)
*India's Hybrid Legal, Compliance & G2C Bureaucracy Digitization Platform*

NyayaSetu automates high-friction offline legal and compliance workflows across India, bridging the gap between central/state online portals and real-world execution.

---

## What All Features Have We Added? (What Users Can Do)

### 1. Dual Lead Intake Channels
* **WhatsApp Business Conversational Bot (`/webhook/whatsapp`)**:
  - Citizens can apply for Gazette name change or recover lost shares via a 2-minute WhatsApp conversation.
  - Multi-turn state machine handling identity extraction, statutory register lookup, document photo intake, and instant docket issuance (e.g. `#NS-GAZ-9921`).
* **Web & Mobile Intake Portal (`/api/v1/intake/web-submit`)**:
  - Structured web intake API for onboarding citizens and legal heirs, validating KYC inputs, and tracking real-time case dockets (`/api/v1/intake/docket/{docket_id}`).

### 2. National High-Volume Rail: Central Gazette & Identity Rectification
* **Live e-Gazette Client (`egazette.gov.in`)**: Direct connection to official Category 4 (Part-IV: Private Individuals) gazettes at IP `164.100.190.144` without third-party scrapers.
* **Automated Affidavit Drafting**: Instant statutory affidavit generation compliant with Controller of Publications guidelines.
* **Newspaper Syndication**: Formatted classified notices for National English and State Vernacular dailies.
* **Status Verification**: Automatically searches published gazettes to confirm when a citizen's official notification has dropped.

### 3. High-Ticket Unclaimed Wealth Rail: IEPF & Deceased Share Recovery
* **MCA/IEPF Cryptographic Engine**: Reverse-engineered and implemented the Ministry of Corporate Affairs' PBKDF2/AES-128-CBC encryption scheme (`clientlibs-encrptdecrypt.min.js`) in native Python, connecting to `iepf.gov.in` without paid API subscriptions.
* **SEBI Statutory Dossier Generator**: Auto-generates the entire paperwork package at zero software cost:
  - **Form ISR-1**: KYC & Bank details registration.
  - **Form ISR-2**: Banker signature verification format.
  - **Form-A Affidavit**: Statutory legal heir declaration.
  - **Form-B Indemnity Bond**: ₹500 NeSL-format indemnity with two sureties.
  - **Form IEPF-5**: MCA21 electronic refund claim form.
* **Contingency Fee Engine**: Dynamic 12%–20% success fee calculator with zero upfront financial burden on families.

### 4. Local RTA (Registrar & Transfer Agent) Expansion
* **RTA Registry Directory**: Maps 100+ top Indian listed companies (Tata Steel, Reliance, Infosys, ITC, SBI, HDFC) to their designated RTA (Link Intime, KFintech, Datamatics, In-House).
* **Statutory Public Unclaimed Register Search**: Searches statutory registers mandated by Section 124(2) of the Companies Act to find matching deceased shareholder folios and unclaimed dividend balances.
* **SEBI Form ISR-4 Auto-Generator**: Generates Form ISR-4 for requesting duplicate share certificates or letters of confirmation in lieu of lost paper shares.

### 5. Cross-Border MEA Apostille & Municipal Commercial Hub
* **MEA Apostille Vault Tracker**: Visual milestone tracking (Doorstep Vault -> University OCR -> State HRD -> MEA Apostille -> Embassy Legalization).
* **Hyper-Local Municipal Launchpad**: Turnkey commercial licensing (Trade License, Fire NOC, Shop & Est, FSSAI) across BBMP (Bengaluru), BMC (Mumbai), MCD (Delhi), and GHMC (Hyderabad).

---

## Quickstart & Verification

### Running the Test Suite (All 8 Suites Verified)
```bash
python tests/test_engines.py
```

### Starting the FastAPI Server
```bash
uvicorn nyayasetu.api:app --reload --port 8000
```
API Documentation will be available at `http://localhost:8000/docs`.
