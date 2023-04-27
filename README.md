# HomeLift Api :
## Table of Contents

- [Installation](#How-to-use:)
- [Usage](#usage)
  * [Authentification](#Authentification)
  * [Product, (sub)categories ..](#Product)
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
