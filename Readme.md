# CarsAPI Project

## The Backend
This API is built with **Flask** and allows you to:
- Register a car by providing its **brand** and **color**.
- Retrieve a list of all registered cars.
### The docker image name
##### weleassane/car-api-image:v1.0.0
Once the container is up and running, you can access the API's welcome page by navigating to the API address in your browser.

### Endpoints
- `/car-api/post-car` : Add a car.
- `/car-api/get-cars` : Retrieve all cars.

### Sample Requests
You can test the API using `curl` commands:

```bash
# Add a car
curl -X POST http://127.0.0.1:5000/car-api/post-car -H "Content-Type: application/json" -d '{"brand": "Toyota", "colour": "Red"}'

# Get all cars
curl http://127.0.0.1:5000/car-api/get-cars
```

## The Database
The API uses a **MySQL** database. To test or run this API, you need to have a MySQL server running. For simplicity, the database is containerized in this project.

## Docker Setup

### Docker Network
You will need a Docker network to link the MySQL container with the API container. We have named our network `car-api-network`. You can create it using the following command:

```bash
docker network create car-api-network
```

### The Database Container
To run the MySQL container, you'll need to set environment variables to configure the database:

- `MYSQL_ROOT_PASSWORD`: Set the root user password.
- `MYSQL_DATABASE`: Specify the name of the database to be created at startup.
- `MYSQL_USER` and `MYSQL_PASSWORD`: Optionally create a new user with these credentials.

#### Example Command for Running the MySQL Container:
```bash
docker run --network car-api-network \
    --name mysql-container-for-car-api \
    -e MYSQL_ROOT_PASSWORD=password \
    -e MYSQL_DATABASE=cars_db \
    -p 3306:3306 mysql
```

### The API Container
To run the API container, you need to pass the following environment variables:

- `DATABASE_HOST`: The hostname of the database (MySQL) container.
- `DATABASE_USER`: The MySQL username.
- `DATABASE_PASSWORD`: The MySQL password.
- `DATABASE_NAME`: The name of the database.
- `DATABASE_PORT`: The port on which the MySQL database is running.

#### Example Command for Running the API Container:
```bash
docker run --network car-api-network \
    --name car-api-container \
    -e DATABASE_HOST=mysql-container-for-car-api \
    -e DATABASE_USER=root \
    -e DATABASE_PASSWORD=password \
    -e DATABASE_NAME=cars_db \
    -e DATABASE_PORT=3306 \
    -p 5000:5000 weleassane/car-api-image:v1.0.0
```

## Docker Compose

To simplify container orchestration and ensure that the database is ready before the API container starts, **Docker Compose** is used. This ensures there are no dependency issues since the API relies on the database being available.

### Customizing Environment Variables
In the `docker-compose.yml` file, you can change the default environment variables according to your needs.

### Data Persistence
A volume is added to **persist the MySQL database data**. This ensures that the data remains available even if the containers are stopped or recreated.

### Commands to Start and Stop the Containers
- To start the services, use:
  ```bash
  docker-compose up -d
  ```
- To stop and remove the containers, use:
  ```bash
  docker-compose down
  ```