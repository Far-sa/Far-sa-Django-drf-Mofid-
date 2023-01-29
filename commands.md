# commands

django-admin startproject

./manage.py runserver

from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())

pip install -r requirements.txt

pytest -h / pytest
pytest -k <name of test/fn>
pytest -x
pytest -s <run other command rather than test>

django-treebeard
django-mptt

./manage.py spectacular --file schema.yml

coverage run -m pytest
coverage html

pytest --cov

django-mptt==0.14.0
djangorestframework==3.14.0
drf-spectacular==0.25.1
pytest==7.2.0
pytest-django==4.5.2
pytest-factoryboy==2.5.1
