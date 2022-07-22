"""
Models for Wishlist

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Wishlist.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""

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

    items = db.relationship("Item", backref="wishlist", passive_deletes=True)

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
        """Removes a Wishlist from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Wishlist into a dictionary"""
        return {"id": self.id, "name": self.name, "customer_id": self.customer_id}

    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]

            try:
                self.customer_id = int(data["customer_id"])
            except ValueError:
                # Handle the exception - data validation error
                raise DataValidationError(
                    "Invalid type for integer [customer_id]: "
                    + str(type(data["customer_id"]))
                )

        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0])
        except KeyError as error:
            raise DataValidationError("Invalid Wishlist: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlist: body of request contained bad or no data"
                + str(error)
            )
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the Wishlists in the database"""
        logger.info("Processing all Wishlists")
        return cls.query.all()

    @classmethod
    def find(cls, by_id: int):
        """Finds a Wishlist by it's ID"""
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
    def find_by_param(cls, query):
        """Returns all Wishlists with the given name

        Args:
            query (dict): contains the key value pairs of the query
        """
        logger.info("Processing query for %s ...", str(query))

        result = None

        if query["name"] and query["customer_id"]:
            result = cls.query.filter(
                cls.name == query["name"], cls.customer_id == query["customer_id"]
            )
        elif query["name"]:
            result = cls.query.filter(cls.name == query["name"])
        elif query["customer_id"]:
            result = cls.query.filter(cls.customer_id == query["customer_id"])
        return result

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


class Item(db.Model):
    """
    Class that represents a Wishlist item
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(
        db.Integer, db.ForeignKey("wishlist.id", ondelete="CASCADE"), nullable=False
    )
    product_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Item id=[%s] wishlist_id=[%s] product_id=[%s]>" % (
            self.id,
            self.wishlist_id,
            self.product_id,
        )

    def create(self):
        """
        Creates a Wishlist item to the database
        """
        logger.info(
            "Creating wishlist_id=[%s] product_id=[%s]",
            self.wishlist_id,
            self.product_id,
        )
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Wishlist item to the database
        """
        logger.info(
            "Creating wishlist_id=[%s] product_id=[%s]",
            self.wishlist_id,
            self.product_id,
        )
        db.session.commit()

    def delete(self):
        """Removes a Wishlist item from the data store"""
        logger.info("Deleting %s", self.id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Wishlist into a dictionary"""
        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "product_id": self.product_id,
        }

    def deserialize(self, wishlist_id, product_id):
        """
        Deserializes the wishlist from wishlist_id and product_id

        Args:
            wishlist_id, product_id
        """

        # skipping validations required since we are accepting them as integers in the API endpoint itself,
        # can add later if required
        self.wishlist_id = wishlist_id
        self.product_id = product_id

        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our SQLAlchemy tables

    @classmethod
    def find_by_wishlist_id_and_product_id(
        cls, wishlist_id: int, product_id: int
    ) -> list:
        """Returns the item with wishlist_id and product_id

        :param wishlist_id: the wishlist_id of the Wishlist you want to match
        :type wishlist_id: int

        :param product_id: the product_id of the Wishlist you want to match
        :type product_id: int

        :return: a collection of wishlist items
        :rtype: list

        """
        logger.info(
            "Processing category query for wishlist_id %s and product_id %s ...",
            wishlist_id,
            product_id,
        )
        return cls.query.filter(
            cls.wishlist_id == wishlist_id, cls.product_id == product_id
        )

    @classmethod
    def find_by_wishlist_id(cls, wishlist_id: int) -> list:
        """Returns the item with wishlist_id and product_id

        :param wishlist_id: the wishlist_id of the Wishlist you want to match
        :type wishlist_id: int

        :return: a collection of wishlist items
        :rtype: list

        """
        logger.info("Processing category query for wishlist_id %s ...", wishlist_id)
        return cls.query.filter(cls.wishlist_id == wishlist_id)

    @classmethod
    def find_by_wishlist_id_and_item_id(cls, wishlist_id: int, item_id: int) -> list:
        """Returns the item with wishlist_id and product_id

        :param wishlist_id: the wishlist_id of the Wishlist you want to match
        :type wishlist_id: int

        :param item_id
        :type item_id: int

        :return: a collection of wishlist items
        :rtype: list

        """
        logger.info(
            "Processing category query for wishlist_id %s ... item_id %s",
            wishlist_id,
            item_id,
        )
        return cls.query.filter(cls.id == item_id, cls.wishlist_id == wishlist_id)
