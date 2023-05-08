# HomeLift Api :
## Table of Contents

- [Installation](#how-to-use)
- [Swagger API Documentation](#swagger-more-in-depth-api-documentation-)
- [Usage](#usage)
  * [Authentification](#authentification--latest-version-old-endpoints--new-for-staff)
  * [Products & Archiving](#product-)
  * [Categories](#categories-)
  * [Sub-Categories](#sub-categories)
  * [Users Management](#retrieveupdatedelete-customer-you-can-block-here)
    - [Block Staff Or customer](#retrieveupdatedelete-staff-you-can-block-here)
    - [View Blocked Users](#view-blocked-users-)
- [Notes](#notes)




### **Swagger** More in depth Api Documentation :
**Visit:**   

```http
GET http://127.0.0.1:8000/swagger/
GET http://127.0.0.1:8000/redoc/

```
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

#### Responses

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

#### Responses


```javascript
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```




 ### Product :
##### **a) Products List**
 
```http
GET http://127.0.0.1:8000/homeLift/products/ #Products list 

GET /api/products/          # get all products

GET /api/products/<pk>/     # get a specific product by primary key

GET /api/products/?min_price=<min_price>&max_price=<max_price>&price_exact=<price_exact> # filter products by price range 

GET /api/products/?archived=True #Filter By archived products

GET /api/products/?search=<search_term> # search for products by name, description, category, or subcategory

GET /api/products/?ordering=<ordering_field> # order products by name, price, or quantity

```

#### Responses
```http
HTTP 200 OK
```
```javascript
{
        "id": 6,
        "productComments": [],
        "productImages": [],
        "productRatings": [],
        "category_name": "Dining Room",
        "subcategory_name": "Dining table",
        "in_stock": true,
        "name": "Coffe Table",
        "image": "http://127.0.0.1:8000/images/images/coffetable_MABDhkG.jpg",
        "price": 21111.0,
        "description": "descr",
        "quantity": 2000,
        "rating_rv": 0.0,
        "rating_nb": 0,
        "created_at": "2023-04-20T13:09:31.814193Z",
        "updated_at": "2023-04-20T13:09:31.814193Z",
        "archived": false,
        "subcategory": 5,
        "category": 4
    },
```

##### **b) Products Pictures**
 
```http
POST http://127.0.0.1:8000/homeLift/products/<int:pk>/images-create/ #Add images for specific Prodcut 
```
| Key | Type | Description |
| :--- | :--- | :--- |
| `image ` | `image` | ``<int:pk>``==product id |

#### Response
```http
HTTP 201 Created
```
```javascript
{
    "id": 2,
    "image": "http://127.0.0.1:8000/images/images/image.jpg"
}
```

```http
GET|PUT|DELETE http://127.0.0.1:8000/homeLift/products/images/<int:pk>/ #Get Image by id
```
| Key | Type | Description |
| :--- | :--- | :--- |
| `image ` | `image` | ``<int:pk>``==image id |

#### Response
```http
HTTP 201 Created
```
```javascript
{
    "id": 2,
    "image": "http://127.0.0.1:8000/images/images/image.jpg"
}
```
##### **c) Create A Product:**
  
```http
POST  http://127.0.0.1:8000/homeLift/products/
```
in the Request Body : 
| Key | Type | Description |
| :--- | :--- | :--- |
| `name ` | `string` | **Required** **Unique**  |
| `image` | `picture` ||
| `price` | `integer` |**Required**   |
| `description ` | `string` |  |
| `quantity` | `integer` |  |
| `category` | `string` | category.name |
| `subcategory` | `string` | subcategory.name |
| `archived` | `bool` | default = False |

#### Responses
```http
HTTP 201 Created
```
```javascript
{
    "id": 9,
    "productComments": [],
    "productImages": [],
    "productRatings": [],
    "category_name": "Bedroom",
    "subcategory_name": "Nightstand",
    "in_stock": true,
    "name": "Test Product 1",
    "image": "http://127.0.0.1:8000/images/images/fc_GQ9Uy1Q.jpg",
    "price": 188888.0,
    "description": "Description",
    "quantity": 5000,
    "rating_rv": 0.0,
    "rating_nb": 0,
    "created_at": "2023-04-28T21:44:56.529072Z",
    "updated_at": "2023-04-28T21:44:56.529072Z",
    "archived": false,
    "subcategory": 7,
    "category": 2

}
```
##### **c) Retrieve/Updat/Delete a Product : (& Archive a Product)**
  
```http
GET|PUT|Patch|DELETE http://127.0.0.1:8000/homeLift/products/<id:int>/
```
in the Request Body : 
| Key | Type | Description |
| :--- | :--- | :--- |
| `name ` | `string` | **Required** **Unique**  |
| `image` | `picture` ||
| `price` | `integer` |**Required**   |
| `description ` | `string` |  |
| `quantity` | `integer` |  |
| `category` | `string` | category.name |
| `subcategory` | `string` | subcategory.name |
| `archived` | `bool` | default = False |

#### Responses
```http
HTTP 201 Created
```
```javascript
{
    "id": 9,
    "productComments": [],
    "productImages": [],
    "productRatings": [],
    "category_name": "Bedroom",
    "subcategory_name": "Nightstand",
    "in_stock": true,
    "name": "Test Product 1",
    "image": "http://127.0.0.1:8000/images/images/fc_GQ9Uy1Q.jpg",
    "price": 188888.0,
    "description": "Description",
    "quantity": 5000,
    "rating_rv": 0.0,
    "rating_nb": 0,
    "created_at": "2023-04-28T21:44:56.529072Z",
    "updated_at": "2023-04-28T21:44:56.529072Z",
    "archived": false,
    "subcategory": 7,
    "category": 2

}
```
 To archive a Product Patch Request with archived = True
```javascript
{
    "id": 9,
    "archived": true,
}
```

### **Categories :**
 
```http
GET|POST http://127.0.0.1:8000/homeLift/categories/ #List All categories/ Add a category
```
in the Request Body : 
| Key | Type | Description |
| :--- | :--- | :--- |
| `name ` | `string` | **Required** **Unique**  |

##### Responses
```http
HTTP 201 Created
```
```javascript
{
    "id": 6,
    "subCategories": [],
    "name": Category name
}
```
 
### **Sub-Categories**
```http
GET http://127.0.0.1:8000/homeLift/categories/<int:pk>/subcategory/ #List All sub categories in a category
```
in the Request Body : 
| Key | Type | Description |
| :--- | :--- | :--- |
| `name ` | `string` | **Required** **Unique**  |

##### Responses
```http
HTTP 201 Created
```
```javascript
{
    "id": 6,
    "subCategories": [],
    "name": Category name
}
```
 

```http
POST http://127.0.0.1:8000/homeLift/categories/<int:pk>/subcategory/ #Create sub-category
```
in the Request Body : 
| Key | Type | Description |
| :--- | :--- | :--- |
| `name ` | `string` | **Required** **Unique**  , ``<int:pk>`` == Category ID  |

##### Responses
```http
HTTP 201 Created
```
```javascript
{
    "id": 9,
    "products": [],
    "name": "Sub-Category Name
}
```
 

```http
GET|Put|Patch|Delete http://127.0.0.1:8000/homeLift/categories/subcategory/<int:pk>/ #Edit subcategory
```
in the Request Body : 
| Key | Type | Description |
| :--- | :--- | :--- |
| `name ` | `string` | **Required** **Unique**  , ``<int:pk>`` == Sub-Category ID  |

##### Responses
```http
HTTP 201 Created
```
```javascript
{
    "id": 5,
    "products": [],
    "name": New-Name
}
```

### View Customer List
```http
  GET http://127.0.0.1:8000/account/customer-list/
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

### RetrieveUpdateDelete Customer (you can Block here)
```http
http://127.0.0.1:8000/account/customer-list/<int:pk>/
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
    "role": 2,
    "blocked": True or False,
    "profile_picture": profile picture
}
```



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
  PUT http://127.0.0.1:8000/account/${id}/view-profile/
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
### RetrieveUpdateDelete Staff (you can Block here)
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
```http
  PUT  http://127.0.0.1:8000/account/staff-list/${id}/
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
    "role": 2,
    "blocked": True or False,
    "profile_picture": profile picture
}
```
###### 3)Delete:
```http
Delete http://127.0.0.1:8000/account/staff-list/${id}/
```
###### View blocked Users : 
```http
GET http://127.0.0.1:8000/account/blocked/
```
Response : 
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
# Notes:
#### Roles:
| id | Role     | 
| :-------- | :------- | 
| `Admin`      | `1` |
| `Staff`      | `2` |
| `Client`      | `3` |

