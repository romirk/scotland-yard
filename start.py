import os

import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scotlandyard.settings')
port = int(os.environ.get("PORT", 8000))

django.setup()

# call_command("makemigrations", interactive=False)
# call_command("migrate", interactive=False)
call_command("runserver", f"0.0.0.0:{port}")
