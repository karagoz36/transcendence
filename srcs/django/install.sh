if [ ! -e /app/manage.py ]; then
	django-admin startproject transcendence app
fi

if [ !-e /app/views ]; then
	python /app/manage.py startapp views
fi

python /app/manage.py runserver 0.0.0.0:8000
