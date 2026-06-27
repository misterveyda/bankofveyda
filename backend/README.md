<<<<<<< HEAD
"""Bank of Veyda Backend - Compliance Simulator

A sophisticated fintech simulator demonstrating KYC/AML compliance, account lifecycle management,
and risk scoring for temporary financial identities.

## Project Structure

```
backend/
├── app/
│   ├── models/          # SQLAlchemy models (Account, KYC, Transaction, Audit, RiskScore)
│   ├── schemas/         # Pydantic request/response schemas
│   ├── api/             # FastAPI endpoints
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── accounts.py      # Account management endpoints
│   │       │   └── transactions.py  # Transaction endpoints
│   │       └── router.py
│   ├── services/        # Business logic
│   │   ├── account_service.py       # Account operations
│   │   ├── kyc_service.py          # KYC verification (Onfido integration)
│   │   ├── risk_engine.py          # Dynamic risk scoring
│   │   ├── banking_service.py      # BaaS integrations (Stripe, Plaid)
│   │   └── lifecycle_engine.py     # TTL expiration & cleanup
│   ├── workers/         # Celery background tasks
│   ├── utils/           # Helper utilities
│   ├── config.py        # Settings and configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI app factory
├── tests/               # Unit and integration tests
├── requirements.txt     # Python dependencies
├── run.py              # Application entry point
├── docker-compose.yml  # Docker services (PostgreSQL, Redis)
└── Dockerfile          # Application containerization
```

## Key Features

### 1. Time-Locked Accounts
- Every account has a TTL (Time-To-Live) in days
- Automated expiration and closure enforcement
- Educational: Demonstrates regulatory constraints

### 2. KYC Integration (Sandbox)
- Onfido sandbox integration for identity verification
- Document upload and verification workflow
- Educational: Shows why KYC is the bottleneck for anonymous accounts

### 3. Risk Scoring Engine
- Dynamic fraud detection (0-100 score)
- Multiple risk factors:
  - KYC risk assessment
  - Transaction velocity monitoring
  - High-value transaction detection
  - Geographic anomaly detection
  - Pattern anomaly detection (structuring, smurfing)

### 4. Account Lifecycle Management
- PENDING_KYC → ACTIVE → FROZEN/EXPIRED → CLOSED
- Automated cleanup on expiration
- Balance return-to-source on closure

### 5. Audit Trail
- Immutable compliance logging
- Every action tracked with timestamp, IP, device fingerprint
- Educational: Shows why privacy is impossible in finance

### 6. Background Workers
- Celery + Redis for scheduled tasks
- Automatic account cleanup (hourly)
- Risk score recalculation
- Expiration notifications

## Setup & Running

### Prerequisites
- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- Docker & Docker Compose (optional)

### Local Development

1. **Clone and setup virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start PostgreSQL and Redis:**
```bash
docker-compose up -d postgres redis
```

5. **Run database migrations (first time):**
```bash
alembic upgrade head
```

6. **Start the API server:**
```bash
python run.py
```

Server runs on `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Running with Docker

```bash
docker-compose up
```

This starts:
- FastAPI application (port 8000)
- PostgreSQL database (port 5432)
- Redis (port 6379)
- Celery worker

## API Endpoints

### Accounts

**Create Burner Account**
```
POST /api/v1/accounts/create
{
  "account_holder_name": "John Doe",
  "ttl_days": 30,
  "creation_ip": "192.168.1.1",
  "creation_device_fingerprint": "device_hash"
}
```

**Get Account Details**
```
GET /api/v1/accounts/{account_id}
```

**Submit KYC**
```
POST /api/v1/accounts/{account_id}/kyc/submit
{
  "full_name": "John Doe",
  "date_of_birth": "1990-01-01",
  "country": "US",
  "document_type": "passport",
  "document_number": "ABC123456",
  "document_expiry": "2030-12-31"
}
```

**Check KYC Status**
```
GET /api/v1/accounts/{account_id}/kyc/status
```

**Freeze Account**
```
POST /api/v1/accounts/{account_id}/freeze
```

### Transactions

**Submit Transaction**
```
POST /api/v1/transactions/{account_id}/submit
{
  "type": "transfer_out",
  "amount": 1000.00,
  "counterparty_name": "John Smith",
  "counterparty_account": "12345678901234567",
  "counterparty_routing": "021000021",
  "description": "Payment for services"
}
```

**Get Transaction History**
```
GET /api/v1/transactions/{account_id}/history
```

## Database Schema

### BurnerAccount
- Core account information
- TTL configuration (expires_at, ttl_days)
- Status tracking (pending_kyc, active, frozen, expired, closed)
- Risk scores and flags
- Integration IDs (stripe_account_id, plaid_account_id)

### KYCVerification
- User identity information
- Document details
- Verification status and provider (Onfido)
- Audit trail

### Transaction
- Account transactions (deposits, withdrawals, transfers)
- Counter-party information
- Status tracking
- Audit references

### AuditLog
- Immutable compliance records
- Event types and descriptions
- User context (IP, device, user agent)
- Timestamps and severity

### RiskScore
- Risk assessment records
- Component scores (KYC, velocity, high-value, geographic, pattern)
- Risk factors and recommended actions
- Recommendations

## Educational Insights

### Why Anonymous Accounts Don't Exist
1. **KYC Requirement**: Every account requires identity verification
2. **Audit Trail**: Every transaction is logged with IP/device info
3. **TTL Enforcement**: Accounts have expiration dates
4. **Risk Monitoring**: Automatic detection of suspicious patterns
5. **Data Retention**: Regulatory compliance requires long-term data storage

### Key Compliance Concepts Demonstrated
- Know Your Customer (KYC) requirements
- Anti-Money Laundering (AML) monitoring
- Transaction velocity analysis
- Structuring detection
- Geographic risk assessment
- Real-time risk scoring

## Configuration

All settings are environment-based (.env file):

```
DATABASE_URL=postgresql://user:password@localhost:5432/bankofveyda
REDIS_URL=redis://localhost:6379/0
STRIPE_API_KEY=sk_test_...
ONFIDO_API_TOKEN=your_token
PLAID_CLIENT_ID=your_id
PLAID_SECRET=your_secret
DEFAULT_ACCOUNT_TTL_DAYS=30
RISK_SCORE_THRESHOLD=75
```

## Testing

Run tests with pytest:

```bash
pytest tests/
```

## Development

Code style with Black:
```bash
black .
```

Type checking with mypy:
```bash
mypy app/
```

Linting with flake8:
```bash
flake8 app/
```

## License

MIT License - See LICENSE file

## Contributing

This is an educational project demonstrating fintech compliance concepts.
"""

print(__doc__)
=======
# Bank of Veyda Backend

This directory contains a Django backend for the Bank of Veyda fintech/regtech simulation.

## Getting Started

### Option 1: Local virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

### Option 2: Docker Compose

```bash
cd backend
docker compose up --build
```

Then open http://localhost:8000.

### Django frontend

- The dashboard is available at `/`
- The new account request page is available at `/request-account/`

### Seed sample data

```bash
python manage.py seed_data
```

### Notes

- The app expects Postgres on `db:5432` when running in Docker.
- Use `.env.example` to provide local database credentials.
>>>>>>> db7bb07 (commit)
