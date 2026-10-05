# Hamrah-e-Madar Django REST API

Independent local backend for the same future Hamrah-e-Madar product. Android is **not connected** to this API in the current phase.

## Stack

Python, Django 5.2 LTS, Django REST Framework, SimpleJWT with refresh-token blacklist, django-filter, drf-spectacular, and SQLite for local development. There is no Docker, Redis, Celery, WebSocket, Firebase, payment/subscription, AI, analytics, or cloud deployment configuration.

## Setup

```bash
python -m venv .venv
# activate the environment
pip install -r requirements.txt
cp .env.example .env   # or export equivalent environment variables
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

The application reads `DEBUG`, `SECRET_KEY`, and `ALLOWED_HOSTS` directly from the environment. `.env.example` documents values, but the project does not require a settings helper package.

Development schema/docs:

- `/api/schema/`
- `/api/docs/`

## Demo authentication

Seed user: `09120000000` / display name `Sara`.

OTP endpoints:

```text
POST /api/v1/auth/otp/request/
POST /api/v1/auth/otp/verify/
POST /api/v1/auth/token/refresh/
POST /api/v1/auth/logout/
```

When and only when `DEBUG=True`, the deterministic local OTP is **123456** and `ConsoleSMSProvider` may print it to development console output. The raw OTP is never stored in the database: a Django password hash is stored instead. OTP TTL is 2 minutes, maximum verification attempts are 5, resend cooldown is 60 seconds, codes are single-use, and basic phone/IP database-backed request limits are enforced. A production SMS implementation must replace the development provider; the DEBUG code path is not enabled when DEBUG is false.

## Apps and architecture

- `accounts`: custom UUID user, phone identity, OTP/JWT, account deletion
- `pregnancies`: lifetime pregnancy records, one-active-pregnancy rule, gestational calculation, week content
- `health`: weight, structured blood pressure, blood glucose, symptoms
- `records`: visits/questions, labs, ultrasounds, medications and protected local attachment download
- `care`: curated task templates and pregnancy-specific tasks
- `content`: categories and published-only articles
- `reminders`: reminder CRUD only; no push infrastructure
- `audit`: minimal account/security action metadata, never full medical record contents
- `dashboard`: optimized aggregate reads for Home

Business logic lives in services/selectors rather than views where it is meaningful: OTP lifecycle, pregnancy age, pregnancy creation, care-plan generation, and dashboard aggregation.

## Ownership and privacy

Every user-owned queryset is scoped through the authenticated user. Pregnancy-owned viewsets use a reusable ownership mixin that verifies the submitted pregnancy belongs to the caller. Object IDs alone never grant access. Cross-user tests cover health and record resources.

The API does not intentionally log OTPs (outside the explicit DEBUG console SMS provider), JWTs, medical notes/results, symptom details, or uploaded files. Attachment serializers never expose filesystem paths. Lab/ultrasound files are downloadable only through authenticated, owner-scoped API actions. Do not expose `MEDIA_ROOT` with a public static URL in production.

## Local media

Lab and ultrasound uploads allow PDF/JPG/JPEG/PNG up to 5 MB. Local filesystem storage exists only for development. Production must use private object storage with access control and an appropriate malware/content-scanning policy.

## API conventions

All mobile endpoints are under `/api/v1/`. JSON dates/times are ISO-8601. English machine enums are stable; Persian display labels belong to Android. List endpoints use page-number pagination (default 20, max 100), safe ordering fields, and filters where useful. The standard exception handler returns:

```json
{
  "code": "validation_error",
  "message": "The submitted information is invalid.",
  "errors": {"field_name": ["..."]}
}
```

Singleton/aggregate endpoints such as Dashboard and Health Summary are not paginated.

## Required endpoint groups

Implemented routes cover current user, pregnancies/current pregnancy/weeks, dashboard today, health summary and all four health resources, visits/questions, labs, ultrasounds, medications/today completion, care tasks, articles, reminders, and records summary. Router-generated detail routes provide GET/PATCH/DELETE where appropriate; pregnancy and care resources intentionally restrict methods to the product contract.

## Demo seed

`python manage.py seed_demo` creates a fresh active pregnancy around 24w3d and coherent demo records: 12 weights, 10 blood pressures, 8 glucose measurements, 15 symptoms, 4 visits, 7 labs, 4 ultrasounds, 5 medications/supplements, 15 reminders, 25 published demo articles plus 3 source-backed reference articles, 40 pregnancy weeks, and 120 user care tasks. Educational text is marked as demo content; fake medical authorities/sources are not created.

## Admin

Django Admin is configured for users, pregnancies, pregnancy-week content, categories/articles, care templates/tasks, visits/questions, labs, ultrasounds, medications and audit records with practical search/filter/list settings. Content administrators control publication state; normal API users receive published articles only.

## Tests and checks

Run:

```bash
python manage.py check
python manage.py test
```

Tests cover OTP request/expiry/wrong/used/attempt controls, JWT/logout/deletion, pregnancy age and active-pregnancy rules, health CRUD/summary/ownership, cross-user visit/lab/ultrasound isolation, published-only content, and dashboard response structure.

## PostgreSQL and production evolution

Model/query code avoids SQLite-specific application logic. Switching to PostgreSQL should primarily be a database settings/migration exercise. Production would additionally require a distributed rate limiter, real SMS provider, private object storage, hardened secret management, TLS/reverse proxy/application server, monitoring, backups, and a deployment pipeline. Those are intentionally not implemented in this phase.

## Local Android connectivity

For an Android Emulator running on the same development machine, the host Django server is reachable at `http://10.0.2.2:8000/` when Django is started with `runserver 0.0.0.0:8000`. For a physical device, use the development machine's LAN IPv4 address and include that address in the `ALLOWED_HOSTS` environment variable. See `LOCAL_RUN_FA.md` and the helper scripts under `scripts/`.

The seeded measurements and health records are synthetic/realistic test data, not records of real patients. Do not treat them as clinical reference data.

## CMS Panel
- Staff dashboard: `/cms/`
- Django admin: `/admin/`

## Google Sign-In API
- `POST /api/v1/auth/google/` with body `{ "id_token": "..." }`
- Configure `GOOGLE_OAUTH_CLIENT_IDS` with the allowed web client id(s).
