
# Advanced Features and Security

This Django project demonstrates the implementation of advanced features and security best practices:

- **Custom User Model**: Located in `accounts/models.py`, extends `AbstractUser` with additional fields:
	- `date_of_birth` (DateField)
	- `profile_photo` (ImageField)
	- Managed by a custom user manager (`CustomUserManager`) supporting `create_user` and `create_superuser` methods.
	- Registered in admin with a custom display via `CustomUserAdmin` in `accounts/admin.py`.
	- Set as the default user model in `project/settings.py` using `AUTH_USER_MODEL = 'accounts.CustomUser'`.

- **Permissions and Groups**:
	- Custom permissions (`can_view`, `can_create`, `can_edit`, `can_delete`) are defined in the `SecureDocument` model (`accounts/permissions_models.py`).
	- Views in `accounts/views.py` enforce permissions using the `@permission_required` decorator.
	- Groups (Editors, Viewers, Admins) can be managed via Django admin and assigned appropriate permissions.

- **Security Best Practices**:
	- All security-related configurations are set in `project/settings.py`:
		- `DEBUG = False` (for production)
		- `SECURE_BROWSER_XSS_FILTER = True`
		- `X_FRAME_OPTIONS = 'DENY'`
		- `SECURE_CONTENT_TYPE_NOSNIFF = True`
		- `CSRF_COOKIE_SECURE = True`
		- `SESSION_COOKIE_SECURE = True`
		- `SECURE_SSL_REDIRECT = True`
		- `SECURE_HSTS_SECONDS = 31536000`
		- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
		- `SECURE_HSTS_PRELOAD = True`
	- All forms should include `{% csrf_token %}` for CSRF protection.
	- Django ORM is used for all queries to prevent SQL injection.
	- Content Security Policy (CSP) can be added via middleware for additional XSS protection.

- **HTTPS and Secure Redirects**:
	- HTTPS is enforced via `SECURE_SSL_REDIRECT` and HSTS settings in `project/settings.py`.
	- Secure cookies are configured for session and CSRF tokens.
	- Additional secure headers are set to protect against clickjacking and XSS.

## Next Steps

1. Run migrations:
	 ```bash
	 python manage.py makemigrations accounts && python manage.py migrate
	 ```
2. Create a superuser:
	 ```bash
	 python manage.py createsuperuser
	 ```
3. Log in to the admin site and test user management, permissions, and security features.

## Documentation

- **Custom User Model**: See `accounts/models.py` and `accounts/admin.py` for implementation details.
- **Permissions**: See `accounts/permissions_models.py` and `accounts/views.py` for permission setup and enforcement.
- **Security Settings**: All settings are documented in `project/settings.py`.
- **Templates**: Ensure all forms include CSRF tokens and follow secure coding practices.

For further details, refer to the code comments and Django documentation.
