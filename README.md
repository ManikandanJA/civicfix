# CivicFix — Local Issue Reporting System

Basic Django + MySQL + Bootstrap project for reporting and tracking civic issues
(road damage, water leak, streetlight, garbage, drainage) in a local area.

## Setup

1. Create a virtual environment and install requirements:
   ```
   pip install django mysqlclient pillow
   ```

2. Create the MySQL database:
   ```sql
   CREATE DATABASE civicfix_db;
   ```

3. Update DB credentials in `civicfix/settings.py` → `DATABASES` (USER, PASSWORD).

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create an admin/staff account (for the admin panel):
   ```
   python manage.py createsuperuser
   ```
   Note: mark the user as staff (`is_staff=True`) so they can access `/admin-panel/`.

6. (Optional) Add a few categories via Django admin (`/django-admin/`):
   Road, Water, Electricity, Garbage, Drainage.

7. Run the server:
   ```
   python manage.py runserver
   ```

## URLs

- `/signup/` — citizen registration
- `/login/` — login
- `/` — citizen dashboard (own complaints + status)
- `/submit/` — submit a new complaint
- `/complaint/<id>/` — complaint detail (e.g. CF-2026-0001)
- `/admin-panel/` — staff-only: view/filter all complaints
- `/admin-panel/<id>/update/` — staff-only: update status + upload resolution proof
- `/django-admin/` — Django's built-in admin (manage Categories, Users)

## What to extend next (once basics work)

- Upvote/duplicate detection for repeated complaints in the same area
- REST API endpoints (Django REST Framework) so a React frontend can consume this later
- Email/SMS notification when status changes
- Deploy on Render/Railway + Aiven MySQL for a live demo link
