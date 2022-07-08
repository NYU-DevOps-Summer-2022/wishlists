"""
Test cases for Wishlist Model

"""
import os
import logging
import unittest
from werkzeug.exceptions import NotFound
from service.models import Wishlist, Item, DataValidationError, db
from service import app
from tests.factories import WishlistFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  W I S H L I S T   M O D E L   T E S T   C A S E S
######################################################################
class TestWishlist(unittest.TestCase):
    """Test Cases for Wishlist Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Wishlist.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_wishlist(self):
        """It should Create a wishlist and assert that it exists"""
        wishlist = Wishlist(name="AccessoriesList", customer_id=20)
        self.assertEqual(str(wishlist), "<Wishlist 'AccessoriesList' id=[None]>")
        self.assertTrue(wishlist is not None)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.name, "AccessoriesList")
        self.assertEqual(wishlist.customer_id, 20)
        wishlist = Wishlist(name="AccessoriesList2")
        self.assertTrue(wishlist is not None)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.name, "AccessoriesList2")
        self.assertEqual(wishlist.customer_id, None)

    def test_add_a_wishlist(self):
        """It should Create a wishlist and add it to the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = Wishlist(name="Summer", customer_id=20)
        self.assertTrue(wishlist is not None)
        self.assertEqual(wishlist.id, None)
        wishlist.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        # Add another entry and assert that the length of database is 2
        wishlist = Wishlist(name="Winter", customer_id=22)
        self.assertTrue(wishlist is not None)
        self.assertEqual(wishlist.id, None)
        wishlist.create()
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 2)

    def test_read_a_wishlist(self):
        """It should Read a Wishlist"""
        wishlist = WishlistFactory()
        logging.debug(wishlist)
        wishlist.id = None
        wishlist.create()
        self.assertIsNotNone(wishlist.id)
        # Fetch it back
        found_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(found_wishlist.id, wishlist.id)
        self.assertEqual(found_wishlist.name, wishlist.name)
        self.assertEqual(found_wishlist.customer_id, wishlist.customer_id)

    def test_delete_a_wishlist(self):
        """It should Delete a Wishlist"""
        wishlist = WishlistFactory()
        wishlist.create()
        self.assertEqual(len(Wishlist.all()), 1)
        # delete the wishlist and make sure it isn't in the database
        wishlist.delete()
        self.assertEqual(len(Wishlist.all()), 0)

    def test_serialize_a_wishlist(self):
        """It should serialize a wishlist"""
        wishlist = WishlistFactory()
        data = wishlist.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], wishlist.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], wishlist.name)
        self.assertIn("customer_id", data)
        self.assertEqual(data["customer_id"], wishlist.customer_id)

    def test_deserialize_a_wishlist(self):
        """It should de-serialize a wishlist"""
        data = WishlistFactory().serialize()
        wishlist = Wishlist()
        wishlist.deserialize(data)
        self.assertNotEqual(wishlist, None)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.name, data["name"])
        self.assertEqual(wishlist.customer_id, data["customer_id"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a Wishlist with missing data"""
        data = {"id": 1, "name": "Summer"}
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, data)
        data = {"id": 2, "customer_id": 23}
        self.assertRaises(DataValidationError, wishlist.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "random data"
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, data)

    def test_deserialize_bad_available(self):
        """It should not deserialize a bad customer_id attribute"""
        test_wishlist = WishlistFactory()
        data = test_wishlist.serialize()
        data["customer_id"] = 3.456
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, data)
        data["customer_id"] = "sdfg"
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, data)
        data["customer_id"] = False
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, data)

    def test_find_wishlist(self):
        """It should Find a wishlist by ID"""
        wishlists = WishlistFactory.create_batch(5)
        for wishlist in wishlists:
            wishlist.create()
        logging.debug(wishlists)
        # make sure they got saved
        self.assertEqual(len(Wishlist.all()), 5)
        # find the 2nd wishlist in the list
        wishlist = Wishlist.find(wishlists[1].id)
        self.assertIsNot(wishlist, None)
        self.assertEqual(wishlist.id, wishlists[1].id)
        self.assertEqual(wishlist.name, wishlists[1].name)
        self.assertEqual(wishlist.customer_id, wishlists[1].customer_id)
        # find the last wishlist in the list
        wishlist = Wishlist.find(wishlists[-1].id)
        self.assertIsNot(wishlist, None)
        self.assertEqual(wishlist.id, wishlists[-1].id)
        self.assertEqual(wishlist.name, wishlists[-1].name)
        self.assertEqual(wishlist.customer_id, wishlists[-1].customer_id)

    def test_find_by_name(self):
        """It should Find a Wishlist by Name"""
        wishlists = WishlistFactory.create_batch(5)
        for wishlist in wishlists:
            wishlist.create()
        logging.debug(wishlists)
        name = wishlists[3].name
        found = Wishlist.find_by_name(name)
        self.assertEqual(found.count(), 1)
        self.assertEqual(found[0].name, wishlists[3].name)
        self.assertEqual(found[0].customer_id, wishlists[3].customer_id)

    def test_find_by_customer_id(self):
        """It should Find Wishlists by Customer_IDs"""
        wishlists = WishlistFactory.create_batch(10)
        for wishlist in wishlists:
            wishlist.create()
        logging.debug(wishlists)
        customer_id = wishlists[0].customer_id
        count = len(
            [wishlist for wishlist in wishlists if wishlist.customer_id == customer_id]
        )
        found = Wishlist.find_by_customer_id(customer_id)
        self.assertEqual(found.count(), count)
        for wishlist in found:
            self.assertEqual(wishlist.customer_id, customer_id)

    def test_find_or_404_found(self):
        """It should Find or return 404 not found"""
        wishlists = WishlistFactory.create_batch(10)
        for wishlist in wishlists:
            wishlist.create()
        logging.debug(wishlists)

        wishlist = Wishlist.find_or_404(wishlists[6].id)
        self.assertIsNot(wishlist, None)
        self.assertEqual(wishlist.id, wishlists[6].id)
        self.assertEqual(wishlist.name, wishlists[6].name)
        self.assertEqual(wishlist.customer_id, wishlists[6].customer_id)

    def test_find_or_404_not_found(self):
        """It should return 404 not found"""
        self.assertRaises(NotFound, Wishlist.find_or_404, 0)


######################################################################
#  I T E M   M O D E L   T E S T   C A S E S
######################################################################
class TestItem(unittest.TestCase):
    """Test Cases for Item Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Item.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_wishlist_item(self):
        """It should Create a wishlist item and assert that it exists"""
        item = Item(wishlist_id=1, product_id=10)
        self.assertEqual(str(item), "<Item id=[None] wishlist_id=[1] product_id=[10]>")
        self.assertTrue(item is not None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.wishlist_id, 1)
        self.assertEqual(item.product_id, 10)

    def test_find_by_wishlist_id_and_product_id(self):
        """It should find wishlist items by wishlist id and product id"""
        wishlist = WishlistFactory()
        logging.debug(wishlist)
        wishlist.id = None
        wishlist.create()
        self.assertIsNotNone(wishlist.id)

        item = Item(wishlist_id=wishlist.id, product_id=10)
        item.create()

        logging.debug(item)

        items = Item.find_by_wishlist_id_and_product_id(wishlist.id, 10)

        results = [item.serialize() for item in items]

        self.assertGreater(len(results), 0)

    def test_find_by_wishlist_id_and_item_id(self):
        """It should find wishlist items by wishlist id and item id"""
        wishlist = WishlistFactory()
        logging.debug(wishlist)
        wishlist.id = None
        wishlist.create()
        self.assertIsNotNone(wishlist.id)

        item = Item(wishlist_id=wishlist.id, product_id=10)
        item.create()

        logging.debug(item)

        items = Item.find_by_wishlist_id_and_item_id(wishlist.id, item.id)

        results = [item.serialize() for item in items]

        self.assertGreater(len(results), 0)
