"""
File to insert get email informations.
"""

import os

DEFAULT_FROM_EMAIL = 'Nome <victorhad@gmail.com>'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'victorhad@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD", "******")
EMAIL_PORT = 587
CONTACT_EMAIL = 'victorhad@gmail.com'
