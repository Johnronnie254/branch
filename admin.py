from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import current_app

admin = Admin(name='E-Commerce Admin', template_mode='bootstrap3')

class ProductAdmin(ModelView):
    column_searchable_list = ['name', 'description']

with current_app.app_context():
    from app.models import db, Product

admin.add_view(ProductAdmin(Product, db.session))
