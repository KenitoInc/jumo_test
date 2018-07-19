
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy

from app import db, login_manager

# Base model that for other models to inherit from
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(UUID(as_uuid=True),
           server_default=sqlalchemy.text("uuid_generate_v4()"),unique=True )
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

class User(UserMixin, Base):

    __tablename__ = 'users'

    email = db.Column(db.String(60), index=True)
    username = db.Column(db.String(60), index=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'user_name': self.username,
            'is_admin': self.is_admin
        }


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Transaction(Base):

    __tablename__ = 'transactions'

    username = db.Column(db.String(60), index=True)
    phone_number = db.Column(db.String(60), index=True)
    amount = db.Column(db.String)
    discount = db.Column(db.Float, default=0)
    status = db.Column(db.String(60), nullable=True)
    error_message = db.Column(db.String(160), default=None)
    transaction_ref = db.Column(db.String(20))

    def __repr__(self):
        return '<Transaction : {}>'.format(self.username)

    def to_json(self):
        return {
            'errorMessage': "None",
            'phoneNumber': self.phone_number,
            'amount': "KES "+self.amount,
            'discount': self.discount,
            'status': "sent",
            'requestId': self.uuid

        }