import enum
from sqlalchemy import Enum
import flask.ext.sqlalchemy
import flask.ext.restless
from flask_jwt_extended import JWTManager

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format('root', '', '127.0.0.1', '3306', 'core')

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = flask.ext.sqlalchemy.SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'JWT_PASSWORD_SUPER_SECRET'
jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

class Factory(db.Model):
    __tablename__ = 'factory'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))

class Store(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(30))
    zip = db.Column(db.String(8))

class ProductType(enum.Enum):
    SORVETE = 1
    PICOLE = 2
    BALDE = 3

class PaymentMethod(enum.Enum):
    DINHEIRO = 1
    DEBITO = 2
    CREDITO = 3

class OrderStatus(enum.Enum):
    FINALIZADO = 1
    CANCELADO = 2

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    type = db.Column(Enum(ProductType))
    bar_code = db.Column(db.String(100))
    price = db.Column(db.Float)

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    payment_method = db.Column(Enum(PaymentMethod))
    date = db.Column(db.Date)
    status = db.Column(Enum(OrderStatus))
    items = db.relationship("OrderItem")

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    total_price = db.Column(db.Float)
    discount = db.Column(db.Float)
    qty = db.Column(db.Float)

class PO(db.Model):
    __tablename__ = 'po'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    factory_id = db.Column(db.Integer, db.ForeignKey('factory.id'))
    date = db.Column(db.Date)
    cancel_date = db.Column(db.Date)
    receipt_date = db.Column(db.Date)
    status = db.Column(Enum(OrderStatus))

class POItem(db.Model):
    __tablename__ = 'po_item'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    total_price = db.Column(db.Float)
    discount = db.Column(db.Float)
    qty = db.Column(db.Float)

class ReceiptItem(db.Model):
    __tablename__ = 'receipt_item'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    po_id = db.Column(db.Integer, db.ForeignKey('po.id'))
    qty = db.Column(db.Float)

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    qty = db.Column(db.Float)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

# Create the database tables.
db.create_all()
