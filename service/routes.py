"""
Wishlist Service

Paths:
------
POST /wishlists - creates a new Wishlist record in the database
"""

from flask import jsonify, request, abort, make_response
from flask_restx import Resource, fields, reqparse
from service.utils import status  # HTTP Status Codes
from service.models import Wishlist, Item

# Import Flask application
from . import app, api


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return app.send_static_file("index.html")


######################################################################
# GET WISHLIST INDEX (ITEMS)
######################################################################
@app.route("/wishlists/<int:wishlist_id>/view")
def wishlist_index(wishlist_id):
    """Root URL response"""
    app.logger.info("Request for wishlist %s view", wishlist_id)

    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        return app.send_static_file("wishlist_not_found.html")

    return app.send_static_file("wishlist_index.html")


# Dict to hold the data of each item in a wishlist
# items_fields = {
#     "id": fields.Integer(required=True, description="The unique assigned"),
#     "product_id": fields.Integer(
#         required=True, description="The ID unique to each product"
#     ),
#     "wishlist_id": fields.Integer(
#         required=True, description="The ID unique to each Wishlist"
#     ),
# }

# Define the Item model so that the docs reflect what can be sent
create_model_2 = api.model(
    "Item",
    {
        "wishlist_id": fields.Integer(
            required=True, description="The ID unique to each Wishlist"
        ),
        "product_id": fields.Integer(
            required=True, description="The ID unique to each Product"
        ),
    },
)

item_model = api.inherit(
    "ItemModel",
    create_model_2,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# Define the model so that the docs reflect what can be sent
create_model = api.model(
    "Wishlist",
    {
        "name": fields.String(required=True, description="The name of the Wishlist"),
        "customer_id": fields.Integer(
            required=True, description="The ID unique to each customer"
        ),
        "items": fields.List(
            fields.Nested(
                item_model,
                required=False,
                description="Nested dictionary to access the items schema",
            ),
        ),
    },
)

wishlist_model = api.inherit(
    "WishlistModel",
    create_model,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)


create_model_3 = api.model(
    "Simple_Wishlist",
    {
        "name": fields.String(required=True, description="The name of the Wishlist"),
        "customer_id": fields.Integer(
            required=True, description="The ID unique to each customer"
        ),
    },
)

simple_wishlist_model = api.inherit(
    "Simple_Wishlist_Model",
    create_model_3,
    {
        "id": fields.Integer(
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# query string arguments
wishlist_args = reqparse.RequestParser()
wishlist_args.add_argument(
    "name", type=str, required=False, help="List Wishlist by name", location="args"
)
wishlist_args.add_argument(
    "customer_id",
    type=int,
    required=False,
    help="List Wishlist by customer id",
    location="args",
)


######################################################################
#  PATH: /wishlists/{id}
######################################################################
@api.route("/wishlists/<int:wishlist_id>")
@api.param("wishlist_id", "The Wishlist identifier")
class WishlistResource(Resource):
    """
    WishlistResource class

    Allows the manipulation of a single Wishlist
    GET /wishlists/{id} - Returns a wishlist with the id
    PUT /wishlists/{id} - Update a wishlist with the id
    DELETE /wishlists/{id} -  Deletes a wishlist with the id
    """

    # ---------------------------------------------------------------------
    # RETRIEVE A WISHLIST
    # ---------------------------------------------------------------------
    @api.doc("get_wishlists")
    @api.response(404, "Wishlist not found")
    @api.marshal_with(wishlist_model)
    def get(self, wishlist_id):
        """
        Retrieve a single Wishlist

        This endpoint will return a Wishlist based on it's id
        """
        app.logger.info("Request for wishlist with id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with id '{wishlist_id}' was not found.",
            )

        app.logger.info("Returning wishlist: %s", wishlist.name)

        response = wishlist.serialize()

        response["items"] = [
            item.serialize() for item in Item.find_by_wishlist_id(wishlist_id)
        ]

        return response, status.HTTP_200_OK

    # ---------------------------------------------------------------------
    # UPDATE WISHLIST NAME
    # ---------------------------------------------------------------------
    @api.doc("update_wishlists")
    @api.response(404, "Wishlist not found")
    @api.response(400, "The posted wishlist data was not valid")
    @api.expect(wishlist_model)
    @api.marshal_with(wishlist_model)
    def put(self, wishlist_id):
        """
        Updates a Wishlist name
        This endpoint will update a Wishlist name based on the data in the body
        """

        app.logger.info("Request to update a wishlist")
        check_content_type("application/json")

        req = api.payload

        # TODO : validate param
        customer_id = req["customer_id"]

        wishlists = []
        app.logger.info("Request for wishlists with customer id: %s", customer_id)

        wishlists = Wishlist.find_by_customer_id(customer_id)

        results = [wishlist.serialize() for wishlist in wishlists]

        if len(results) == 0:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with customer id '{customer_id}' was not found.",
            )

        if not any(wishlist["id"] == wishlist_id for wishlist in results):
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with customer id '{customer_id}' and id '{wishlist_id}' was not found.",
            )

        wishlist = Wishlist.find(wishlist_id)
        req = api.payload
        wishlist.name = req["name"]
        wishlist.update()

        message = wishlist.serialize()

        message["items"] = [
            item.serialize() for item in Item.find_by_wishlist_id(wishlist_id)
        ]

        return message, status.HTTP_200_OK

    # ---------------------------------------------------------------------
    # DELETE A WISHLIST
    # ---------------------------------------------------------------------
    @api.doc("delete_wishlists")
    @api.response(204, "Wishlist deleted")
    def delete(self, wishlist_id):
        """
        Delete a Wishlist

        This endpoint will delete a Wishlist based the id specified in the path
        """
        app.logger.info("Request to delete wishlist with id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if wishlist:
            wishlist.delete()

        app.logger.info("Wishlist with ID [%s] delete complete.", wishlist_id)
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /wishlists
######################################################################
@api.route("/wishlists", strict_slashes=False)
class WishlistCollection(Resource):
    """Handles all interactions with collections of Wishlists"""

    # ---------------------------------------------------------------------
    # LIST ALL WISHLISTS
    # ---------------------------------------------------------------------
    @api.doc("list_wishlists")
    @api.expect(wishlist_args, validate=True)
    @api.marshal_list_with(wishlist_model)
    def get(self):
        """Returns all of the Wishlists"""
        app.logger.info("Request for the list of wishlists")
        wishlists = []

        # print(request.args.keys())
        args = wishlist_args.parse_args()

        # name = request.args.get("name", None)
        # customer_id = request.args.get("customer_id", None)

        query = {"name": args["name"], "customer_id": args["customer_id"]}

        if args["name"] or args["customer_id"]:
            wishlists = Wishlist.find_by_param(query)
        else:
            wishlists = Wishlist.all()

        results = []
        if wishlists is not None:
            wishlist_results = [wishlist.serialize() for wishlist in wishlists]
            for wishlist in wishlist_results:
                wishlist["items"] = [
                    item.serialize()
                    for item in Item.find_by_wishlist_id(wishlist["id"])
                ]
                results.append(wishlist)
        app.logger.info("Returning %d wishlists", len(results))

        # print(results)
        return results, status.HTTP_200_OK

    # ---------------------------------------------------------------------
    # ADD A NEW WISHLIST
    # ---------------------------------------------------------------------
    @api.doc("create_wishlists")
    @api.response(400, "The posted data was not valid")
    @api.expect(wishlist_model)
    @api.marshal_with(wishlist_model, code=201)
    def post(self):
        """
        Creates a Wishlist
        This endpoint will create a Wishlist based the data in the body that is posted
        """
        app.logger.info("Request to create a wishlist")
        check_content_type("application/json")
        wishlist = Wishlist()
        wishlist.deserialize(api.payload)
        wishlist.create()
        message = wishlist.serialize()
        message["items"] = []
        location_url = api.url_for(
            WishlistResource, wishlist_id=wishlist.id, _external=True
        )

        app.logger.info("Wishlist with ID [%s] created.", wishlist.id)
        return message, status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /wishlists/{id}/clear
######################################################################
@api.route("/wishlists/<int:wishlist_id>/clear")
@api.param("wishlist_id", "The Wishlist identifier")
class ClearResource(Resource):
    """Clear action on a Wishlist"""

    @api.doc("clear_wishlist")
    @api.response(404, "Wishlist not found")
    def put(self, wishlist_id):
        """
        Clear a Wishlist

        This endpoint will clear a Wishlist based the id specified in the path
        """
        app.logger.info("Request to clear wishlist with id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with id '{wishlist_id}' was not found.",
            )

        items = Item.find_by_wishlist_id(wishlist_id)

        for item in items:
            item.delete()

        response = wishlist.serialize()

        response["items"] = [
            item.serialize() for item in Item.find_by_wishlist_id(wishlist_id)
        ]

        return response, status.HTTP_200_OK


######################################################################
#  PATH: /wishlists/{id}/items
######################################################################
@api.route("/wishlists/<int:wishlist_id>/items", strict_slashes=False)
class WishlistItemsCollection(Resource):
    """Handles all interactions with collections of Items in a wishlist"""

    # ---------------------------------------------------------------------
    # RETRIEVE A WISHLIST'S ITEMS
    # ---------------------------------------------------------------------
    @api.doc("list_wishlists_items")
    @api.expect(wishlist_args, validate=True)
    @api.marshal_list_with(item_model)
    def get(self, wishlist_id):
        """
        Retrieve a Wishlist's items

        This endpoint will return a Wishlist's items based on it's id
        """
        app.logger.info("Request for wishlist items with wishlist_id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with id '{wishlist_id}' was not found.",
            )

        app.logger.info("Returning wishlist: %s", wishlist.name)

        response = [item.serialize() for item in Item.find_by_wishlist_id(wishlist_id)]

        return response, status.HTTP_200_OK

    # ---------------------------------------------------------------------
    # CREATE WISHLIST ITEM
    # ---------------------------------------------------------------------
    @api.doc("create_wishlist_items")
    @api.response(400, "The posted data was not valid")
    @api.expect(wishlist_model)
    @api.marshal_with(item_model, code=201)
    def post(self, wishlist_id):
        """
        Updates a Wishlist, adds products
        This endpoint will add a new product to a wishlist
        """

        app.logger.info("Request to create a wishlist item")
        check_content_type("application/json")

        req = api.payload

        # TODO : validate param
        product_id = req["product_id"]

        # check for existence
        Wishlist.find_or_404(wishlist_id)

        items = Item.find_by_wishlist_id_and_product_id(wishlist_id, product_id)
        results = [item.serialize() for item in items]

        if len(results) != 0:
            # already exists, so return same object
            message = results[0]
            return message, status.HTTP_200_OK

        item = Item()
        item.deserialize(wishlist_id, product_id)
        item.create()
        message = item.serialize()

        return message, status.HTTP_201_CREATED


######################################################################
#  PATH: /wishlists/{id}/items/{id}
######################################################################
@api.route("/wishlists/<int:wishlist_id>/items/<int:item_id>")
@api.param("wishlist_id", "The Wishlist identifier")
@api.param("item_id", "The Item identifier")
class WishlistItemResource(Resource):
    # ---------------------------------------------------------------------
    # RETRIEVE A WISHLIST'S ITEM BY ID
    # ---------------------------------------------------------------------
    @api.doc("get_wishlists_item_by_id")
    @api.response(404, "Item not found")
    @api.marshal_with(item_model)
    def get(self, wishlist_id, item_id):
        """
        Retrieve a Wishlist's items

        This endpoint will return a Wishlist's items based on it's id
        """
        app.logger.info("Request for wishlist items with wishlist_id: %s", wishlist_id)
        wishlist = Wishlist.find(wishlist_id)
        if not wishlist:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with id '{wishlist_id}' was not found.",
            )

        app.logger.info("Returning wishlist: %s", wishlist.name)

        response = [
            item.serialize()
            for item in Item.find_by_wishlist_id_and_item_id(wishlist_id, item_id)
        ]

        if len(response) == 0:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist with id '{wishlist_id}' was not found with item '{item_id}'",
            )

        return response[0], status.HTTP_200_OK

    # ---------------------------------------------------------------------
    # UPDATE WISHLIST ITEM
    # ---------------------------------------------------------------------
    @api.doc("update_wishlist_items")
    @api.response(404, "Item not found")
    @api.response(400, "The posted Item data was not valid")
    @api.expect(wishlist_model)
    @api.marshal_with(item_model)
    def put(self, wishlist_id, item_id):
        """
        Updates a wishlist item
        """

        app.logger.info("Request to update a wishlist item")
        check_content_type("application/json")

        req = api.payload

        # TODO : validate param
        product_id = req["product_id"]

        app.logger.info(
            "Request for wishlists with wishlist_id id: %s and item_id: %s",
            wishlist_id,
            item_id,
        )

        # check for existence
        Wishlist.find_or_404(wishlist_id)

        items = Item.find_by_wishlist_id_and_item_id(wishlist_id, item_id)

        message = ""

        results = [item.deserialize(wishlist_id, product_id) for item in items]

        if len(results) > 0:
            item = results[0]
            item.update()

            message = item.serialize()

        else:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Wishlist item {item_id} not found",
            )

        return message, status.HTTP_200_OK

    # ---------------------------------------------------------------------
    # DELETE A WISHLIST ITEM
    # ---------------------------------------------------------------------
    @api.doc("delete_pets")
    @api.response(204, "Item deleted")
    def delete(self, wishlist_id, item_id):
        """
        Delete a Wishlist Item
        This endpoint will delete a Product based on the product id
        """
        app.logger.info(
            "Request to delete Product %s for Wishlist id: %s", (item_id, wishlist_id)
        )

        item = Item.find_by_wishlist_id_and_item_id(wishlist_id, item_id)
        if item:
            item.delete()

        return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """Initializes the SQLAlchemy app"""
    global app
    Wishlist.init_db(app)


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
