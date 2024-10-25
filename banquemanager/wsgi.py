"""
WSGI config for banquemanager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import threading

from django.core.wsgi import get_wsgi_application

from banquemanager.management.commands.start_scheduler import start_scheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banquemanager.settings')

application = get_wsgi_application()

if os.environ.get('RUN_MAIN') == 'true':
    from django.core.management import call_command

    def start_scheduler():
        call_command('start_scheduler')


    # Lancer le scheduler dans un thread séparé
    threading.Thread(target=start_scheduler).start()