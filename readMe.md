git pull origin main
— reload webapp


git clone https://github.com/AVSOLVE/rentals.git alexandrelima.pythonanywhere.com
git pull origin main
— reload webapp



@ ADD USER
----------------------------------------------------------------
cd rentals
python
>>>>>
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rentals.settings'
import django
django.setup()
from django.contrib.auth.models import User
user = User.objects.create_user('triade', 'triade@example.com', 'jk2024')
user.save()


source env/bin/activate
pip install -r requirements.txt
python manage.py runserver
