# HomeLift Api :
## Table of Contents

- [Installation](#How-to-use:)
- [Usage](#usage)
  * [Authentification](#authentification--latest-version-old-endpoints--new-for-staff)
  * [Product, (sub)categories ..](#product-)
  * [Configuration](#configuration)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

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
## Usage :

### Authentification : [Latest Version Old endpoints + New](https://djoser.readthedocs.io/en/latest/base_endpoints.html) for staff
 ### Authentification ( Old without verification)  for customers
 ##### a) Registration
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




 ### Product :

 ##### a) CRUD Product 
```http
POST http://127.0.0.1:8000/homeLift/products/
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

}
```


## Users Management
### View And Edit Profile
###### 1)view profile:
```http
  GET http://127.0.0.1:8000/account/${id}/view-profile/
```

#### Responses
```javascript
{
    "id": id,
    "username": username,
    "fullname": fullname,
    "email": email,
    "phone_number": phone_number,
    "shipping_address": shipping_address,
    "payment_info":payment_info ,
    "role": role_id,
    "blocked": True or False,
    "profile_picture": profile picture
}

```
###### 2)edit profile:
```http
  PUT /http://127.0.0.1:8000/account/${id}/view-profile/
```

| Key | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` |    |
| `fullname`      | `string` | **Required**(not necessarily modified) |
| `email`      | `string` | **Required** (not necessarily modified)|
| `phone_number`      | `string` | **Required** (not necessarily modified)|
| `shipping_address`      | `string` |  |
| `payment_info`      | `string` | |
| `profile_picture`      | `picture` | |

#### Responses
```javascript
{
    "id": id,
    "username": username,
    "fullname": fullname,
    "email": email,
    "phone_number": phone_number,
    "shipping_address": shipping_address,
    "payment_info":payment_info ,
    "role": role_id,
    "blocked": True or False,
    "profile_picture": profile picture
}
```
### View Staff List
```http
  GET http://127.0.0.1:8000/account/staff-list/
```
#### Responses
```javascript
{
    "id": id,
    "username": username,
    "fullname": fullname,
    "email": email,
    "phone_number": phone_number,
    "shipping_address": shipping_address,
    "payment_info":payment_info ,
    "role": role_id,
    "blocked": True or False,
    "profile_picture": profile picture
}

```
### Add Staff
```http
  POST http://127.0.0.1:8000/account/staff-list/add/
```

| Key | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` |    |
| `fullname`      | `string` | **Required** |
| `email`      | `string` | **Required Unique**|
| `phone_number`      | `string` | **Required Unique**|
| `shipping_address`      | `string` |  |
| `payment_info`      | `string` | |
| `profile_picture`      | `picture` | |

#### Responses
```javascript
{
    "id": id,
    "username": username,
    "fullname": fullname,
    "email": email,
    "phone_number": phone_number,
    "shipping_address": shipping_address,
    "payment_info":payment_info ,
    "role": 2,
    "blocked": True or False,
    "profile_picture": profile picture
}
```

### RetrieveUpdateDelete Staff 

###### 1)Retrieve:
```http
  GET http://127.0.0.1:8000/account/staff-list/${id}/
```
#### Responses
```javascript
{
    "id": id,
    "username": username,
    "fullname": fullname,
    "email": email,
    "phone_number": phone_number,
    "shipping_address": shipping_address,
    "payment_info":payment_info ,
    "role": 2,
    "blocked": True or False,
    "profile_picture": profile picture
}
```
###### 2)Update:
  PUT http://127.0.0.1:8000/account/staff-list/${id}/



| Key | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` |    |
| `fullname`      | `string` | **Required**(not necessarily modified) |
| `email`      | `string` | **Required** (not necessarily modified)|
| `phone_number`      | `string` | **Required** (not necessarily modified)|
| `shipping_address`      | `string` |  |
| `payment_info`      | `string` | |
| `profile_picture`      | `picture` | |

#### Responses
```javascript
{
    "id": id,
    "username": username,
    "fullname": fullname,
    "email": email,
    "phone_number": phone_number,
    "shipping_address": shipping_address,
    "payment_info":payment_info ,
    "role": 2,
    "blocked": True or False,
    "profile_picture": profile picture
}

```
###### 3)Delete:
Delete http://127.0.0.1:8000/account/staff-list/${id}/


# Notes:
#### Roles:
| id | Role     | 
| :-------- | :------- | 
| `Admin`      | `1` |
| `Staff`      | `2` |
| `Client`      | `3` |
