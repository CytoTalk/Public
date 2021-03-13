
## Installation process
1. create a virtual environment and activate it
2. Run `pip install -r requirements.txt`
3. Create a .env in the project directory
4. Add the following variables to the env file
```
DB_USER=<Postgres db username>
DB_PASSWORD=<Postgres db password>
DB_NAME=<Postgres database name>
ADMIN_EMAIL=<the username you would like to use for the admin section>
ADMIN_PASSWORD=<password for the admin panel>

```
5. Run the following command
```
python manage.py db init
python manage.py db migrate
python manage.py runserver
```
