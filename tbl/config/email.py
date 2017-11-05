"""
File to insert get email informations.
"""

import os

# Send email to console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Default from email.
DEFAULT_FROM_EMAIL = 'victorhad@gmail.com'

# Use a TLS (secure) connection when talking to the SMTP server.
EMAIL_USE_TLS = True
# TLS connection port
EMAIL_PORT = 587

# Gmail configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'victorhad@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD", "******")
