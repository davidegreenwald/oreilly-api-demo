# O'Reilly Search API Demo

## About this repo

This API demo is a Python project using Django and the Django REST Framework.

It is capable of populating a local Postgres database with a subset of data from
the O'Reilly Search API and making it consumable from a number of endpoints.

## Local set-up

Docker and `docker-compose` is the only dependency to demo this project. 
`docker-compose.yml` includes a built Django Docker container (built from the 
  Dockerfile in this repo) and Postgres.

```
docker-compose up -d
```

Note that the API application will test briefly to ensure the database is ready 
before starting up.

It will become available at:

```
http://localhost:8000
```

## Endpoints

```
/books/refresh/
```

View this endpoint with a `GET` request to populate the database with the latest 
search results for Python books from the O'Reilly API.

Additional requests to this path will compare ISBN numbers with existing 
database entries and only add new results.

```
/books/add-book/
```

Add a book to the database in JSON format with a `POST` request.

```
/books
```

Query the full list of books in the local database.

```
/books/python/
```

See all Python books in the local database. This will match the full list.

```
/books/python/data-science/
```

Query all Python books on the topic of data science from the local database.

```
/books/isbn/$ISBN_NUM/
```

Query individual books, using their ISBN number.

For example, `/books/isbn/9781492081005`.

## TODO/Next Steps

See TODO comments throughout the project for additional notes.

### Configuration and security
- Turn off Django's `DEBUG = True`, set `ALLOWED_HOSTS` value
- Secure/remove additional endpoints such as Django's default `/admin`
- Authentication for the `/books/refresh` and `/books/add` endpoints
- Secure server access under Nginx for SSL
- Run the Django server under a non-root user

### Performance
- Integrate Redis or memcached object cache for database requests

### Deployment
- Kubernetes manifest files including configs for secrets for database credentials and environment variables
- Set Django `SECRET_KEY` with a K8s secret environment variable


