"""
Wishlist Service

Paths:
------
POST /wishlists - creates a new Wishlist record in the database
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from service.utils import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Wishlist, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Wishlist Demo REST API Service",
            version="1.0",
            paths=url_for("create_wishlists", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# LIST ALL WISHLISTS
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """Returns all of the Wishlists"""
    app.logger.info("Request for the list of wishlists")
    wishlists = []
    print(request.args.keys())
    name = request.args.get("name")
    customer_id = request.args.get("customer_id")
    if customer_id:
        wishlists = Wishlist.find_by_customer_id(customer_id)
    elif name:
        wishlists = Wishlist.find_by_name(name)
    else:
        wishlists = Wishlist.all()
    results = [wishlist.serialize() for wishlist in wishlists]
    app.logger.info("Returning %d wishlists", len(results))
    return jsonify(results), status.HTTP_200_OK

######################################################################
# RETRIEVE A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["GET"])
def get_wishlists(wishlist_id):
    """
    Retrieve a single Wishlist

    This endpoint will return a Wishlist based on it's id
    """
    app.logger.info("Request for wishlist with id: %s", wishlist_id)
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(status.HTTP_404_NOT_FOUND, f"Wishlist with id '{wishlist_id}' was not found.")

    app.logger.info("Returning wishlist: %s", wishlist.name)
    return jsonify(wishlist.serialize()), status.HTTP_200_OK

######################################################################
# RETRIEVE WISHLISTS OF A CUSTOMER
######################################################################
@app.route("/wishlists/customer/<int:customer_id>", methods=["GET"])
def get_wishlists_customerID(customer_id):
    """
    Retrieve a all wishlists with a specific customer id
    This endpoint will return any Wishlist based on it's id
    """
    wishlists = []
    app.logger.info("Request for wishlists with customer id: %s", customer_id)
    wishlists = Wishlist.find_by_customer_id(customer_id)
    if not wishlists:
        abort(status.HTTP_404_NOT_FOUND, f"Wishlist with customer id '{customer_id}' was not found.")

    results = [wishlist.serialize() for wishlist in wishlists]
    app.logger.info("Returning %s wishlist", len(results))
    return jsonify(results), status.HTTP_200_OK

######################################################################
# ADD A NEW WISHLIST
######################################################################
@app.route("/wishlists", methods=["POST"])
def create_wishlists():
    """
    Creates a Wishlist
    This endpoint will create a Wishlist based the data in the body that is posted
    """
    app.logger.info("Request to create a wishlist")
    check_content_type("application/json")
    wishlist = Wishlist()
    wishlist.deserialize(request.get_json())
    wishlist.create()
    message = wishlist.serialize()
    location_url = url_for("get_wishlists", wishlist_id=wishlist.id, _external=True)

    app.logger.info("Wishlist with ID [%s] created.", wishlist.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}

######################################################################
# DELETE A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
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

@app.route("/wishlists/<int:customer_id>/<int:wishlist_id>", methods=["PUT"])
def update_wishlist_name(customer_id, wishlist_id):
    """
    Updates a Wishlist name
    This endpoint will update a Wishlist name based on the data in the body
    """

    app.logger.info("Request to update a wishlist")
    check_content_type("application/json")

    wishlists = []
    app.logger.info("Request for wishlists with customer id: %s", customer_id)

    wishlists = Wishlist.find_by_customer_id(customer_id)

    if not wishlists:
        abort(status.HTTP_404_NOT_FOUND, f"Wishlist with customer id '{customer_id}' was not found.")

    results = [wishlist.serialize() for wishlist in wishlists]

    if not any(wishlist['id'] == wishlist_id for wishlist in results):
        abort(status.HTTP_404_NOT_FOUND, f"Wishlist with customer id '{customer_id}' and id '{wishlist_id}' was not found.")

    wishlist = Wishlist.find(wishlist_id)
    wishlist.name = request.get_json()["name"]
    wishlist.update()

    message = wishlist.serialize()

    return jsonify(message), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
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

