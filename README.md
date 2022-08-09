# Wishlists

[![Build Status](https://github.com/NYU-DevOps-Summer-2022/wishlists/actions/workflows/ci.yml/badge.svg)](https://github.com/NYU-DevOps-Summer-2022/wishlists/actions)
[![codecov](https://codecov.io/gh/NYU-DevOps-Summer-2022/wishlists/branch/master/graph/badge.svg?token=ZQI6MNHOPK)](https://codecov.io/gh/NYU-DevOps-Summer-2022/wishlists)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

## Overview

In this project, we have created a wishlist resource as a part of an e-commerce website for the final project of the DevOps class at NYU taught by Professor John Rofrano for the Summer of 2022. We utilized the base code provided in https://github.com/nyu-devops/ across the various repositories. The members of the project are:

Aashiq Mohamed baig, Anugya Shah, MD Shahedur Rahman, Namratha Vempaty Neeraj Kanuri

To run the all the test cases locally, please use the command "nosetests". 

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
.
├── Dockerfile
├── LICENSE
├── Makefile
├── Procfile
├── README.md
├── __pycache__
│   └── config.cpython-39.pyc
├── config.py
├── coverage.xml
├── deploy
│   ├── dev-deployment.yaml
│   ├── dev-postgresql.yaml
│   ├── dev-service.yaml
│   ├── dev.yaml
│   ├── prod-deployment.yaml
│   ├── prod-postgresql.yaml
│   ├── prod-service.yaml
│   └── prod.yaml
├── dot-env-example
├── features
│   ├── environment.py
│   ├── steps
│   │   ├── web_steps.py
│   │   └── wishlists_steps.py
│   └── wishlists.feature
├── requirements.txt
├── service
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── models.cpython-39.pyc
│   │   └── routes.cpython-39.pyc
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   ├── css
│   │   │   ├── blue_bootstrap.min.css
│   │   │   ├── cerulean_bootstrap.min.css
│   │   │   ├── darkly_bootstrap.min.css
│   │   │   ├── flatly_bootstrap.min.css
│   │   │   └── slate_bootstrap.min.css
│   │   ├── images
│   │   │   └── newapp-icon.png
│   │   ├── index.html
│   │   └── js
│   │       ├── bootstrap.min.js
│   │       ├── jquery-3.6.0.min.js
│   │       └── rest_api.js
│   └── utils
│       ├── __pycache__
│       │   ├── cli_commands.cpython-39.pyc
│       │   ├── error_handlers.cpython-39.pyc
│       │   ├── log_handlers.cpython-39.pyc
│       │   └── status.cpython-39.pyc
│       ├── cli_commands.py
│       ├── error_handlers.py
│       ├── log_handlers.py
│       └── status.py
├── setup.cfg
└── tests
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-39.pyc
    │   ├── factories.cpython-39.pyc
    │   ├── test_cli_commands.cpython-39.pyc
    │   ├── test_models.cpython-39.pyc
    │   └── test_routes.cpython-39.pyc
    ├── factories.py
    ├── test_cli_commands.py
    ├── test_models.py
    └── test_routes.py
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.