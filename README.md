# Flask User Form App

This application is created to save user information in Flask using both synchronous and asynchronous requests using celery + rabbitmq. 


## Getting Started

Follow these steps to build and run the app.


### Clone the repository
```
git clone https://github.com/Kinciorska/flask_user_form.git
```

### Change into the correct directory
```
cd flask_user_form
```

### Build the Docker Image:

   Needed environment files:

- .flask
- .postgres
- .rabbitmq

Environment files should be located in .envs directory, examples of these environment files are available in the same directory.
 
Build and run the Docker container using
```
docker compose up
```
### Initialize the db
``` 
docker compose run flask python init_db.py
```
### Start Celery worker (N - worker number)
``` 
docker compose run flask celery -A app.celery worker --loglevel=INFO --concurrency=10 -n workerN@%h
```
   
### Technologies
- Flask
- PostgreSQL
- RabbitMQ
- Celery
- Docker

#### License
This app is open-source and distributed under the MIT License.
