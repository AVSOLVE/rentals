import os
import sys

# Add your project directory to the sys.path
project_home = '/home/alexandrelima/rentals'
if project_home not in sys.path:
    sys.path.append(project_home)

# Add your virtualenv directory to the sys.path
venv_path = os.path.join(project_home, 'env', 'lib', 'python3.10', 'site-packages')
if venv_path not in sys.path:
    sys.path.append(venv_path)

# Set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'rentals.settings'

# Import Django's WSGI handler and assign it to `application`
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
