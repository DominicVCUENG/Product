# Product Service API

This Flask application serves as a Product Service API that manages products in a database. It provides endpoints for retrieving, adding, updating, and deleting product information.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Flask-CORS

## Setup

1. Clone the repository:

```
git clone <repository_url>
cd <repository_name>
```
   
2. Install dependencies:

```
pip install -r requirements.txt
```
3. Run the application:
   
```
python app.py
```

4. The application will run on http://localhost:5000 by default.

## Endpoints

### Retrieve all products

- **GET** `/products`

Retrieves a list of all products stored in the database.

### Retrieve a specific product by ID

- **GET** `/products/<product_id>`

Retrieves a specific product by its ID.

### Add a new product

- **POST** `/products`

Creates a new product in the database. Requires a JSON payload with id, name, price, and quantity fields.

### Remove a product by ID

- **DELETE** `/products/<product_id>`

Deletes a product from the database based on its ID.

### Remove a specific quantity from a product

- **PUT** `/products/<product_id>/remove_quantity`

Updates the quantity of a product by subtracting a specified amount. Requires a JSON payload with quantity field.

### Add a specific quantity to a product

- **PUT** `/products/<product_id>/add_quantity`

Updates the quantity of a product by adding a specified amount. Requires a JSON payload with quantity field.

### Remove all products

- **DELETE** `/products`

Deletes all products from the database.

## Example Usage

### Retrieve all products

```python
import requests

response = requests.get('http://localhost:5000/products')
print(response.json())
```

### Add a new product

```python
import requests

data = {
    "id": 101,
    "name": "New Product",
    "price": 29.99,
    "quantity": 50
}
response = requests.post('http://localhost:5000/products', json=data)
print(response.json())
```

### Remove a product by ID

```python
import requests

response = requests.delete('http://localhost:5000/products/101')
print(response.json())
```

### Remove a specific quantity from a product

```python
import requests

data = {
    "quantity": 5
}
response = requests.put('http://localhost:5000/products/101/remove_quantity', json=data)
print(response.json())
```

### Add a specific quantity to a product

```python
import requests

data = {
    "quantity": 10
}
response = requests.put('http://localhost:5000/products/101/add_quantity', json=data)
print(response.json())
```

### Remove all products

```python
import requests

response = requests.delete('http://localhost:5000/products')
print(response.json())
```