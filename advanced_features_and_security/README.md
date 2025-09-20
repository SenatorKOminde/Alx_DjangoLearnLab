# Advanced Features and Security

This Django project demonstrates:
- Custom user model with extra fields
- Permissions and groups
- Security best practices
- HTTPS and secure redirects

## Custom User Model
- Located in `accounts/models.py`
- Fields: `date_of_birth`, `profile_photo`
- Registered in admin with custom display
- Set as default user model in `settings.py` via `AUTH_USER_MODEL = 'accounts.CustomUser'`

## Security Settings
- See `project/settings.py` for all security-related configurations
- CSRF and session cookies are secure
- HTTPS and HSTS enforced
- XSS and clickjacking protections enabled

## Next Steps
- Run migrations: `python manage.py makemigrations accounts && python manage.py migrate`
- Create a superuser: `python manage.py createsuperuser`
- Log in to admin and test user management
