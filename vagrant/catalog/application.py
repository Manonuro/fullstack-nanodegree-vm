from flask import (
   Flask,
   render_template,
   request,
   redirect,
   url_for,
   flash,
   jsonify,
   abort,
   g
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth
from models import Base, Category, Item, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)
auth = HTTPBasicAuth()


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


# Connect to Database and create database session
engine = create_engine('sqlite:///itemCatalogwithusers.db',
    connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    #return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already'
            'connected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
        150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token'
            'for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).first()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.name})


# Provide a JSON endpoint
@app.route('/catalog.json')
def categoryItemJSON():
    categories = session.query(Category).all()
    final_list = []
    final_dict = {}
    for c in categories:
        items = session.query(Item).filter_by(
            cat_id = c.id).all()
        lst = jsonify(Items=[i.serialize for i in items])
        cat = jsonify(c.serialize)
        res = [cat, lst]

        final_dict[cat]=lst
    #return result
    #final_dict['Category'] = final_list
    return lst


# Show all Categories and Latest Items
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).order_by(Category.name.asc())
    items = session.query(Item).order_by(Item.title.asc())
    if 'username' not in login_session:
        return render_template('catalog.html',categories=categories,
            items=items)
    else:
        return render_template('catalog_loggedIn.html',categories=categories,
            items=items)


# Show Category Items
@app.route('/catalog/<string:category>/items')
def categoryItems(category):
    categories = session.query(Category).all()
    selectedCategory = session.query(Category).filter_by(name = category).first()
    items = session.query(Item).filter_by(
        category = selectedCategory).all()
    nItems = len((items))
    userId=selectedCategory.user_id
    creator = getUserInfo(userId)
    if 'username' not in login_session or creator.id!=login_session['user_id']:
        return render_template('categoryitems.html',
            categories=categories, category=selectedCategory,
            items=items, nItems=nItems)
    else:
        return render_template('categoryitems_loggedIn.html',
            categories=categories, category=selectedCategory,
            items=items, nItems=nItems, creator=creator)

# Show Item Information
@app.route('/catalog/<string:category>/<string:item>/')
def itemInformation(category,item):
    selectedCategory = session.query(Category).filter_by(
        name = category).first()
    selectedItem = session.query(Item).filter_by(title = item).first()
    creator = getUserInfo(selectedCategory.user_id)
    if 'username' not in login_session or creator.id!=login_session['user_id']:
        return render_template('categoryiteminfo.html',
            category = selectedCategory, item = selectedItem)
    else:
        return render_template('categoryiteminfo_loggedIn.html',
            category = selectedCategory, item = selectedItem, creator=creator)


# Create a new category item
@app.route('/catalog/<string:category>/add', methods=['GET', 'POST'])
def newCategoryItem(category):
    selectedCategory = session.query(Category).filter_by(
            name = category).one()
    if 'username' not in login_session:
        return redirect('/login')
    if selectedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized\
            to add Item to this category. Please make item addition to your\
            own categories.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newItem = Item(user_id=login_session['user_id'],title = request.form['title'], description = request.form['description'], cat_id=selectedCategory.id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('categoryItems', category=selectedCategory.name))
    else:
        return render_template('newcategoryitem.html',category=selectedCategory)


# Edit a new category item
@app.route('/catalog/<string:category>/<string:item>/edit',
    methods = ['GET', 'POST'])
def categoryItemEdit(category, item):
    selectedCategory = session.query(Category).filter_by(
        name = category).first()
    editedItem = session.query(Item).filter_by(
        title = item).first()
    if 'username' not in login_session:
        return redirect('/login')
    if selectedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized\
        to edit this Item. Please edit items in your own category items.');\
        }</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('itemInformation',
            category=selectedCategory.name ,
            item = editedItem.title))
    else:
        return render_template('editcategoryitem.html',
            category=selectedCategory ,
            item = editedItem)


# Delete a category item
@app.route('/catalog/<string:category>/<string:item>/delete',
    methods = ['GET', 'POST'])
def categoryItemDelete(category, item):
    selectedCategory = session.query(Category).filter_by(
        name = category).first()
    itemToDelete = session.query(Item).filter_by(
        title = item).first()
    if 'username' not in login_session:
        return redirect('/login')
    if selectedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not authorized\
        to delete Item in this category. Please make item deletion in your\
        own categories.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('categoryItems',
            category=selectedCategory.name))
    else:
        return render_template('deletecategoryitem.html',
            category=selectedCategory ,
            item = itemToDelete)

if __name__ == '__main__':
     app.secret_key = 'super_secret_key'
     app.debug = True
     app.run(host='0.0.0.0', port=8000)
