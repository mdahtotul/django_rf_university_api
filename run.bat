@echo off
cd .\api\
call venv\Scripts\activate
py.exe manage.py wait_for_db && py.exe manage.py migrate && py.exe manage.py runserver