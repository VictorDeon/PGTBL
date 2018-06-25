"""
File responsible for the project templates.
"""

# Insert some features (user, request, ...) to all templates.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.today_date',
            ],
            'libraries':{
                'filterGRAT': 'questions.templatetags.my_templatetag',

            }
        },
    },
]
