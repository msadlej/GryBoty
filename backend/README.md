# Backend
FastAPI-based backend for the Gry Boty project.


## Table of Contents
- [Installation](#installation)
- [Database](#database)
- [Usage](#usage)
- [Testing](#testing)


## Installation
Clone the repository and navigate to the backend directory.
```bash
git clone [repo]
cd repo/backend
```

To install the package, use the following command.
This will install the package and all of its dependencies.
```bash
make build
```


If you want to install the package in editable mode, use the following command.
This will allow you to make changes to the code and install aditional dependencies needed to run tests.
```bash
make build-dev
```


## Database
In order to run the backend, you need to have a MongoDB instance running.
To check if you have MongoDB running, use the following command:
```bash
systemctl status mongod
```
To start MongoDB, use the following command:
```bash
sudo systemctl start mongod
```
To stop MongoDB, use the following command:
```bash
sudo systemctl stop mongod
```


## Usage
To run the backend, use the following command:
```bash
make run
```
Go to localhost:8000/docs to see the API documentation.


## Testing
To test the package, use the following command.
This will run all the tests, as well as generate a coverage report, lint and type check the code.
```bash
make test
```
Note: You need to have the package installed in dev mode to run tests. (see [Installation](#installation))
