import os
import sys

import django
from django.conf import settings
from django.core.management import call_command

from scotlandyard import settings as sysettings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scotlandyard.settings')
port = int(os.environ.get("PORT", 5000))

django.setup()

call_command("makemigrations", interactive=False)
call_command("migrate", interactive=False)
call_command("runserver", f"0.0.0.0:{port}")
