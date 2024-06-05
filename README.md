# Flask User Form App

This application is created to save user information in Flask using both synchronous and asynchronous requests using celery + redis. 


## Getting Started

Follow these steps to build and run the app.

### Clone the repository:

   ```bash
   git clone https://github.com/Kinciorska/warehouse.git
   ```
### Build the Docker Image:

Needed environment files:

- .flask

- .postgres

Environment files should be located in .envs directory, examples of these environment files are available in the same directory.
 

1. Clone the repository
    ```
   git clone https://github.com/Kinciorska/flask_user_form.git
    ```
2. Install the necessary dependencies:
    ``` 
   pip install -r requirements.txt
    ```
3. Initialize the db
    ``` 
   python init_db.py
    ```
4. Run Redis Stack in Docker
    ``` 
   docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:7.2.0-v10
    ```
5. Run the app
    ``` 
   python app.py
    ```
   
6. Start celery workers (N - worker number)
   ``` 
   celery -A app.celery worker --loglevel=INFO --concurrency=10 -n workerN@%h
    ```
   
### Technologies
- Flask
- PostgreSQL
- Redis
- Celery


#### License
This app is open-source and distributed under the MIT License.
