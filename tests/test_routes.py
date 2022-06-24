"""
Test Wishlist API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from urllib.parse import quote_plus
from service import app
from service.models import db, init_db, Wishlist
from service.utils import status  # HTTP Status Codes
from tests.factories import WishlistFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/wishlists"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   W I S H L I S T   S E R V I C E
######################################################################
class TestWishlistServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_wishlists(self, count):
        """Factory method to create wishlists in bulk"""
        wishlists = []
        for _ in range(count):
            test_wishlist = WishlistFactory()
            response = self.app.post(
                BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test wishlist"
            )
            new_wishlist = response.get_json()
            test_wishlist.id = new_wishlist["id"]
            wishlists.append(test_wishlist)
        return wishlists

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        response = self.app.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Wishlist Demo REST API Service")

    def test_get_wishlist(self):
        """It should Get a single Wishlist"""
        # get the id of a wishlist
        test_wishlist = self._create_wishlists(1)[0]
        response = self.app.get(f"{BASE_URL}/{test_wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_wishlist.name)

    def test_create_wishlist(self):
        """It should Create a new Wishlist"""
        test_wishlist = WishlistFactory()
        logging.debug("Test Wishlist: %s", test_wishlist.serialize())
        response = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
        )
        print(response.get_json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_wishlist = response.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name)

        # Check that the location header was correct
        print(location)
        response = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        print(response.get_json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_wishlist = response.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name)
