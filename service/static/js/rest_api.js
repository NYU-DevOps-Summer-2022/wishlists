$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#wishlist_id").val(res.id);
        $("#wishlist_name").val(res.name);
        $("#wishlist_customer_id").val(res.customer_id);
    }

    // Updates the form with data from the response
    function update_item_form_data(res) {
        $("#wishlist_item_id").val(res.id);
        $("#wishlist_id").val(res.wishlist_id);
        $("#wishlist_product_id").val(res.product_id);
        $("#wishlist_product_name").val(res.product_name);
        $("#wishlist_product_price").val(res.product_price);
    }

    // Clears all form fields
    function clear_form_data() {
        $("#wishlist_name").val("");
        $("#wishlist_customer_id").val("");
    }

    // Clears all form fields
    function clear_item_form_data() {
        $("#wishlist_product_id").val("");
        $("#wishlist_product_name").val("");
        $("#wishlist_product_price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#wishlist_name").val();
        let customer_id = parseInt($("#wishlist_customer_id").val());

        let data = {
            "name": name,
            "customer_id": customer_id,
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/api/wishlists",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-item-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();
        let product_id = parseInt($("#wishlist_product_id").val());
        let product_name = $("#wishlist_product_name").val();
        let product_price = parseFloat($("#wishlist_product_price").val());

        let data = {
            "product_id": product_id,
            "product_name": product_name,
            "product_price": product_price,
        };

        $("#flash_message").empty();

        if (product_name == ""){
            flash_message("Name must be filled out");

            return false;
        }
        
        let ajax = $.ajax({
            type: "POST",
            url: `/api/wishlists/${wishlist_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Wishlist
    // ****************************************

    $("#update-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();
        let name = $("#wishlist_name").val();
        let customer_id = parseInt($("#wishlist_customer_id").val());

        let data = {
            "name": name,
            "customer_id": customer_id,
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/wishlists/${wishlist_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Update an Item
    // ****************************************

    $("#update-item-btn").click(function () {

        let item_id = $("#wishlist_item_id").val();
        let wishlist_id = $("#wishlist_id").val();
        let product_id = parseInt($("#wishlist_product_id").val());
        let product_name = $("#wishlist_product_name").val();
        let product_price = parseFloat($("#wishlist_product_price").val());

        let data = {
            "product_id": product_id,
            "product_name": product_name,
            "product_price": product_price,
        };

        $("#flash_message").empty();

        if (product_name == ""){
            flash_message("Name must be filled out");

            return false;
        }

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/wishlists/${wishlist_id}/items/${item_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message("Wishlist Not Found")
        });

    });


    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-item-btn").click(function () {

        let item_id = $("#wishlist_item_id").val();
        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/wishlists/${wishlist_id}/items/${item_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_item_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Wishlist
    // ****************************************

    $("#delete-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-item-btn").click(function () {

        let item_id = $("#wishlist_item_id").val();
        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/wishlists/${wishlist_id}/items/${item_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_item_form_data()
            flash_message("Wishlist item has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear Wishlist
    // ****************************************

    $("#clear-wishlist-btn").click(function () {
        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/api/wishlists/${wishlist_id}/clear`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_item_form_data()
            flash_message("Wishlist has been cleared")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#wishlist_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Clear the item form
    // ****************************************

    $("#clear-item-btn").click(function () {
        $("#wishlist_item_id").val("");
        $("#flash_message").empty();
        clear_item_form_data();
    });

    // ****************************************
    // Search for a wishlist
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#wishlist_name").val();
        let customer_id = $("#wishlist_customer_id").val();

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (customer_id) {
            if (queryString.length > 0) {
                queryString += '&customer_id=' + customer_id
            } else {
                queryString += 'customer_id=' + customer_id
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/wishlists?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Customer ID</th>'
            table += '</tr></thead><tbody>'
            let firstWishlist = "";

            for(let i = 0; i < res.length; i++) {
                let wishlist = res[i];
                table +=  `<tr id="row_${i}" onclick="view_item(${wishlist.id})"><td>${wishlist.id}</td><td>${wishlist.name}</td><td>${wishlist.customer_id}</td></tr>`;
                if (i == 0) {
                    firstWishlist = wishlist;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstWishlist != "") {
                update_form_data(firstWishlist)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Search for a wishlist item
    // ****************************************

    $("#search-item-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/wishlists/${wishlist_id}/items`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Wishlist ID</th>'
            table += '<th class="col-md-2">Product ID</th>'
            table += '<th class="col-md-2">Product Name</th>'
            table += '<th class="col-md-2">Product Price</th>'
            table += '</tr></thead><tbody>'
            let firstItem = "";
            for(let i = 0; i < res.length; i++) {
                let item = res[i];
                table +=  `<tr id="row_${i}"><td>${item.id}</td><td>${item.wishlist_id}</td><td>${item.product_id}</td><td>${item.product_name}</td><td>${item.product_price}</td></tr>`;
                if (i == 0) {
                    firstItem = item;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstItem != "") {
                update_item_form_data(firstItem)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
