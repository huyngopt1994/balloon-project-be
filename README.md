# balloon-project-be
Using:
1. Django
2. Django-RestFrameWork(View Set)

https://www.django-rest-framework.org/tutorial/1-serialization/


# Steps for working with current project

If you want to update your database when you have any changings in your models.py
```bash
python manage.py makemigrations
```
=> It will automatically figure out what models changed and generate new migrations script.

```
python manage.py migrate
```

# Run server

```bash
python manage.py runserver
```

# Using admin page.
https://docs.djangoproject.com/en/2.2/ref/contrib/admin/
1. Create super user for admin page with using:
```bash
python manage.py createsuperuser
```
2. Access to admin page.
```bash
access to this URl. http://localhost:8000/admin/
```

# Apply JWT for securing 
https://simpleisbetterthancomplex.com/tutorial/2018/12/19/how-to-use-jwt-authentication-with-django-rest-framework.html

