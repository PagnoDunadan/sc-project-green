# Introduction
SpringCamp project for Green Team #MaliZeleni <br />
Learn.com is an elearning web application with implemented courses to help you learn better and faster. <br />
![myimage-alt-tag](/static/img/homepage.png)

# Installation
1. Install requirements <br />
$ sudo apt-get update <br />
$ sudo apt-get install python-pip python-dev mysql-server libmysqlclient-dev <br />

2. Create Database and User <br />
$ mysql -u root -p <br />
mysql> CREATE DATABASE my_database CHARACTER SET UTF8; <br />
mysql> CREATE USER user@localhost IDENTIFIED BY 'password'; <br />
mysql> GRANT ALL PRIVILEGES ON my_database.* TO user@localhost; <br />
mysql> FLUSH PRIVILEGES; <br />

3. Clone project and create settings.py and private_settings.py files in sc-project-green/djangoelearning/ <br />
$ git clone https://github.com/ExtensionEngine/sc-project-green.git <br /> <br />
private.py format: <br />
[client] <br />
database = my_database <br />
user = user <br />
password = password <br />
host = localhost <br />
port =  <br />
default-character-set = utf8 <br /> <br />
private_settings.py format: <br />
LOCAL_SETTINGS = True <br />
from settings import * <br />
SECRET_KEY = 'some generated secret key' <br />
ALLOWED_HOSTS = ['localhost', '127.0.0.1'] <br />

3. Install Virtual Environment in sc-project-green, activate it, install REQUIREMENTS and apply migrations to the database <br />
$ cd sc-project-green <br />
$ sudo pip install virtualenv <br />
$ virtualenv djangoenv <br />
$ source djangoenv/bin/activate <br />
$ pip install -r REQUIREMENTS <br />
$ python manage.py migrate <br />

4. Run Django App <br />
$ python manage.py runserver <br />
address http://localhost:8000/ <br />

# Compatibility
Python 2.7 <br />
Django 1.11
