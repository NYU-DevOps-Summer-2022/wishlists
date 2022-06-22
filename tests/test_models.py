"""
Test cases for Wishlist Model

"""
import os
import logging
import unittest
from werkzeug.exceptions import NotFound
from service.models import Wishlist, DataValidationError, db
from service import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  W I S H L I S T   M O D E L   T E S T   C A S E S
######################################################################
class TestWishlist(unittest.TestCase):
    """ Test Cases for Wishlist Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Wishlist.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_wishlist(self):
        """ It should create a wishlist and assert that it exists """
        wishlist = Wishlist(name="Summer")
        self.assertEqual(str(wishlist), "<Wishlist 'Summer' id=[None]>")
        self.assertTrue(wishlist is not None)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.name, "Summer")
        
