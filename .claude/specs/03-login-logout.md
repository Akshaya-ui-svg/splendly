# Spec: Login and Logout

## Overview
This feature implements the authentication mechanism for Spendly. It allows registered users to securely sign into their accounts and end their sessions. Authentication is handled via Flask sessions, ensuring that the user's identity is persisted across requests for access to protected areas of the application.

## Depends on
- 02 Registration

## Routes
- `POST /login` — Authenticates user via email and password; starts a session — public
- `GET /logout` — Clears the user session and redirects to login — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `templates/login.html` — Ensure the login form uses the `POST` method and correctly targets the `/login` route.

## Files to change
- `app.py` — Implement the POST handler for `/login` and the logic for `/logout`.
- `database/db.py` — Add a helper function to retrieve a user by email for credential verification.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use `check_password_hash` from `werkzeug.security` to verify passwords
- Use `flask.session` to store the `user_id` upon successful login
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done
- [ ] User can successfully log in with a valid email and password.
- [ ] User receives a clear error message ("Invalid email or password") when providing incorrect credentials.
- [ ] Successful login redirects the user to the `/profile` page.
- [ ] Logged-in user can click logout and be redirected back to the `/login` page.
- [ ] The session is fully cleared upon logout.
- [ ] Attempting to access `/logout` without being logged in redirects to `/login`.
