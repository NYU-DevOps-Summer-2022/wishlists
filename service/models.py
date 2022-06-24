"""
Models for Wishlist

All of the models are stored in this module
"""
import logging
from enum import Enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

def init_db(app):
    """Initialize the SQLAlchemy app"""
    Wishlist.init_db(app)

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass


class Wishlist(db.Model):
    """
    Class that represents a Wishlist
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Wishlist %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Wishlist to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Wishlist to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Wishlist from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Wishlist into a dictionary """
        return {
            "id": self.id, 
            "name": self.name,
            "customer_id": self.customer_id
        }

    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            if isinstance(data["customer_id"], int) and type(data["customer_id"])!=bool:
                self.customer_id = data["customer_id"]
            else:
                raise DataValidationError("Invalid type for integer [customer_id]: " + str(type(data["customer_id"])))
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid Wishlist: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError("Invalid Wishlist: body of request contained bad or no data" + str(error))
        return self

    
    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Wishlists in the database """
        logger.info("Processing all Wishlists")
        return cls.query.all()

    @classmethod
    def find(cls, by_id: int):
        """ Finds a Wishlist by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)
    
    @classmethod
    def find_or_404(cls, wishlist_id: int):
        """Find a Wishlist by it's id

        :param wishlist_id: the id of the Wishlist to find
        :type wishlist_id: int

        :return: an instance with the wishlist_id, or 404_NOT_FOUND if not found
        :rtype: Wishlist

        """
        logger.info("Processing lookup or 404 for id %s ...", wishlist_id)
        return cls.query.get_or_404(wishlist_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Wishlists with the given name

        Args:
            name (string): the name of the Wishlists you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
    
    @classmethod
    def find_by_customer_id(cls, customer_id: int) -> list:
        """Returns all of the Wishlists with a specific customer_id

        :param customer_id: the customer_id of the Wishlists you want to match
        :type customer_id: str

        :return: a collection of Wishlists by the customer with customer id <customer_id> 
        :rtype: list

        """
        logger.info("Processing category query for %s ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id)

