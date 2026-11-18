# Entry point a web server uses to run the site

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gasite.settings")
application = get_wsgi_application()
