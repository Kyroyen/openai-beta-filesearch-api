"""
WSGI config for chatqueryapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.conf import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatqueryapi.settings')

application = get_wsgi_application()
