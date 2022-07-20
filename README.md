# Wishlists

[![Build Status](https://github.com/NYU-DevOps-Summer-2022/wishlists/actions/workflows/ci.yml/badge.svg)](https://github.com/NYU-DevOps-Summer-2022/wishlists/actions)

[![codecov](https://codecov.io/gh/NYU-DevOps-Summer-2022/wishlists/branch/master/graph/badge.svg?token=ZQI6MNHOPK)](https://codecov.io/gh/NYU-DevOps-Summer-2022/wishlists)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is a skeleton you can use to start your projects

## Overview

This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples to copy from.

## Calls to the Wishlist

These are the available REST API calls which are used for Wishlist.

| Endpoint                 | Methods     | Rule                                                   |
| ------------------------ | ----------- | ------------------------------------------------------ |
| index                    | GET         | /                                                      |
| health                   | GET         | /health                                                |
| list_wishlists           | GET         | /wishlists                                             |
| create_wishlists         | POST        | /wishlists                                             |
| get_wishlists            | GET         | /wishlists/<int:wishlist_id>                           |
| update_wishlist_name     | PUT         | /wishlists/<int:wishlist_id>                           |
| delete_wishlists         | DELETE      | /wishlists/<int:wishlist_id>                           |
| clear_wishlist           | PUT         | /wishlists/<int:wishlist_id>/clear                     |
| get_wishlist_items       | GET         | /wishlists/<int:wishlist_id>/items                     |
| create_wishlist_items    | POST        | /wishlists/<int:wishlist_id>/items                     |
| get_wishlist_item        | GET         | /wishlists/<int:wishlist_id>/items/<int:item_id>       |
| update_wishlist_items    | PUT         | /wishlists/<int:wishlist_id>/items/<int:item_id>       |
| delete_wishlist_item     | DELETE      | /wishlists/<int:wishlist_id>/items/<int:item_id>       |

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── utils                  - utility package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
