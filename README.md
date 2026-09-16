# NyayaSetu & CardSmart Unified Platform (v1.8.0)
*India's Hybrid Legal, Compliance, FinTech & Consumer Protection Platform*

[![GitHub repo](https://img.shields.io/badge/GitHub-hukku1anshul%2Fnyayasetu-blue?logo=github)](https://github.com/hukku1anshul/nyayasetu)
[![Render Auto-Deploy](https://img.shields.io/badge/Render-Auto--Deploy-success?logo=render)](https://render.com)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

NyayaSetu unites consumer legal rights, statutory tax advisory, RBI 2025 compliant digital lending comparison, credit card reward maximization, and zero-cost public G2C registry lookup into a single lightning-fast platform.

---

## 🚀 Live Cloud Deployment & Render Auto-Sync

This repository is configured for **continuous deployment on Render**:
- **GitHub Repository**: [`https://github.com/hukku1anshul/nyayasetu`](https://github.com/hukku1anshul/nyayasetu)
- **Render Configuration**: [`render.yaml`](./render.yaml) specifies automated builds on branch `main` (`autoDeploy: true`).
- **Trigger**: Any commit pushed to `origin main` automatically initiates a cloud build and deployment on Render with zero downtime.
- **Health Check Endpoint**: `/health` (monitored automatically by Render and Docker).

### Render Service Specifications
| Setting | Value |
| :--- | :--- |
| **Service Name** | `nyayasetu-cardsmart` |
| **Environment** | Python 3.12 (via `.python-version` & `render.yaml`) |
| **Build Command** | `pip install --upgrade pip && pip install -r requirements.txt` |
| **Start Command** | `uvicorn nyayasetu.api:app --host 0.0.0.0 --port $PORT` |
| **Health Check Path** | `/health` |
| **Region** | Singapore (`singapore` - Lowest latency to India on Render free tier) |

---

## 🌟 Core Engines & Modules

### 1. 🤝 Loan Mitra — RBI 2025 Digital Lending Framework
* **Multi-Lender Web Aggregation**: Complies with RBI Directions prohibiting dark patterns, stealth insurance cross-sells, and biased lender rankings.
* **Statutory Key Fact Statement (KFS)**: Real-time calculation of **APR (Annual Percentage Rate)** encompassing all processing fees, verification fees, documentation charges, and GST.
* **Floating Rate Foreclosure Protection**: Transparently flags zero foreclosure penalty mandates on floating-rate individual loans.
* **Balance Transfer Optimizer**: Computes net tenure compression and total interest savings factoring in switching costs.
* **Lead CRM (`/api/v1/loans/apply`)**: Direct multi-lender lead dispatch with docket generation.

### 2. 💳 CardSmart — Credit Card Personalized ROI Marketplace
* **Multi-Dimensional Matching Engine**: Takes monthly income, spending split (dining, travel, shopping, groceries, fuel), lounge needs, and annual fee tolerance.
* **Net Value Proposition Formula**:
  $$\text{Net Annual Value} = \text{Welcome Benefits} + \text{Annual Rewards/Cashback} + \text{Lounge Value} + \text{Fuel Surcharge Waiver} - \text{Annual Fee}$$
* **Break-Even Spend Calculator**: Exact spend required to negate the annual card membership fee.

### 3. ⚖️ AI Vakil & CA India Suite (Statutory Legal & Tax Engines)
* **Section 138 NI Act Cheque Bounce Notice**: Automated statutory 15-day demand notice compliant with Supreme Court guidelines.
* **Section 106 TPA Eviction / Arrears Notice**: 15-day tenancy termination and statutory mesne profit demand.
* **Employment Contract Non-Compete Risk Auditor**: Flags post-termination covenants void under **Section 27 of Indian Contract Act, 1872** (*Percept D'Mark v. Zaheer Khan*).
* **FY 2026-27 Tax Regime Decider**: Side-by-side Section 115BAC New vs Old Regime with Chapter VI-A deductions and breakeven threshold.
* **Section 44ADA Presumptive Taxation**: 50% deemed profit calculation with mandatory quarterly advance tax calendar (15% Jun 15, 45% Sep 15, 75% Dec 15, 100% Mar 15).
* **Plain-English IT Notice Explainer**: Explains Section 143(1), 139(9), 148, and 156 demand notices with statutory response deadlines.

### 4. 🇮🇳 Real-Time Zero-Cost Public Rails
* **Razorpay Open IFSC API Client**: Instant bank, branch, RTGS/NEFT/IMPS/UPI support lookup without paid third-party aggregators.
* **India Post Pincode Rails**: Resolves Indian postal pincodes to exact post office, circle, district, and state.
* **Section 139A PAN Entity Decoder**: Decodes the 4th character entity type (Company, Individual, HUF, Firm, AOP, Trust) and verifies checksum format.
* **15-Digit GSTIN Jurisdiction Decoder**: Extracts state jurisdiction, PAN link, and tax entity type.

### 5. 🏛️ NyayaSetu Bureaucracy Digitization
* **Central e-Gazette Live Client**: Direct client for Category 4 (Private Individuals) name and gender change notifications.
* **MCA/IEPF Unclaimed Asset Recovery**: Native implementation of MCA PBKDF2/AES-128-CBC encryption scheme for Form IEPF-5, Form ISR-1, and Form-B indemnity bonds.
* **RTA Statutory Directory**: Company-to-RTA mapping (Link Intime, KFintech, Datamatics) for duplicate share recovery (SEBI Form ISR-4).
* **Free Consumer Viral Tools**: Statutory Section 10(13A) HRA Rent Exemption calculator, Hindu Succession Act share distribution engine, and Vehicle RTO radar.

### 6. 👤 User Experience & History
* **Persona Switcher**: Switch between *Aditya Verma (Salaried IT Techie)*, *Priya Sharma (Tech Freelancer)*, *Kunal Deshmukh (SME Founder)*, and *Guest*.
* **Persistent Activity History**: Local browser storage preserving all tool calculations and queries, with real-time category filtering and JSON audit export.
* **Companion Cross-Linking**: Direct navigation to companion Next.js portal (`vakil-ca-india`).

---

## 🧪 Testing & Verification

Run the comprehensive unit test suites:
```bash
# Engine unit test suite (15+ engine tests)
python tests/test_engines.py

# REST API endpoint live integration tests (10 endpoints)
python tests/test_api_endpoints.py
```

---

## 💻 Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hukku1anshul/nyayasetu.git
   cd nyayasetu
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**:
   ```bash
   uvicorn nyayasetu.api:app --reload --port 8000
   ```
   Access the dashboard at `http://localhost:8000` and interactive API docs at `http://localhost:8000/docs`.

