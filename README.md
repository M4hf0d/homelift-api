# HomeLift Api :

## How to use: 
Clone the Repo then :

```python
python3 -m venv env
source env/bin/activate  
# On Windows use `env\Scripts\activate`

# Install the requirements
pip install -r requirements.txt

#Run the server 
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser #optional

python manage.py runserver
```

### View All Costumers:
```http
GET http://127.0.0.1:8000/account/customer/
```
###### Responses

```javascript
{
  {
        "id": n,
        "username": username,
        "fullname": fullname,
        "email": ,
        "phone_number": phone_number,
        "shipping_address": shipping_address,
        "payment_info": payment_info
    }
}
```

### View  Costumer by ID:
```http
GET http://127.0.0.1:8000/account/customer/<id>/
```
###### Responses

```javascript
{
  {
        "id": n,
        "username": username,
        "fullname": fullname,
        "email": ,
        "phone_number": phone_number,
        "shipping_address": shipping_address,
        "payment_info": payment_info
    }
}
```
## Authentification : [Latest Version Old endpoints + New](https://djoser.readthedocs.io/en/latest/base_endpoints.html) for staff
## Authentification ( Old without verification)  for customers
 #### a) Registration
```http
POST http://127.0.0.1:8000/account/register/
```
in the Request Body : 
| Key | Type | Description |
| :--- | :--- | :--- |
| `email` | `string` | **Required** **Unique** The Users Email |
| `phone_number` | `string` | **Required** **Unique**|
| `password` | `string` | **Required**  |
| `fullname` | `string` | **Required** |
| `username` | `string` |  |
| `shipping_address` | `string` |  |
| `payment_info` | `string` |  |

## Responses

```javascript
{
  "response": "Registration Successful!",
    "phone_number": Phone_Number,
    "email": email,
    "token": {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
}
```
#### b) Login
```http
POST http://127.0.0.1:8000/account/api/token/
```
in the Request Body : 
| Key | Type | 
| :--- | :--- 
| `email` | `string` 
| `password` | `string` 

## Responses


```javascript
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```


## Status Codes

Gophish returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |

