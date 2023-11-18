# Newsletter Subscription API

This project is a simple Newsletter Subscription API built with Flask and SQLAlchemy. It provides an endpoint to add new subscribers to a newsletter.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
 - Python 3.8 or higher
 - PostgreSQL

## Installation

- Clone the repository:
    ```sh
        git clone https://github.com/ankurgajurel/newsletter-backend.git
    ```

- Navigate to the project directory:
    ```sh
    cd newsletter-backend
    ```

- Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

- Set up your PostgreSQL database and update the connection string in the .env file.

- Run the Flask application:
    ```sh
    flask run
    ```

## Usage
To add a new subscriber, send a POST request to the /newSubscriber endpoint with a JSON body containing the fullName and email of the subscriber:

## Docker
This application can also be run using Docker. Here's how you can do it:

### Building the Docker Image
 - Make sure you have Docker installed on your machine.

 - Navigate to the project directory.

 - Build the Docker image:
    ```sh
    docker build -t newsletter-backend .
    ```

### Running the Docker Container
Run the Docker container:
```sh
docker run -p 4040:4040 newsletter-backend
```

Now, your application should be running at http://localhost:5000.

### Docker Compose
Setup your .env file and run:
```sh
docker compose up
```

Now, your application should be running at http://localhost/

## Testing
You can test the API using a tool like Postman or curl.

## Acknowledgments
Thanks to Flask and SQLAlchemy for making this project possible.