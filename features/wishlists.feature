Feature: The wishlists service back-end
    As a the manager of an E-Commerce website
    I need a RESTful wishlists service
    So that my customers can keep track of their wishlist items

Background:
    Given the following wishlists
        | name       | customer_id |
        | winter     | 1           |
        | summer     | 2           |
        | spring     | 5           |
        | fall       | 5           |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlists RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Wishlist
    When I visit the "Home Page"
    And I set the "Name" to "dev-summer"
    And I set the "Customer ID" to "34"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Customer ID" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "dev-summer" in the "Name" field
    And I should see "34" in the "Customer ID" field

Scenario: List all wishlists
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "winter" in the results
    And I should see "summer" in the results
    And I should see "spring" in the results
    And I should see "fall" in the results
    And I should not see "monsoon" in the results

Scenario: Search by customer_id
    When I visit the "Home Page"
    And I set the "Customer ID" to "5"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "spring" in the results
    And I should see "fall" in the results
    And I should not see "winter" in the results
    And I should not see "summer" in the results

Scenario: Search by wishlist name
    When I visit the "Home Page"
    And I set the "Name" to "summer"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "summer" in the results
    And I should not see "fall" in the results
    And I should not see "winter" in the results
    And I should not see "spring" in the results

Scenario: Update a Wishlist
    When I visit the "Home Page"
    And I set the "Name" to "summer"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "summer" in the "Name" field
    And I should see "2" in the "Customer ID" field
    When I change "Name" to "monsoon"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "monsoon" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "monsoon" in the results
    And I should not see "summer" in the results

Scenario: Delete a Wishlist
    When I visit the "Home Page"
    And I set the "Name" to "summer"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "summer" in the "Name" field
    When I copy the "Id" field
    And I press the "Delete" button
    Then I should see the message "Wishlist has been Deleted!"
    When I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Wishlist Not Found"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should not see "summer" in the results


Scenario: Create a Wishlist Item
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I click row "0"
    And I set the "Product ID" to "425"
    And I set the "Product Name" to "phone"
    And I set the "Product Price" to "500.45"
    And I press the "Create Item" button
    Then I should see the message "Success"
    When I copy the "Item ID" field
    And I press the "Clear Item" button
    Then the "Item ID" field should be empty
    And the wishlist ID should be accurate
    And the "Product ID" field should be empty
    And the "Product Name" field should be empty
    And the "Product Price" field should be empty
    When I paste the "Item ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "425" in the "Product ID" field
    And I should see "phone" in the "Product Name" field
    And I should see "500.45" in the "Product Price" field
    And the wishlist ID should be accurate
    And close the tab

Scenario: List Wishlist items
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I click row "0"
    And I set the "Product ID" to "425"
    And I set the "Product Name" to "apple"
    And I set the "Product Price" to "24"
    And I press the "Create Item" button
    Then I should see the message "Success"
    When I press the "Clear Item" button
    And I set the "Product ID" to "589"
    And I set the "Product Name" to "phone"
    And I set the "Product Price" to "500.45"
    And I press the "Create Item" button
    Then I should see the message "Success"
    When I copy the "Item ID" field
    And I press the "Clear Item" button
    Then the "Item ID" field should be empty
    And the wishlist ID should be accurate
    And the "Product ID" field should be empty
    And the "Product Name" field should be empty
    And the "Product Price" field should be empty
    When I paste the "Item ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "589" in the "Product ID" field
    And I should see "phone" in the "Product Name" field
    And I should see "500.45" in the "Product Price" field
    And the wishlist ID should be accurate
    When I press the "Search Item" button
    Then I should see the message "Success"
    And I should see "425" in the results
    And I should see "589" in the results
    And I should see "phone" in the results
    And I should see "apple" in the results
    And I should see "24" in the results
    And I should see "500.45" in the results
    And I should not see "426" in the results
    And I should not see "car" in the results
    And the wishlist ID should be accurate
    And close the tab

Scenario: Update a Wishlist Item
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I click row "0"
    And I set the "Product ID" to "425"
    And I set the "Product Name" to "phone"
    And I set the "Product Price" to "500.45"
    And I press the "Create Item" button
    Then I should see the message "Success"
    When I copy the "Item ID" field
    And I press the "Clear Item" button
    Then the "Item ID" field should be empty
    And the wishlist ID should be accurate
    And the "Product ID" field should be empty
    When I paste the "Item ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "425" in the "Product ID" field
    And I should see "phone" in the "Product Name" field
    And I should see "500.45" in the "Product Price" field
    And the wishlist ID should be accurate
    When I set the "Product ID" to "426"
    And I press the "Update Item" button
    Then I should see the message "Success"
    When I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "426" in the "Product ID" field
    And I should see "phone" in the "Product Name" field
    And I should see "500.45" in the "Product Price" field
    And the wishlist ID should be accurate
    And close the tab

Scenario: Delete Wishlist item
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I click row "0"
    And I set the "Product ID" to "425"
    And I set the "Product Name" to "apple"
    And I set the "Product Price" to "24"
    And I press the "Create Item" button
    Then I should see the message "Success"
    When I press the "Clear Item" button
    And I set the "Product ID" to "589"
    And I set the "Product Name" to "phone"
    And I set the "Product Price" to "500.45"
    And I press the "Create Item" button
    Then I should see the message "Success"
    When I copy the "Item ID" field
    And I press the "Clear Item" button
    Then the "Item ID" field should be empty
    And the wishlist ID should be accurate
    And the "Product ID" field should be empty
    When I paste the "Item ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "589" in the "Product ID" field
    And the wishlist ID should be accurate
    When I press the "Search Item" button
    Then I should see the message "Success"
    And I should see "425" in the results
    And I should see "589" in the results
    And I should not see "426" in the results
    And the wishlist ID should be accurate
    When I press the "Delete Item" button
    Then I should see the message "Wishlist item has been Deleted!"
    Then the wishlist ID should be accurate
    When I press the "Search Item" button
    Then I should see the message "Success"
    And I should not see "426" in the results
    And I should not see "425" in the results
    And I should see "589" in the results
    And I should see "phone" in the results
    And I should not see "apple" in the results
    And I should not see "24" in the results
    And I should see "500.45" in the results
    And I should not see "426" in the results
    And I should not see "car" in the results
    And close the tab

Scenario: Clear Wishlist
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    When I click row "0"
    And I set the "Product ID" to "425"
    And I set the "Product Name" to "apple"
    And I set the "Product Price" to "24"
    And I press the "Create Item" button
    Then I should see the message "Success"
    When I press the "Clear Item" button
    And I set the "Product ID" to "589"
    And I set the "Product Name" to "phone"
    And I set the "Product Price" to "500.45"
    And I press the "Create Item" button
    Then I should see the message "Success"
    When I copy the "Item ID" field
    And I press the "Clear Item" button
    Then the "Item ID" field should be empty
    And the wishlist ID should be accurate
    And the "Product ID" field should be empty
    When I paste the "Item ID" field
    And I press the "Retrieve Item" button
    Then I should see the message "Success"
    And I should see "589" in the "Product ID" field
    And the wishlist ID should be accurate
    When I press the "Search Item" button
    Then I should see the message "Success"
    And I should see "425" in the results
    And I should see "589" in the results
    And I should not see "426" in the results
    And the wishlist ID should be accurate
    When I press the "Clear Wishlist" button
    Then I should see the message "Wishlist has been cleared"
    Then the wishlist ID should be accurate
    When I press the "Search Item" button
    Then I should see the message "Success"
    And I should not see "426" in the results
    And I should not see "425" in the results
    And I should not see "589" in the results
    And I should not see "phone" in the results
    And I should not see "apple" in the results
    And I should not see "24" in the results
    And I should not see "500.45" in the results
    And I should not see "426" in the results
    And I should not see "car" in the results
    And close the tab
