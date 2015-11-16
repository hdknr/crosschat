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

