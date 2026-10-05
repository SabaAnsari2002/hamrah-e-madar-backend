# V1 API endpoint inventory

All endpoints below are JSON under `/api/v1/` unless noted. JWT authentication is required except OTP request/verify and token refresh.

| Path | Methods | Purpose |
|---|---|---|
| `auth/otp/request/` | POST | Generate hashed, expiring OTP challenge |
| `auth/otp/verify/` | POST | Verify single-use OTP and issue access/refresh JWTs |
| `auth/token/refresh/` | POST | Refresh access token |
| `auth/logout/` | POST | Blacklist refresh token |
| `me/` | GET, PATCH, DELETE | Current user profile / actual account deletion |
| `pregnancies/` | GET, POST | User pregnancy history / create pregnancy |
| `pregnancies/{id}/` | GET, PATCH | User-owned pregnancy detail |
| `pregnancy/current/` | GET | Current active pregnancy |
| `pregnancy/weeks/` | GET | Curated pregnancy week content |
| `pregnancy/weeks/{week}/` | GET | Week 1–40 detail |
| `dashboard/today/` | GET | Aggregate Home payload |
| `health/summary/` | GET | Latest weight/BP/glucose and today's symptom count |
| `health/weights/` | GET, POST | Weight history/create |
| `health/weights/{id}/` | GET, PATCH, DELETE | Weight detail/update/delete |
| `health/blood-pressures/` | GET, POST | BP history/create |
| `health/blood-pressures/{id}/` | GET, PATCH, DELETE | BP detail/update/delete |
| `health/blood-glucose/` | GET, POST | Glucose history/create |
| `health/blood-glucose/{id}/` | GET, PATCH, DELETE | Glucose detail/update/delete |
| `health/symptoms/` | GET, POST | Symptom history/create |
| `health/symptoms/{id}/` | GET, PATCH, DELETE | Symptom detail/update/delete |
| `visits/` | GET, POST | Prenatal visits |
| `visits/{id}/` | GET, PATCH, DELETE | Visit detail/update/delete |
| `visits/{id}/questions/` | GET, POST | Visit questions |
| `visit-questions/{id}/` | PATCH, DELETE | Edit/mark answered/delete question |
| `labs/` | GET, POST | Lab records |
| `labs/{id}/` | GET, PATCH, DELETE | Lab detail/update/delete |
| `labs/{id}/attachment/` | GET | Authenticated owner-only file download |
| `ultrasounds/` | GET, POST | Ultrasound records |
| `ultrasounds/{id}/` | GET, PATCH, DELETE | Ultrasound detail/update/delete |
| `ultrasounds/{id}/attachment/` | GET | Authenticated owner-only file download |
| `medications/` | GET, POST | Medication/supplement records |
| `medications/{id}/` | GET, PATCH, DELETE | Medication detail/update/delete |
| `medications/{id}/today-completion/` | POST | Record today's user-reported completion |
| `care/tasks/` | GET | User care tasks |
| `care/tasks/{id}/` | PATCH | Complete/skip task |
| `articles/` | GET | Published articles only; category/week filters |
| `articles/{slug}/` | GET | Published article detail |
| `reminders/` | GET, POST | Reminder CRUD |
| `reminders/{id}/` | GET, PATCH, DELETE | Reminder detail/update/delete |
| `records/summary/` | GET | Concise visit/lab/ultrasound/medication summary |

Development-only API documentation lives at `/api/schema/` and `/api/docs/`.

## Common filtering/ordering

Health measurements accept `date_from`, `date_to`, `pregnancy`, and resource-specific filters plus safe `ordering` such as `-measured_at`. Visits/labs/ultrasounds accept date filters and relevant status/type filters. Reminders accept type/completion/pregnancy/date filters. Articles accept `category` (machine code) and `week`.

## Medical-safety behavior

These endpoints store and retrieve user-entered or curated records. They do not diagnose disease, interpret measurements as a diagnosis, prescribe medication, or alter treatment. Medical content publication is controlled by content administrators and draft content is not returned to normal users.
