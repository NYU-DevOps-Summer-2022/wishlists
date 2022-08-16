"""
Test Factory to make fake objects for testing
"""
import factory
import random
from service.models import Item, Wishlist


class WishlistFactory(factory.Factory):
    """Creates fake Wishlists"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Wishlist

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    customer_id = factory.LazyAttribute(lambda x: random.randrange(0, 10000))


class ItemFactory(factory.Factory):
    """Creates fake Wishlist items"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Item

    id = factory.Sequence(lambda n: n)
    wishlist_id = factory.LazyAttribute(lambda x: random.randrange(0, 10000))
    product_id = factory.LazyAttribute(lambda x: random.randrange(0, 10000))
    product_name = factory.Faker("name")
    product_price = factory.LazyAttribute(lambda x: random.randrange(20, 10000))
