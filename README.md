# Bookstore API Project
=====================================

## Overview
------------

This project is a simple bookstore API built using Django and Django REST framework. It allows users to interact with two main objects: books and authors.

### Books

*   `id` (int): Unique identifier for the book
*   `title` (str): Title of the book
*   `author` (id): Foreign key referencing the author of the book
*   `count` (int): Number of copies of the book in stock

### Authors

*   `id` (int): Unique identifier for the author
*   `first_name` (str): First name of the author
*   `last_name` (str): Last name of the author

## API Endpoints
----------------

The API provides the following endpoints:

### Books

*   `GET /api/books`: Returns a list of all books
*   `POST /api/books`: Creates a new book
*   `PUT /api/books/{id}`: Updates a book
*   `POST /api/books/{id}/buy`: Buys a book and decrements the count

### Authors

*   `GET /api/authors`: Returns a list of all authors
*   `POST /api/authors`: Creates a new author
*   `PUT /api/authors/{id}`: Updates an author

## Requirements
---------------

*   Python 3.10
*   Django 5.1.3
*   Django REST framework 3.15.2

## Installation
------------

1.  Clone the repository
2.  Install the requirements using pip: `pip install -r requirements.txt`
3.  Run the migrations: `python manage.py migrate`
4.  Run the server: `python manage.py runserver`

## Usage
-----

Use a tool like curl or Postman to interact with the API endpoints.

Example:

*   Get all books: `curl http://localhost:8000/api/books`
*   Create a new book: `curl -X POST -H "Content-Type: application/json" -d '{"title": "New Book", "author": 1, "count": 10}' http://localhost:8000/api/books`

## Testing
-------

Run the tests using the following command: `python manage.py test`

## Docker
-------

A Dockerfile is provided to build a Docker image for the project.

1.  Build the image: `make docker build`
2.  Run the container: `make docker-compose up`

## Contributing
------------

Contributions are not required, but if you want to, you're always welcome! Please submit a pull request with your changes.

## License
-------

This project is licensed under the MIT License. See LICENSE for details.