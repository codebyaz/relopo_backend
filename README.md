# 📚 RELOPO

### Project setup

#### Create the project directory

```
mkdir relopo
cd relopo
```

#### Create a virtual environment to isolate our package dependencies locally

```
python -m venv env
source env/bin/activate
``` 
##### On Windows use ``env\Scripts\activate`` to activate the venv

#### Install dependencies

```
pip install -r requirements.txt
```

#### Bootstrap the database

```
python manage.py migrate
```

#### Create environment variables

From within the project root directory ``/relopo`` make a copy of the file  ``.env.example`` naming it ``.env``, then setup the blank variables with the provided values

#### Cache setup

Some of the resources throughout the application requires cache, so it is required to have ``Redis`` installed.

ℹ️ For this project it's been used the image: https://hub.docker.com/r/bitnami/redis/

Recommended to use a `Docker` container for it:

Download and install Docker if not installed from: https://www.docker.com/

from within the project's root directory ``/relopo`` run:

```
docker-compose up redis-master -d
```

Questions❓

https://chat.openai.com/