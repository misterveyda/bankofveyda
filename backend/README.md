# Bank of Veyda Backend

A Django-based fintech compliance simulator for account lifecycle management, KYC workflows, risk monitoring, and governance dashboards.

## Project structure

- `config/` — Django settings and URL configuration
- `core/` — Django app with models, forms, views, and templates
- `templates/` — shared HTML templates and auth pages
- `manage.py` — Django management entry point
- `Dockerfile` — container image build
- `docker-compose.yml` — local development services
- `requirements.txt` — Python dependencies

## Local development

1. Activate your environment:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Docker development

Build and run the Django app with PostgreSQL:

```bash
docker compose up --build
```

## Main routes

- Home: `/`
- Dashboard: `/dashboard/`
- Login: `/login/`
- Sign up: `/signup/`
- Logout: `/logout/`
- Request account: `/request-account/`
- Compliance dashboard: `/compliance/`
- Password reset: `/password-reset/`

## Notes

- The active backend is the Django app under `config/` and `core/`.
- The root `/` view redirects unauthenticated users to `/login/` and authenticated users to `/dashboard/`.
- Dashboard, compliance, request-account, and JSON API views are protected by `login_required`.
- Password reset uses Django's built-in auth views with console email backend by default.

## Cleanup observation

This repository still contains legacy FastAPI-related files under `app/` and `run.py` that are not part of the active Django backend. Those can be removed once the Django direction is finalized.

## License

MIT License
