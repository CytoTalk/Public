serve:
		python3 manage.py runserver
install:
		pip3 install -r requirements.txt
migrate:
		python3 manage.py db migrate
		python3 manage.py db upgrade
create_admin:
		python3 manage.py create_admin
db:
		python3 manage.py db
cap:
		python3 manage.py change_admin_password