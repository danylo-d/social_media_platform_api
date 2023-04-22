# Social Media Platform Api

## Installing using GitHub:

```shell
  git clone https://github.com/danylo-d/social_media_platform_api.git
  cd social_media_platform_api
  python -m venv venv
Linux/macOS:
  source venv/bin/activate
  pip install -r requirements.txt
  export DB_HOST=<your db hostname>
  export DB_NAME=<your db name>
  export DB_USER=<your db user>
  export DB_PASSWORD=<your db password>
  export SECRET_KEY=<your django secret key>
Windows: 
  venv\Scripts\activate
  pip install -r requirements.txt
  set DB_HOST=<your db hostname>
  set DB_NAME=<your db name>
  set DB_USER=<your db user>
  set DB_PASSWORD=<your db password>
  set SECRET_KEY=<your django secret key>
  python manage.py migrate
  python manage.py runserver
```

## Run with docker:
```shell
  docker-compose up --build
```

## Documentation:
```shell
  localhost/api/doc/swagger
```
