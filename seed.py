from app import app, db
from faker import Faker
from models import User, Product, Order, Cart, Address, Transaction, Contact  # Import the Contact model

fake = Faker()

# Create an application context
app.app_context().push()

def generate_fake_data():
    # Generate fake data for existing models
    users = [User(name=fake.name(), email=fake.email()) for _ in range(10)]

    electronic_products = [
        Product(name=fake.word(), price=fake.random_number(2), image_url=fake.image_url(width=800, height=600))
        for _ in range(10)
    ]

    carts = [Cart(user=user) for user in users]
    addresses = [
        Address(user=user, street=fake.street_address(), city=fake.city()) for user in users
    ]

    # Add data for the Contact model
    contacts = [
        Contact(name=fake.name(), email=fake.email(), message=fake.text())
        for _ in range(5)
    ]

    # Add data to the database session individually
    for obj_list in [users, electronic_products, carts, addresses, contacts]:
        db.session.add_all(obj_list)

    # Commit the changes to the database
    db.session.commit()

if __name__ == '__main__':
    generate_fake_data()
