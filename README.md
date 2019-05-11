# balloon-project-be
Using:
1. Django
2. Django-ViewSet


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
