# LibraryProject

This Django project demonstrates advanced features and security best practices:

## Features
- Custom user model (`CustomUser`) with extra fields (date_of_birth, profile_photo)
- Custom user manager for user creation and superuser creation
- Admin registration for custom user and Book models
- Custom permissions for Book: can_view, can_create, can_edit, can_delete
- Permission checks in views using `@permission_required`
- Security best practices in settings (XSS, CSRF, HTTPS, HSTS, CSP)
- All forms use CSRF tokens
- Secure session and cookie settings

## Permissions & Groups
- Groups: Editors, Viewers, Admins (assign via Django admin or management command)
- Permissions: can_view, can_create, can_edit, can_delete (assign to groups as needed)

## Security
- DEBUG=False, secure cookies, HTTPS enforced
- Content Security Policy (CSP) example in settings
- Security event logging to `security.log`

## Usage
- Run migrations after setup: `python manage.py makemigrations bookshelf && python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Assign users to groups and permissions via Django admin

## Documentation
See `SECURITY_DOCUMENTATION.md` for details on security configuration and best practices.
