if [ ! -e /app/manage.py ]; then
	django-admin startproject transcendence app
fi

DJANGO_SUPERUSER_USERNAME=$POSTGRES_USER
DJANGO_SUPERUSER_PASSWORD=$POSTGRES_PASSWORD
DJANGO_SUPERUSER_EMAIL=""

python /app/manage.py createsuperuser --email '' --username $POSTGRES_USER --noinput
python /app/manage.py migrate
python /app/manage.py makemigrations
python /app/manage.py runserver 0.0.0.0:8000
