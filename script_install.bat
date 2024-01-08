@echo off
pip install virtualenv
call virtualenv env
call env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
call env\Scripts\deactivate