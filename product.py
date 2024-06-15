import os
from flask import current_app
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Endpoint 1: Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity} for product in products]
    return jsonify({"products": product_list})

# Endpoint 2: Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({"product": {"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity}})
    else:
        return jsonify({"error": "Product not found"}), 404
    
# Endpoint 3: Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    if "id" not in data or data['id'] is None:
        return jsonify({"error": "id is required"}), 400
    if "name" not in data or data['name'] is None:
        return jsonify({"error": "Name is required"}), 400
    if "price" not in data or data['price'] is None:
        return jsonify({"error": "Price is required"}), 400
    if "quantity" not in data or data['quantity'] is None:
        return jsonify({"error": "Quantity is required"}), 400

    # Type checks for each field
    if not isinstance(data['id'], int):
        return jsonify({"error": "id must be an integer"}), 400
    if not isinstance(data['name'], str):
        return jsonify({"error": "Name must be a string"}), 400
    if not isinstance(data['price'], (int, float)):
        return jsonify({"error": "Price must be a number"}), 400
    if not isinstance(data['quantity'], int):
        return jsonify({"error": "Quantity must be an integer"}), 400
    
    existing_product = Product.query.filter_by(id=data['id']).first()
    if existing_product:
        return jsonify({"error": "Product with this id already exists"}), 409

    new_product = Product(id=data['id'],name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added", "product": {"id": new_product.id, "name": new_product.name, "price": new_product.price, "quantity": new_product.quantity}}), 201

# Endpoint 4: Remove a product by ID
@app.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": f"Product {product_id} removed"}), 200
    else:
        return jsonify({"error": f"Product {product_id} not found"}), 404

# Endpoint 5: Remove a specific quantity of a product by ID
@app.route('/products/<int:product_id>/remove_quantity', methods=['PUT'])
def remove_product_quantity(product_id):
    data = request.json
    if "quantity" not in data:
        return jsonify({"error": "Quantity is required"}), 400

    product = Product.query.get(product_id)
    if product:
        if product.quantity >= data['quantity']:
            product.quantity -= data['quantity']
            if product.quantity == 0:
                db.session.delete(product)
            db.session.commit()
            return jsonify({"message": f"Quantity {data['quantity']} removed from product {product_id}"}), 200
        else:
            return jsonify({"error": "Insufficient quantity"}), 400
    else:
        return jsonify({"error": f"Product {product_id} not found"}), 404

# Endpoint 6: Add a specific quantity of a product by ID
@app.route('/products/<int:product_id>/add_quantity', methods=['PUT'])
def add_product_quantity(product_id):
    data = request.json
    if "quantity" not in data:
        return jsonify({"error": "Quantity is required"}), 400

    product = Product.query.get(product_id)
    if product:
        product.quantity += data['quantity']
        db.session.commit()
        return jsonify({"message": f"Quantity {data['quantity']} added to product {product_id}"}), 200
    else:
        return jsonify({"error": f"Product {product_id} not found"}), 404

# Endpoint 7: Remove all products
@app.route('/products', methods=['DELETE'])
def remove_all_products():
    all_products = Product.query.all()

    if all_products:
        for product in all_products:
            db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "All products removed"}), 200
    else:
        return jsonify({"message": "No products found"}), 404
    
if __name__ == '__main__':
    """with app.app_context():
        db.create_all()
    """
    app.run(debug=True)