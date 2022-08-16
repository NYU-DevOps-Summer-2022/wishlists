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
BASE_URL = "/api/wishlists"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   W I S H L I S T   S E R V I C E
######################################################################
class TestWishlistServer(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        self.app = app.test_client()
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.query(Item).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
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
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test wishlist",
            )
            new_wishlist = response.get_json()
            test_wishlist.id = new_wishlist["id"]
            wishlists.append(test_wishlist)
        return wishlists

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_health(self):
        """It should test the health API"""
        response = self.app.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "OK")

    def test_index(self):
        """It should return the index page"""
        response = self.app.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Wishlists REST API Service", response.data)

    def test_get_wishlist_list(self):
        """It should Get a list of Wishlists"""
        self._create_wishlists(7)
        response = self.app.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        print(data)
        self.assertEqual(len(data), 7)

    def test_get_wishlist(self):
        """It should Get a single Wishlist"""
        # get the id of a wishlist
        test_wishlist = self._create_wishlists(1)[0]

        item = ItemFactory()
        item.wishlist_id = test_wishlist.id

        req = {"customer_id": test_wishlist.customer_id, "product_id": item.product_id}

        response = self.app.post(
            BASE_URL + "/" + str(test_wishlist.id) + "/items",
            json=req,
            content_type=CONTENT_TYPE_JSON,
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

        req = {"customer_id": test_wishlist.customer_id, "product_id": item.product_id}

        response = self.app.post(
            BASE_URL + "/" + str(test_wishlist.id) + "/items",
            json=req,
            content_type=CONTENT_TYPE_JSON,
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

    def test_clear_wishlist_items(self):
        """It should clear a single Wishlist's items"""
        # get the id of a wishlist
        test_wishlist = self._create_wishlists(1)[0]

        item = ItemFactory()
        item.wishlist_id = test_wishlist.id

        req = {"customer_id": test_wishlist.customer_id, "product_id": item.product_id}

        response = self.app.post(
            BASE_URL + "/" + str(test_wishlist.id) + "/items",
            json=req,
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        items = Item.find_by_wishlist_id(test_wishlist.id)
        self.assertEqual(1, len([item.serialize() for item in items]))

        response = self.app.get(f"{BASE_URL}/{test_wishlist.id}/items")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        print(data)
        self.assertIsNotNone(data[0]["id"])
        self.assertEqual(data[0]["wishlist_id"], item.wishlist_id)
        self.assertEqual(data[0]["product_id"], item.product_id)

        response = self.app.put(
            BASE_URL + "/" + str(test_wishlist.id) + "/clear",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(data["customer_id"], test_wishlist.customer_id)
        self.assertEqual(data["name"], test_wishlist.name)
        self.assertEqual(len(data["items"]), 0)

        response = self.app.put(
            BASE_URL + "/" + str(test_wishlist.id + 1) + "/clear",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_wishlist_item_by_id(self):
        """It should Get a single Wishlist's item by id"""
        # get the id of a wishlist
        test_wishlist = self._create_wishlists(1)[0]

        item = ItemFactory()
        item.wishlist_id = test_wishlist.id

        req = {"customer_id": test_wishlist.customer_id, "product_id": item.product_id}

        response = self.app.post(
            BASE_URL + "/" + str(test_wishlist.id) + "/items",
            json=req,
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        items = Item.find_by_wishlist_id(test_wishlist.id)
        result = [item.serialize() for item in items][0]

        response = self.app.get(f"{BASE_URL}/{test_wishlist.id}/items/{result['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["id"], result["id"])
        self.assertEqual(data["wishlist_id"], item.wishlist_id)
        self.assertEqual(data["product_id"], item.product_id)

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

    def test_get_wishlist_item_id_not_found(self):
        """It should not Get a wishlist's item id thats not found"""
        response = self.app.get(f"{BASE_URL}/0/items/1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

        test_wishlist = self._create_wishlists(1)[0]
        response = self.app.get(f"{BASE_URL}/{test_wishlist.id}/items/1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found with item", data["message"])

    def test_create_wishlist(self):
        """It should Create a new Wishlist"""
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

    def test_query_wishlist_list_by_param(self):
        """It should Query Wishlists by Customer_ID"""
        wishlists = self._create_wishlists(10)
        test_customer_id = wishlists[0].customer_id
        test_name = wishlists[2].name
        customer_id_wishlists = []
        name_wishlists = []

        test_cust_id = wishlists[2].customer_id
        test_cust_name = wishlists[2].name

        # multi param
        cust_name_wishlists = []

        for wishlist in wishlists:
            if wishlist.customer_id == test_customer_id:
                customer_id_wishlists.append(wishlist)

            if wishlist.name == test_name:
                name_wishlists.append(wishlist)

            if (wishlist.customer_id == test_cust_id) and (
                wishlist.name == test_cust_name
            ):
                cust_name_wishlists.append(wishlist)

        response = self.app.get(
            BASE_URL, query_string=f"customer_id={test_customer_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(customer_id_wishlists))
        # check the data just to be sure
        for wishlist in data:
            self.assertEqual(wishlist["customer_id"], test_customer_id)

        response = self.app.get(
            BASE_URL, query_string=f"customer_id={test_cust_id}&name={test_cust_name}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(cust_name_wishlists))
        # check the data just to be sure
        for wishlist in data:
            self.assertEqual(wishlist["customer_id"], test_cust_id)
            self.assertEqual(wishlist["name"], test_cust_name)

        response = self.app.get(BASE_URL, query_string=f"name={test_name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(name_wishlists))
        # check the data just to be sure
        for wishlist in data:
            self.assertEqual(wishlist["name"], test_name)

    def test_query_wishlist_list_by_customer_id(self):
        """It should Query Wishlists by Customer_ID"""
        wishlists = self._create_wishlists(10)
        test_customer_id = wishlists[0].customer_id
        customer_id_wishlists = []
        for wishlist in wishlists:
            if wishlist.customer_id == test_customer_id:
                customer_id_wishlists.append(wishlist)
        response = self.app.get(
            BASE_URL, query_string=f"customer_id={test_customer_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(customer_id_wishlists))
        # check the data just to be sure
        for wishlist in data:
            self.assertEqual(wishlist["customer_id"], test_customer_id)

    def test_delete_wishlist_item(self):
        """It should Delete a Wishlist Item"""
        test_wishlist = self._create_wishlists(1)[0]
        item = ItemFactory()
        item.wishlist_id = test_wishlist.id

        req = {"customer_id": test_wishlist.customer_id, "product_id": item.product_id}

        response = self.app.post(
            BASE_URL + "/" + str(test_wishlist.id) + "/items",
            json=req,
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        items = Item.find_by_wishlist_id(test_wishlist.id)
        result = [item.serialize() for item in items][0]

        # delete an item request
        response = self.app.delete(
            f"{BASE_URL}/{test_wishlist.id}/items/{result['id']}"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # To check the item has been deleted
        response = self.app.get(f"{BASE_URL}/{test_wishlist.id}/items/{result['id']}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_wishlist(self):
        """It should Delete a Wishlist"""
        test_wishlist = self._create_wishlists(1)[0]

        item = ItemFactory()
        item.wishlist_id = test_wishlist.id

        req = {"customer_id": test_wishlist.customer_id, "product_id": item.product_id}

        response = self.app.post(
            BASE_URL + "/" + str(test_wishlist.id) + "/items",
            json=req,
            content_type=CONTENT_TYPE_JSON,
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
        """It should Update the name of a wishlist"""
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
            BASE_URL + "/" + str(new_wishlist["id"]),
            json=test_wishlist.serialize(),
            content_type=CONTENT_TYPE_JSON,
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
        response = self.app.post(BASE_URL, json={"customer_id":20, "name": "Summer"},  content_type="text/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
        response = self.app.get(f"{BASE_URL}/customer/{customer_id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_wishlist_name_wishlist_not_found(self):
        """It should return HTTP 404 not found"""
        test_wishlist = WishlistFactory()
        logging.debug("Test Wishlist: %s", test_wishlist.serialize())
        response = self.app.post(
            BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update wishlist name
        test_wishlist.name = "Winter"

        response = self.app.put(
            BASE_URL + "/0",
            json=test_wishlist.serialize(),
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_wishlist_name_customer_not_found(self):
        """It should return HTTP 404 not found"""
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
            BASE_URL + "/" + str(new_wishlist["id"]),
            json=test_wishlist.serialize(),
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_product_to_wishlist(self):
        """Adds products to a wishlist"""
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

        item = ItemFactory()
        item.wishlist_id = new_wishlist["id"]

        req = {"customer_id": test_wishlist.customer_id, "product_id": item.product_id}

        response = self.app.post(
            BASE_URL + "/" + str(new_wishlist["id"]) + "/items",
            json=req,
            content_type=CONTENT_TYPE_JSON,
        )
        print(response.get_json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()

        self.assertIsNotNone(item.id)
        self.assertEqual(item.wishlist_id, data["wishlist_id"])
        self.assertEqual(item.product_id, data["product_id"])

        req = {"customer_id": test_wishlist.customer_id, "product_id": item.product_id}

        response = self.app.post(
            BASE_URL + "/" + str(new_wishlist["id"]) + "/items",
            json=req,
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()

        self.assertIsNotNone(item.id)
        self.assertEqual(item.wishlist_id, data["wishlist_id"])
        self.assertEqual(item.product_id, data["product_id"])

    def test_update_wishlist_item(self):
        """Updates wishlist item"""
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
        # response = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_wishlist = response.get_json()
        # self.assertEqual(new_wishlist["name"], test_wishlist.name)

        item = ItemFactory()
        item.wishlist_id = new_wishlist["id"]

        req = {"product_id": item.product_id}

        response = self.app.post(
            BASE_URL + "/" + str(new_wishlist["id"]) + "/items",
            json=req,
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.get_json()

        self.assertIsNotNone(item.id)
        self.assertEqual(item.wishlist_id, data["wishlist_id"])
        self.assertEqual(item.product_id, data["product_id"])

        req = {"product_id": 204}

        response = self.app.put(
            BASE_URL + "/" + str(new_wishlist["id"]) + "/items/" + str(data["id"]),
            json=req,
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()

        self.assertIsNotNone(item.id)
        self.assertEqual(item.wishlist_id, data["wishlist_id"])
        self.assertEqual(204, data["product_id"])

        # wishlist not found case
        response = self.app.put(
            BASE_URL + "/" + str(new_wishlist["id"] + 1) + "/items/1232",
            json=req,
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # item not found case
        response = self.app.put(
            BASE_URL + "/" + str(new_wishlist["id"]) + "/items/1232",
            json=req,
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_product_to_wishlist_does_not_exist(self):
        """Adds products to a wishlist, check where wishlist or customer does not exist"""
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

        req = {
            "product_id": item.product_id,
        }

        response = self.app.post(
            BASE_URL + "/" + str(new_wishlist["id"] + 1) + "/items",
            json=req,
            content_type=CONTENT_TYPE_JSON,
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
