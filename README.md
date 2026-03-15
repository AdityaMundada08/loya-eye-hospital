# Loya Eye Hospital – Website

Production-ready website for an eye hospital in Tier 2/3 Maharashtra. Django + PostgreSQL + Bootstrap. Mobile-first, SEO-focused, WhatsApp integration.

## Tech Stack

- **Backend:** Python Django 4.2
- **DB:** PostgreSQL
- **Frontend:** Django Templates + Bootstrap 5 (CDN)
- **Hosting:** Render / DigitalOcean
- **CMS:** Django Admin

## Features

- **Pages:** Home, About, Treatments, Contact, Location, FAQ, Testimonials, Blog
- **Individual treatment pages** (e.g. `/treatments/cataract-surgery/`) for SEO
- **Appointment form** → saves to DB + optional email to admin
- **WhatsApp** link (nav + footer)
- **Schema markup** (MedicalOrganization, MedicalProcedure)
- **Sitemap** and **robots.txt**
- **Mobile-first**, minimal JS, fast load

## Setup (Local)

1. **Clone and create virtualenv**
   ```bash
   cd loya_eye_hospital
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **PostgreSQL**
   - Create database: `createdb loya_eye_db`
   - Copy `.env.example` to `.env` and set:
     - `SECRET_KEY`, `DEBUG=True`, `ALLOWED_HOSTS=localhost,127.0.0.1`
     - `DB_NAME=loya_eye_db`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

3. **Migrations and run**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

4. **Admin:** http://127.0.0.1:8000/admin/  
   - Add **Site Settings** (one row: hospital name, phone, WhatsApp, address, map embed, hours).
   - Add **Doctors**, **Treatments** (with slugs, e.g. `cataract-surgery`, `lasik-surgery`), **Treatment FAQs**, **Testimonials**, **FAQs**, **Blog** as needed.

## Deployment (Render / DigitalOcean)

- Set `DEBUG=False`, strong `SECRET_KEY`, `ALLOWED_HOSTS=yourdomain.com`
- Use `DATABASE_URL` (PostgreSQL) or `DB_*` env vars
- Static: `python manage.py collectstatic` (WhiteNoise serves them)
- Start: `gunicorn config.wsgi:application`
- Add **Google My Business**, update **Site Settings** with real contact and map embed

## URL Structure (Treatments – SEO)

- List: `/treatments/`
- Detail: `/treatments/cataract-surgery/`, `/treatments/lasik-surgery/`, etc. (use **slug** in Admin)

## Environment Variables (.env)

| Variable | Description |
|----------|-------------|
| SECRET_KEY | Django secret key |
| DEBUG | True/False |
| ALLOWED_HOSTS | Comma-separated hosts |
| DATABASE_URL or DB_* | PostgreSQL connection |
| EMAIL_* | Optional; for appointment email to admin |

## License

Private / use as needed.
