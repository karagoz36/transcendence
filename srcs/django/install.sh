if [ ! -e /app/manage.py ]; then
	django-admin startproject transcendence app
fi

python /app/manage.py runserver 0.0.0.0:8000
