migrations:
	python3 manage.py migrate
	python3 manage.py makemigrations

run:
	python3 manage.py runserver

superuser:
	python3 manage.py createsuperuser