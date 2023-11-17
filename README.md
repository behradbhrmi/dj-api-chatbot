# Introduction 
django api server  without authentication 

# Getting Started
all requirements are in requirements.txt file.

<h2>Steps For Test:</h2>

<h4>1.Creating Virtual Environment:</h4>

```bash
python -m venv venv 
```
then activate the venv

<h4>2.Installing Requirements:</h4>

```python
pip install -r requirements.txt
```
<h4>3.Run Server:</h4>

```bash
python manage.py runserver 
```
#Deployment
For Deployment you need to create Virtual Environment after installing all requirements install and use Supervisor to run django back-end via gunicorn with with the given config and use nginx as reverse proxy.<br>

1.clone the project on the server , better to be in the given directory :
```
/srv/API-project/
```
2.create venv with the given command:<br>
Note: you need python3-venv to be installed.

```
python3 -m venv venv 
```
Activating venv:
```
source venv/bin/activate
```
Then change your directory to django root where the manage.py is.<br>

Installing Requirements:
``` 
pip install -r requirements.txt
```
Then it's time to configure the Supervisor.<br>

3.Supervisor config:<br>
change your directory to Supervisor config files.

```
cd /etc/supervisor/conf.d/
```

```
touch gunicorn.conf
```

```
vim gunicorn.conf
```
Enter given config to this file 
```
[program:gunicorn]

# django project root directory
directory = /srv/API-project/config


# command for using gunicorn from venv and run django server  
command = /srv/API-project/venv/bin/gunicorn  config.wsgi:application --workers 3  --bind 127.0.0.1:8000 


autostart = true

autorestart = true

# keep in mind the you need to create gunicorn directory in /var/log/ manually!
stderr_logfile = /var/log/gunicorn/gunicorn.err.log

stdout_logfile = /var/log/gunicorn/gunicorn.out.log
```
Then reread and reload supervisor :

```
supervisorctl reread
```

```
supervisorctl reload 
```

4.setting nginx up 
first install nginx then change directory to the nginx config directory 
```
cd /etc/nginx/sites-available
```

There is a 'default' file there you you remove it and create your own file or write in existing conf

```
upstream django_server {
	server 0.0.0.0:8000;
}

server {
	listen 80;
	server_name 'your ip and your domains';
	location / {
		proxy_pass http://django_server;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded_For $proxy_add_x_forwarded_for;
		proxy_set_header Host $host;
		proxy_redirect off;
	}

	location /static/ {
		root /srv/API-project/;
	}
}
```

then if you have removed default conf in these directory you need to add soft-link of this file into /nginx/sites-enabled/  and remove soft-link of default config file in that directory, and if not,you don't need to.

```
ln -s  <confi-file-name> ../sites-enabled
```

then restart the nginx

```
systemctl restart nginx
```

#Overview
Expected givn parameters in GET request:

<p>
    - message : "str"
</p>

Returns Response with these parameters:

<p>
Response parameters:<br>
    - method : which is GET<br>
    - url : url of api endpoint<br>
    - message: the message to send to the chatbot<br>
    - response : the response of chatbot to the client<br>
</p>
