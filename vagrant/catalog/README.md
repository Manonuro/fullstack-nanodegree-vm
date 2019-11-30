# Item Catalog Project

The web application provides a list of items within a variety of categories and integrates third party user registration and authentication. Authenticated users should have the ability to post, edit, and delete their own items.




## Getting Started

Before we begin coding, there are several steps that you should take to make sure that you have everything downloaded in order to run your future web application.	



### The virtual machine Installation
Install Vagrant and VirtualBox if you have not done so already. Instructions on how to do so can be found on the websites as well as [this website](https://www.udacity.com/wiki/ud088/vagrant).

You will need to install two pieces of software:
- VirtualBox, which you can get from [this download page](https://www.virtualbox.org/wiki/Downloads).
- Vagrant, which you can get from [this download page](https://www.vagrantup.com/downloads.html).

You will also need a Unix-style terminal program. On Mac or Linux systems, you can use the built-in Terminal. On Windows, we recommend Git Bash, which is installed with the Git version control software.

### Clone the fullstack-nanodegree-vm repository
There is a catalog folder provided [here](https://www.google.com/url?q=http://github.com/udacity/fullstack-nanodegree-vm&sa=D&ust=1572660516735000), but no files have been included. If a catalog folder does not exist, simply create your own inside of the vagrant folder.


### Launch the Vagrant VM 
Launch the Vagrant VM (by typing vagrant up in the directory fullstack/vagrant from the terminal). You can find further instructions on how to do so [here](https://www.google.com/url?q=https://www.udacity.com/wiki/ud088/vagrant&sa=D&ust=1572660516736000).



### Required Libraries and dependencies:

This project is written and executed in folloing environment:
- Python 3.5.2
- Flask 1.1.1
- Werkzeug 0.16.0

Following Libraris are imported for this project:

- import os
- import sys
- import random
- import string
- import httplib2
- import requests
- import json

- from sqlalchemy import Column, ForeignKey, Integer, String
- from sqlalchemy.ext.declarative import declarative_base
- from sqlalchemy.orm import relationship, sessionmaker
- from sqlalchemy import create_engine
- from sqlalchemy.ext.declarative import declarative_base
- from sqlalchemy import create_engine
- from sqlalchemy.orm import relationship, sessionmaker
- from sqlalchemy import create_engine

- from flask import session as login_session
- from flask_httpauth import HTTPBasicAuth
- from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, g
- from flask import make_response

- from werkzeug.security import generate_password_hash, check_password_hash

- from passlib.apps import custom_app_context as pwd_context

- from models import Base, Category, Item, User


 
 Python Files:
 
 ( * .py, static, template folder)


Introduction : This includes
What your application is all about
Required Libraries and dependencies (Version of Flask, Python, and SQLAlchemy)

Templates (HTML files used)
Installation Instructions : This includes
Google and/or Facebook OAuth service setup,
The use of requirements.txt to install your own dependencies used (if any needed)
Operating Instructions, This includes:
How to run the database setup,
How to populate the database,
How to run your application




## Project Components:

#### Python files:
-	The **`application.py`** file includes the Flask application methods to put this API online. it includes authentication/authorization to allow users to login before making changes to the catalog contents. After logging in, a user has the ability to add, update, or delete item information. Users are able to modify only those items that they themselves have created.  
-	The **`models.py`** file to setup the database components for this API.
-	The **`lotsOfCategorieswithusers.py`** creats the initial database of the users, categories, and their items.

#### templates directory:
This directory contains the HTML structure of the pages as follows:


-	The **`catalog.html`** is the homepage that displays all current categories with the latest added items to all users.
-	The **`catalog_loggedIn.html`** same as **`catalog.html`** but only for logged-in users.
-	The **`categoryitems_loggedIn.html`** Shows the items listed for the selected category in the catalog for all users. It also shows the **Add Item** option to the logged-in user to add new item to each category.
-	The **`categoryitems_loggedIn.html`** same as **`categoryitems.html`**, but only for logged-in users.
-	The **`categoryiteminfo.html`** Selecting a specific category shows all the items available for that category for all users.
-	The **`categoryiteminfo_loggedIn.html`** same as **`categoryiteminfo.html`**, but only for logged-in users. It also gives the **Delete** and **Edit** options of the item to the logged-in user. 
-	The **`editcategoryitem.html`** page will aloow the logged-in user to modify the information of the item.
-	The **`deletecategoryitem.html`** page will aloow the logged-in user to delete the selected item from category. It will ask for confirmation before deleting the item.
-	The **`newcategoryitem.html`** page will aloow the logged-in user to add a new item to the selected category. 
-	The **`login.html`** page shows the Google API login button and runs it t authenticate the user with OAuth2 method.
-	The **`main.html`** file contains the links to **`styles.css`** and **`bootstrap.min.css`** files and block container to be used for all pages. It prevents us from repeating same HTML header for each pages.
-	The **`header.html`** file is like **`main.html`**  and is being used in all public pages. It shows **`Login`** button in the top of each page.
-	The **`header_loggedIn.html`** file is like **`header.html`** but for the looged-in pages. It shows **`Logout`** button in the top of each page. 


#### static directory:
This Directory contains the **`styles.css`** file which is a CSS file that determines the style of the pages.


#### The Database
It contains the following components:

-   Users
-   Categories
-   Category Items

The **`itemCatalogwithusers.db`** contains the authorised user information, categories created by each user, and the items of each category in the catalog. Each item has its description togetehr with the user ID of its creator. The user ID is part of the category information and is the same as the one for each item under it. 

#### client_secrets.json

The **`client_secrets.json`** file is a JSON formatted style that stores the client ID, client secret and other OAuth 2.0 parameters. 



## Run the application
Run your application within the VM by typing python /vagrant/catalog/application.py into the Terminal. If you named the file from step 4 as something other than application.py, in the above command substitute in the file name on your computer.

Access and test your application by visiting http://localhost:8000 locally on your browser.
The use of requirements.txt to install your own dependencies used (if any needed)

#### Run the database setup:
By running the **`models.py`** file following components of the database will be setup with SQLalchemy:
- User
- Category
- Item
Then by importing it to the application.py, we can add, edit, or modify the datbase by utilizing it.

#### Populate the database:
By running the **`lotsOfCategorieswithusers.py`** file, it will populate the initial database that contains several catgeroies and their items for two users.

#### Run application:
Finaly by running the **`application.py`** file it will automatically be synced to /vagrant/catalog within the VM and we can access and test the application by visiting http://localhost:8000 locally on the browser which shows the main public catalog page with all categories and latest added items for each category.



## Authors

* **Manouchehr Bagheri** - *Initial work* - [Manonuro](https://github.com/Manonuro)
