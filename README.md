# crosschat

- sample chat application with crossbar.io

# Resources

- [github.com/crossbario](https://github.com/crossbario)

# Structure

~~~
$ tree -d -a
.
├── .crossbar           (crossbar direcotry)
├── app
│   └── settings.py     (Django settings)
├── chat                (Django Chat application)
│   ├── static
│   └── templates
│       └── chat
├── cross
│   └── crossbar.py     (crossbar Authenticator/Authorizer)
├── manage.py           (Django manager)

~~~

# Setup

~~~
$ python manage.py makemigrations cross

Migrations for 'cross':
  0001_initial.py:
    - Create model SocketUser
    - Create model Topic
    - Create model TopicUser

$ python manage.py makemigrations chat
Migrations for 'chat':
  0001_initial.py:
    - Create model Announce
    - Create model Room
    - Add field room to announce


$ python manage.py migrate
Operations to perform:
  Apply all migrations: sessions, admin, cross, auth, contenttypes, chat
Running migrations:
  Rendering model states... DONE
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying chat.0001_initial... OK
  Applying sessions.0001_initial... OK


$ python manage.py createsuperuser

Username (leave blank to use 'vagrant'):   
Email address: admin@admin.admin
Password: 
Password (again): 
Superuser created successfully.
~~~

# Start

~~~
$ crossbar start
~~~

~~~
$ python manage.py runserver 0.0.0.0:9000
~~~
