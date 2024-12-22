if [ ! -e /app/manage.py ]; then
	django-admin startproject transcendence app
fi

find /app -type d -name migrations -exec rm -rf {} \; 2>/dev/null

python /app/manage.py makemigrations
python /app/manage.py migrate

python /app/manage.py makemigrations database
python /app/manage.py migrate database

python /app/manage.py createsuperuser --email '' --username $POSTGRES_USER --noinput
python /app/manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='$POSTGRES_USER')
user.set_password('$POSTGRES_PASSWORD')
user.save()"

python /app/manage.py runserver 0.0.0.0:8000