"""
Test Wishlist API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase

from service import app
from service.models import db, init_db, Wishlist, Item
from service.utils import status  # HTTP Status Codes
from tests.factories import WishlistFactory, ItemFactory

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
        db.session.query(Item).delete()  # clean up the last tests
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

    def test_get_wishlist_list(self):
        """It should Get a list of Wishlists"""
        self._create_wishlists(8)
        response = self.app.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 8)

    def test_get_wishlist(self):
        """It should Get a single Wishlist"""
        # get the id of a wishlist
        test_wishlist = self._create_wishlists(1)[0]

        item = ItemFactory()
        item.wishlist_id = test_wishlist.id

        req = {"customer_id":test_wishlist.customer_id}

        response = self.app.put(
            BASE_URL+"/"+str(test_wishlist.id)+"/products/"+str(item.product_id),
            json=req,
            content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        items = Item.find_by_wishlist_id(test_wishlist.id)
        self.assertEqual(1, len([item.serialize() for item in items]))

        response = self.app.get(f"{BASE_URL}/{test_wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_wishlist.name)
        self.assertIsNotNone(data["items"][0]["id"])
        self.assertEqual(data["items"][0]["wishlist_id"], item.wishlist_id)
        self.assertEqual(data["items"][0]["product_id"], item.product_id)

    def test_get_wishlist_items(self):
        """It should Get a single Wishlist's items"""
        # get the id of a wishlist
        test_wishlist = self._create_wishlists(1)[0]

        item = ItemFactory()
        item.wishlist_id = test_wishlist.id

        req = {"customer_id":test_wishlist.customer_id}

        response = self.app.put(
            BASE_URL+"/"+str(test_wishlist.id)+"/products/"+str(item.product_id),
            json=req,
            content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        items = Item.find_by_wishlist_id(test_wishlist.id)
        self.assertEqual(1, len([item.serialize() for item in items]))

        response = self.app.get(f"{BASE_URL}/{test_wishlist.id}/items")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertIsNotNone(data[0]["id"])
        self.assertEqual(data[0]["wishlist_id"], item.wishlist_id)
        self.assertEqual(data[0]["product_id"], item.product_id)

    def test_get_wishlist_not_found(self):
        """It should not Get a wishlist thats not found"""
        response = self.app.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_get_wishlist_items_not_found(self):
        """It should not Get a wishlist's items thats not found"""
        response = self.app.get(f"{BASE_URL}/0/items")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

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

    def test_query_wishlist_list_by_customer_id(self):
        """It should Query Wishlists by Customer_ID"""
        wishlists = self._create_wishlists(10)
        test_customer_id = wishlists[0].customer_id
        customer_id_wishlists = []
        for wishlist in wishlists:
            if wishlist.customer_id == test_customer_id:
                customer_id_wishlists.append(wishlist)
        response = self.app.get(f"/wishlists/customer/{test_customer_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(customer_id_wishlists))
        # check the data just to be sure
        for wishlist in data:
            self.assertEqual(wishlist["customer_id"], test_customer_id)

    def test_delete_wishlist(self):
        """It should Delete a Wishlist"""
        test_wishlist = self._create_wishlists(1)[0]

        item = ItemFactory()
        item.wishlist_id = test_wishlist.id

        req = {"customer_id":test_wishlist.customer_id}

        response = self.app.put(
            BASE_URL+"/"+str(test_wishlist.id)+"/products/"+str(item.product_id),
            json=req,
            content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        items = Item.find_by_wishlist_id(test_wishlist.id)
        self.assertEqual(1, len([item.serialize() for item in items]))

        response = self.app.delete(f"{BASE_URL}/{test_wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.app.get(f"{BASE_URL}/{test_wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        items = Item.find_by_wishlist_id(test_wishlist.id)
        self.assertEqual(0, len([item.serialize() for item in items]))

    def test_update_wishlist_name(self):
        """It should Update the name of a wishlist """
        test_wishlist = WishlistFactory()
        logging.debug("Test Wishlist: %s", test_wishlist.serialize())
        response = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_wishlist = response.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name)

        # Check that the location header was correct
        response = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_wishlist = response.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name)

        # Update wishlist name
        test_wishlist.name = "Winter"

        response = self.app.put(
            BASE_URL+"/"+str(new_wishlist["id"]),
            json=test_wishlist.serialize(),
            content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()

        self.assertEqual(test_wishlist.name, data["name"])
        self.assertEqual(new_wishlist["id"], data["id"])
        self.assertEqual(new_wishlist["customer_id"], data["customer_id"])

    ######################################################################
    #  T E S T   S A D   P A T H S
    ######################################################################

    def test_create_wishlist_no_data(self):
        """It should not Create a Wishlist with missing data"""
        response = self.app.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wishlist_no_content_type(self):
        """It should not Create a Wishlist with no content type"""
        response = self.app.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_wishlist_no_customer_id(self):
        """It should not Create a Wishlist with no customer id"""
        response = self.app.post(BASE_URL, json={"id": 20, "name": "Summer"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wishlist_bad_customer_id(self):
        """It should not Create a Wishlist with bad Customer ID"""
        test_wishlist = WishlistFactory()
        logging.debug(test_wishlist)
        # change available to a string
        test_wishlist.customer_id = "fdgg"
        response = self.app.post(BASE_URL, json=test_wishlist.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wishlist_bad_customer_id_no_route(self):
        """It should not call a method for which there is no route"""
        response = self.app.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_by_customer_id_not_found(self):
        """It should return HTTP 404 not found"""
        customer_id = -1
        response = self.app.get(f"/wishlists/customer/{customer_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_wishlist_name_wishlist_not_found(self):
        """It should return HTTP 404 not found """
        test_wishlist = WishlistFactory()
        logging.debug("Test Wishlist: %s", test_wishlist.serialize())
        response = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update wishlist name
        test_wishlist.name = "Winter"

        response = self.app.put(
            BASE_URL+"/0",
            json=test_wishlist.serialize(),
            content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_wishlist_name_customer_not_found(self):
        """It should return HTTP 404 not found """
        test_wishlist = WishlistFactory()
        logging.debug("Test Wishlist: %s", test_wishlist.serialize())
        response = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the data is correct
        new_wishlist = response.get_json()

        # Update wishlist name
        test_wishlist.name = "Winter"
        test_wishlist.customer_id = 0

        response = self.app.put(
            BASE_URL+"/"+str(new_wishlist["id"]),
            json=test_wishlist.serialize(),
            content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_product_to_wishlist(self):
        """Adds products to a wishlist """
        test_wishlist = WishlistFactory()
        logging.debug("Test Wishlist: %s", test_wishlist.serialize())
        response = self.app.post(
            BASE_URL,
            json=test_wishlist.serialize(),
            content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_wishlist = response.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name)

        # Check that the location header was correct
        response = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_wishlist = response.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name)

        item = ItemFactory()
        item.wishlist_id = new_wishlist["id"]

        req = {"customer_id":test_wishlist.customer_id}

        response = self.app.put(
            BASE_URL+"/"+str(new_wishlist["id"])+"/products/"+str(item.product_id),
            json=req,
            content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()

        self.assertIsNotNone(item.id)
        self.assertEqual(item.wishlist_id, data["wishlist_id"])
        self.assertEqual(item.product_id, data["product_id"])

        req = {"customer_id":test_wishlist.customer_id}

        response = self.app.put(
            BASE_URL+"/"+str(new_wishlist["id"])+"/products/"+str(item.product_id),
            json=req,
            content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()

        self.assertIsNotNone(item.id)
        self.assertEqual(item.wishlist_id, data["wishlist_id"])
        self.assertEqual(item.product_id, data["product_id"])

    def test_add_product_to_wishlist_does_not_exist(self):
        """Adds products to a wishlist, check where wishlist or customer does not exist """
        test_wishlist = WishlistFactory()
        logging.debug("Test Wishlist: %s", test_wishlist.serialize())
        response = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the data is correct
        new_wishlist = response.get_json()

        item = ItemFactory()
        item.wishlist_id = new_wishlist["id"]

        req = {"customer_id":10}

        response = self.app.put(
            BASE_URL+"/"+str(new_wishlist["id"])+"/products/"+str(item.product_id),
            json=req,
            content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.app.put(
            BASE_URL+"/"+str(test_wishlist.customer_id)+"/"+str(10)+"/"+str(item.product_id), content_type=CONTENT_TYPE_JSON
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
