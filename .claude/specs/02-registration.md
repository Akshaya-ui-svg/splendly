# Spec: Registration

## Overview
Registration allows new users to create an account by providing their name, 
## Depends on
01-database-setup

## Routes
- `GET /register` — renders registration form — public
- `POST /register` — handles registration logic (validation, hashing, insertion) — public

## Database changes
No database changes.

## Templates
- **Modify:** `templates/register.html` to include a proper form with `POST` method.

## Files to change
- `app.py`
- `database/db.py`
- `templates/register.html`

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done
- [ ] Visiting `/register` shows a form with fields for Name, Email, and Password.
- [ ] Submitting the form with valid data creates a new user in the `users` table.
- [ ] Passwords in the database are stored as hashes, not plain text.
- [ ] Attempting to register with an existing email returns a clear error message to the user.
- [ ] Registration successfully redirects the user to the login page upon completion.
- [ ] Form validation ensures no empty fields are submitted.

