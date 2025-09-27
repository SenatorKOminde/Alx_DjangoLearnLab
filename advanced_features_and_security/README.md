# Advanced Features and Security - Django Project

## 🎯 Project Overview

This project demonstrates advanced Django security features including custom user models, permissions, groups, and comprehensive security settings. It implements a book management system with role-based access control and security best practices.

## 🚀 Features Implemented

### ✅ Task 0: Custom User Model
- **Custom User Model**: Extended `AbstractUser` with additional fields
- **Additional Fields**: `date_of_birth` and `profile_photo`
- **Custom Manager**: `CustomUserManager` with proper user creation methods
- **Admin Integration**: Custom admin interface for user management

### ✅ Task 1: Permissions and Groups
- **Custom Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **User Groups**: Viewers, Editors, Admins with appropriate permissions
- **Permission Enforcement**: Views protected with `@permission_required` decorators
- **Management Commands**: Automated setup of groups and test users

### ✅ Task 2: Security Best Practices
- **Secure Settings**: Comprehensive security configuration
- **CSRF Protection**: All forms include CSRF tokens
- **XSS Prevention**: Browser XSS filter and content type protection
- **SQL Injection Prevention**: Safe ORM usage and input validation
- **Content Security Policy**: CSP headers for additional protection

### ✅ Task 3: HTTPS and Secure Redirects
- **HTTPS Configuration**: SSL redirect and HSTS implementation
- **Secure Cookies**: HttpOnly, Secure, and SameSite cookie settings
- **Security Headers**: Additional security headers for protection
- **Transport Security**: Secure communication configuration

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.8+
- Django 4.2+
- Pillow (for ImageField support)

### Quick Setup
```bash
# Clone and navigate to project
cd advanced_features_and_security

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Set up groups and permissions
python manage.py setup_groups

# Create test users
python manage.py create_test_users

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 👥 Test Users

The following test users are created with different permission levels:

| Username | Password | Group | Permissions |
|----------|----------|-------|-------------|
| `viewer1` | `testpass123` | Viewers | `can_view` |
| `editor1` | `testpass123` | Editors | `can_view`, `can_create`, `can_edit` |
| `admin1` | `testpass123` | Admins | All permissions |
| `admin` | `admin123` | Superuser | All permissions |

## 🔐 Security Features

### Authentication & Authorization
- Custom user model with additional fields
- Role-based access control with groups
- Permission-based view protection
- Secure password validation

### Input Validation & Sanitization
- Form validation with custom clean methods
- XSS prevention in templates
- SQL injection prevention with ORM
- Safe search functionality

### Session & Cookie Security
- Secure cookie settings
- HttpOnly cookies
- SameSite cookie protection
- Session expiry configuration

### HTTPS & Transport Security
- SSL redirect enforcement
- HSTS implementation
- Secure header configuration
- Content Security Policy

### Application Security
- CSRF token protection
- Frame options protection
- Content type sniffing prevention
- Security event logging

## 📁 Project Structure

```
advanced_features_and_security/
├── accounts/                    # Custom user model app
│   ├── models.py               # CustomUser model
│   ├── admin.py                # Custom user admin
│   └── ...
├── bookshelf/                   # Book management app
│   ├── models.py               # Book model with permissions
│   ├── views.py                # Views with permission checks
│   ├── forms.py                # Secure form validation
│   ├── templates/              # Templates with CSRF tokens
│   ├── management/commands/     # Management commands
│   └── ...
├── project/                     # Main project settings
│   ├── settings.py             # Security configuration
│   └── urls.py                 # URL routing
├── SECURITY_DOCUMENTATION.md   # Detailed security documentation
└── README.md                   # This file
```

## 🧪 Testing the Security Features

### 1. Permission Testing
1. Login as `viewer1` - should only see books, cannot create/edit/delete
2. Login as `editor1` - can view, create, and edit books, cannot delete
3. Login as `admin1` - can perform all operations including delete

### 2. Security Headers Testing
Use browser developer tools to verify:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- Content Security Policy headers

### 3. CSRF Protection Testing
- All forms should include CSRF tokens
- Attempting to submit forms without tokens should fail

### 4. Input Validation Testing
- Try submitting invalid data in forms
- Verify that XSS attempts are blocked
- Test search functionality with special characters

## 🔧 Management Commands

### Setup Groups and Permissions
```bash
python manage.py setup_groups
```
Creates three groups with appropriate permissions:
- **Viewers**: `can_view` permission only
- **Editors**: `can_view`, `can_create`, `can_edit` permissions
- **Admins**: All permissions (`can_view`, `can_create`, `can_edit`, `can_delete`)

### Create Test Users
```bash
python manage.py create_test_users
```
Creates test users for each permission group with login credentials.

## 📊 Security Configuration

### Key Security Settings
- **DEBUG**: `False` for production
- **XSS Protection**: Browser XSS filter enabled
- **CSRF Protection**: Secure cookies with HttpOnly and SameSite
- **Session Security**: Secure, HttpOnly cookies with expiry
- **HTTPS**: SSL redirect and HSTS configuration
- **Content Security Policy**: Restrictive CSP headers

### Security Headers
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security` (HSTS)
- Content Security Policy headers

## 🚨 Production Deployment Notes

1. **Environment Variables**: Use environment variables for sensitive settings
2. **SSL Certificates**: Ensure valid SSL certificates are installed
3. **Security Headers**: Verify all security headers are present
4. **Database Security**: Use secure database connections
5. **Static Files**: Serve static files securely
6. **Logging**: Monitor security logs regularly

## 📚 Documentation

- **SECURITY_DOCUMENTATION.md**: Detailed security implementation documentation
- **Code Comments**: Extensive comments explaining security measures
- **Management Commands**: Self-documenting commands with help text

## 🎓 Learning Objectives Achieved

✅ **Custom User Model**: Extended Django's user model with additional fields  
✅ **Permissions & Groups**: Implemented role-based access control  
✅ **Security Best Practices**: Applied comprehensive security measures  
✅ **HTTPS & Secure Redirects**: Configured secure communication  

## 🔍 Security Testing Checklist

- [ ] Users without permissions cannot access restricted views
- [ ] CSRF tokens are present in all forms
- [ ] XSS protection headers are set
- [ ] SQL injection prevention works
- [ ] HTTPS redirects work (in production)
- [ ] Secure cookies are configured
- [ ] Content Security Policy is active
- [ ] Security events are logged

## 🆘 Troubleshooting

### Common Issues
1. **Pillow Installation**: Required for ImageField support
2. **Migration Issues**: Run `python manage.py makemigrations` then `migrate`
3. **Permission Errors**: Ensure groups are set up with `setup_groups` command
4. **HTTPS Issues**: Security settings require HTTPS in production

### Getting Help
- Check the `SECURITY_DOCUMENTATION.md` for detailed explanations
- Review Django security documentation
- Test with different user accounts to verify permissions

---

**🎉 Congratulations!** You've successfully implemented advanced Django security features including custom user models, permissions, groups, and comprehensive security settings. This project demonstrates production-ready security practices for Django applications.