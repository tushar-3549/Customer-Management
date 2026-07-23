# Customer Management System API

## Technology Stack

- Python 3.12
- Django 5
- Django REST Framework
- PostgreSQL
- Docker
- Swagger (drf-yasg)

---

## Features

- Create Customer
- Get Customer By ID
- Get All Customers
- Update Customer
- Delete Customer
- Multiple Mobile Numbers
- Multiple Addresses
- Multiple Documents
- Pagination
- Search
- Sorting
- Status Filter
- Validation
- Swagger Documentation

---

## Project Structure

```
config/
customers/
manage.py
Dockerfile
docker-compose.yml
requirements.txt
```

---

## API Endpoints

### Create Customer

POST

```
/api/customers/
```

### Customer List

GET

```
/api/customers/
```

Pagination

```
?page=1&page_size=10
```

Search

```
?search=tushar
```

Filter

```
?status=ACTIVE
```

Sorting

```
?ordering=name

?ordering=-created_at
```

---

### Customer Details

GET

```
/api/customers/{id}/
```

---

### Update Customer

PUT

```
/api/customers/{id}/
```

PATCH

```
/api/customers/{id}/
```

---

### Delete Customer

DELETE

```
/api/customers/{id}/
```

---

## Run without Docker

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```

---

## Run with Docker

```bash
docker-compose up --build
```

---

## Swagger

```
http://localhost:8000/swagger/
```

## ReDoc

```
http://localhost:8000/redoc/
```

---

## Validation

- Customer Name Required
- Email Unique
- Mobile Unique
- National ID Unique
- DOB cannot be future date

---

## HTTP Status

```
200 OK

201 Created

204 No Content

400 Bad Request

404 Not Found

500 Internal Server Error
```

---

## AI Tools Used

- ChatGPT
- GitHub Copilot

---

## Sample Prompt

```
Generate Django REST CRUD API with Service Layer and Repository Pattern.
```

---

## Verification

- Manually Tested
- Swagger Tested
- Postman Tested
