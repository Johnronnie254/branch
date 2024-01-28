from flask import Flask, make_response, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Product, Order, Cart, Address, Transaction, OrderItem, Contact

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)


@app.route('/')
def index():
    return f'Welcome to Shopify'

@app.route('/products', methods=['GET'])

def get_products():
    products= Product.query.all()
    
    product_dict=[
         {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image_url':product.image_url
        }
        for product in products
    ]
    
    response= make_response(
        jsonify(product_dict),
        200
    )

    return response


@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)

    if product is not None:
        user_dict = {
            'id': product.id,
            'name': product.name,
            'price':product.price,
            'image_url': product.image_url
        }
        return jsonify(user_dict), 200
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/users', methods=['GET'])
def get_users():
    users= User.query.all()
    users_dict= [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }
        for user in users
    ]

    return jsonify(users_dict), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)

    if user is not None:
        user_dict = {
            'id': user.id,
            'name': user.name
        }
        return jsonify(user_dict), 200
    else:
        return jsonify({'error': 'User not found'}), 404
    


# Endpoint for creating a new cart for a user
@app.route('/carts', methods=['POST'])
def create_cart():
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)

    if user:
        cart = Cart(user=user)
        db.session.add(cart)
        db.session.commit()
        return jsonify({'message': 'Cart created successfully'}), 201
    else:
        return jsonify({'error': 'User not found'}), 404

# Endpoint for getting all carts
@app.route('/carts', methods=['GET'])
def get_all_carts():
    carts = Cart.query.all()
    carts_data = [{'id': cart.id, 'user_id': cart.user_id} for cart in carts]
    return jsonify(carts_data), 200

# Similar endpoints can be created for Transaction, Address, Order, and OrderItem

# Endpoint for creating a new transaction for a user
@app.route('/transactions', methods=['POST'])
def create_transaction():
    user_id = request.json.get('user_id')
    amount = request.json.get('amount')

    user = User.query.get(user_id)

    if user:
        transaction = Transaction(user=user, amount=amount)
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction created successfully'}), 201
    else:
        return jsonify({'error': 'User not found'}), 404

# Endpoint for getting all transactions
@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    transactions = Transaction.query.all()
    transactions_data = [{'id': transaction.id, 'user_id': transaction.user_id, 'amount': transaction.amount} for transaction in transactions]
    return jsonify(transactions_data), 200

# Endpoint for creating a new address for a user
@app.route('/addresses', methods=['POST'])
def create_address():
    user_id = request.json.get('user_id')
    street = request.json.get('street')
    city = request.json.get('city')

    user = User.query.get(user_id)

    if user:
        address = Address(user=user, street=street, city=city)
        db.session.add(address)
        db.session.commit()
        return jsonify({'message': 'Address created successfully'}), 201
    else:
        return jsonify({'error': 'User not found'}), 404

# Endpoint for getting all addresses
@app.route('/addresses', methods=['GET'])
def get_all_addresses():
    addresses = Address.query.all()
    addresses_data = [{'id': address.id, 'user_id': address.user_id, 'street': address.street, 'city': address.city} for address in addresses]
    return jsonify(addresses_data), 200

# Similar endpoints can be created for Order and OrderItem

# Endpoint for creating a new order for a user
@app.route('/orders', methods=['POST'])
def create_order():
    user_id = request.json.get('user_id')
    cart_id = request.json.get('cart_id')

    user = User.query.get(user_id)
    cart = Cart.query.get(cart_id)

    if user and cart:
        order = Order(user=user, cart=cart)
        db.session.add(order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully'}), 201
    else:
        return jsonify({'error': 'User or Cart not found'}), 404

# Endpoint for getting all orders
@app.route('/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    orders_data = [{'id': order.id, 'user_id': order.user_id, 'cart_id': order.cart_id} for order in orders]
    return jsonify(orders_data), 200

# Endpoint for creating a new order item
@app.route('/order_items', methods=['POST'])
def create_order_item():
    order_id = request.json.get('order_id')
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')

    order = Order.query.get(order_id)
    product = Product.query.get(product_id)

    if order and product:
        order_item = OrderItem(order=order, product=product, quantity=quantity)
        db.session.add(order_item)
        db.session.commit()
        return jsonify({'message': 'Order Item created successfully'}), 201
    else:
        return jsonify({'error': 'Order or Product not found'}), 404

# Endpoint for getting all order items
@app.route('/order_items', methods=['GET'])
def get_all_order_items():
    order_items = OrderItem.query.all()
    order_items_data = [{'id': order_item.id, 'order_id': order_item.order_id, 'product_id': order_item.product_id, 'quantity': order_item.quantity} for order_item in order_items]
    return jsonify(order_items_data), 200








@app.route('/contacts/<int:contact_id>', methods=['POST'])
def update_contact_by_id(contact_id):
   
    contact = Contact.query.filter_by(id=contact_id).first()

    if contact is None:
        return jsonify({"error": "Contact not found!!"}), 404

  
    data = request.get_json()

    contact.name = data.get('name', contact.name)
    contact.email = data.get('email', contact.email)
    contact.message = data.get('message', contact.message)

    
    db.session.commit()

  
    contacts_dict = {
        "id": contact.id,
        "name": contact.name,
        "email": contact.email,
        "message": contact.message,
    }

    return jsonify(contacts_dict), 201





if __name__ == '__main__':
    app.run(debug=True)
