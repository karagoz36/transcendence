if [ ! -e /app/manage.py ]; then
	django-admin startproject transcendance app
fi

python /app/manage.py runserver
