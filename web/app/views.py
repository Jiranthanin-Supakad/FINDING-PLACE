import os
from flask import (jsonify, render_template,
                   request, url_for, flash, redirect)
import secrets
import string
#import json
from werkzeug.utils import secure_filename

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user, current_user

from app import oauth
from app import app
from app import db
from app import login_manager

from app.models.boxpost import FindBlog
# from app.models.contact import Contact
# from app.models.contactBlog import BlogEntry
from app.models.authuser import AuthUser, PrivateBoxpost

# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our
#     # user table, use it in the query for the user
#     return AuthUser.query.get(int(user_id))

#UPLOAD_FOLDER = '/web/app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return AuthUser.query.get(int(user_id))

def read_file(filename, mode="rt"):
    with open(filename, mode, encoding='utf-8') as fin:
        return fin.read()

@app.route('/')
def home():
    return "Flask says 'Hello world!'"

@app.route('/crash')
def crash():
    return 1/0

@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)

@app.route('/finding')
def finding_main():
    return render_template('main_page.html')
    
@app.route('/finding_discovery', methods=('GET', 'POST'))
def finding_discovery():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')
        validated = True
        validated_dict = dict()
        valid_keys = ['name', 'email','category','idPet','subdist','district','province', 'detail', 'tel', 'filenameIMG']
        
        if request.form["submit"] == 'Upload':
            id_file = result.get('id', '')
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(hash(filename)) + "." +str(filename.rsplit('.', 1)[1].lower())
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return redirect(request.url)
                
            # validate the input
        for key in result:
            app.logger.debug(key, result[key])
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
            #return f'Upload: {id_}'
            if key == 'filenameIMG':
                validated_dict[key] = filename if file else None
        
        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            # if there is no id_: create blog
            if not id_:
                validated_dict['owner_id'] = current_user.id
                #entry = FindBlog(**validated_dict)
                entry = PrivateBoxpost(**validated_dict)
                app.logger.debug(str(entry))
                db.session.add(entry)
                #db.session.add(upload)
            # if there is an id already: update the blog entry
            else:
                #blog = FindBlog.query.get(id_)
                blog = PrivateBoxpost.query.get(id_)
                if blog.owner_id == current_user.id:
                    blog.update(**validated_dict)
            
            db.session.commit()

        #return finding_db_blog()
    return render_template('navbar_mainpage/search_app.html')

@app.route('/finding_update', methods=('GET', 'POST'))
def finding_update():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')
        validated = True
        validated_dict = dict()
        valid_keys = ['name', 'email','category','idPet','subdist','district','province', 'detail', 'tel', 'filenameIMG']
        
        if request.form["submit"] == 'Upload':
            id_file = result.get('id', '')
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(hash(filename)) + "." +str(filename.rsplit('.', 1)[1].lower())
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return redirect(request.url)

            # validate the input
        for key in result:
            app.logger.debug(key, result[key])
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
            #return f'Upload: {id_}'
            if key == 'filenameIMG':
                validated_dict[key] = filename if file else None
        
        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            # if there is no id_: create blog
            if not id_:
                validated_dict['owner_id'] = current_user.id
                #entry = FindBlog(**validated_dict)
                entry = PrivateBoxpost(**validated_dict)
                app.logger.debug(str(entry))
                db.session.add(entry)
                #db.session.add(upload)
            # if there is an id already: update the blog entry
            else:
                #blog = FindBlog.query.get(id_)
                blog = PrivateBoxpost.query.get(id_)
                if blog.owner_id == current_user.id:
                    blog.update(**validated_dict)
            
            db.session.commit()

        #return finding_db_blog()
    return render_template('navbar_mainpage/update.html')

@app.route('/finding/blog')
def finding_db_blog():
    blog = []
    db_blog = PrivateBoxpost.query.all()
    #db_blog = FindBlog.query.all()
    blog = list(map(lambda x: x.to_dict(), db_blog))
    app.logger.debug("DB blog: " + str(blog))
    return jsonify(blog)

@app.route('/finding/remove_blog', methods=('GET', 'POST'))
@login_required
def remove_blog():
    app.logger.debug("Finding- REMOVE")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            #blog = FindBlog.query.get(id_)
            blog = PrivateBoxpost.query.get(id_)
            if blog.owner_id == current_user.id:
                db.session.delete(blog)
                db.session.commit()
        except Exception as ex:
            app.logger.debug(ex)
            raise
    return finding_db_blog()

@app.route('/homepage')
def homepage_home():
    return render_template('homepage/home.html')

@app.route('/homepage/index')
def homepage_index():
    return render_template('homepage/index.html')

@app.route('/homepage/login', methods=('GET', 'POST'))
def homepage_login():
    if request.method == 'POST':
        # login code goes here
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        user = AuthUser.query.filter_by(email=email).first()
 
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the
        # hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('homepage_login'))

        # if the above check passes, then we know the user has the right
        # credentials
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('finding_main')
        return redirect(next_page)
    return render_template('homepage/login.html')

@app.route('/homepage/signup', methods=('GET', 'POST'))
def homepage_signup():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
 
        validated = True
        validated_dict = {}
        valid_keys = ['email', 'name', 'password']

        # validate the input
        for key in result:
            app.logger.debug(str(key)+": " + str(result[key]))
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
            # code to validate and add user to database goes here
        app.logger.debug("validation done")
        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            email = validated_dict['email']
            name = validated_dict['name']
            password = validated_dict['password']
            # if this returns a user, then the email already exists in database
            user = AuthUser.query.filter_by(email=email).first()
            username = AuthUser.query.filter_by(name=name).first()

            if user:
                # if a user is found, we want to redirect back to signup
                # page so user can try again
                flash('Email address already exists')
                return redirect(url_for('homepage_signup'))
            
            if username:
                # if a user is found, we want to redirect back to signup
                # page so user can try again
                flash('Name already exists')
                return redirect(url_for('homepage_signup'))


            # create a new user with the form data. Hash the password so
            # the plaintext version isn't saved.
            app.logger.debug("preparing to add")
            avatar_url = gen_avatar_url(email, name)
            new_user = AuthUser(email=email, name=name,
                                password=generate_password_hash(
                                    password, method='sha256'),
                                avatar_url=avatar_url)
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('homepage_login'))
    return render_template('homepage/signup.html')

def gen_avatar_url(email, name):
    bgcolor = generate_password_hash(email, method='sha256')[-6:]
    color = hex(int('0xffffff', 0) -
                int('0x'+bgcolor, 0)).replace('0x', '')
    lname = ''
    temp = name.split()
    fname = temp[0][0]
    if len(temp) > 1:
        lname = temp[1][0]

    avatar_url = "https://ui-avatars.com/api/?name=" + \
        fname + "+" + lname + "&background=" + \
        bgcolor + "&color=" + color
    return avatar_url

@app.route('/homepage/profile')
@login_required
def homepage_profile():
    return render_template('homepage/profile.html')

@app.route('/homepage/logout')
@login_required
def homepage_logout():
    logout_user()
    return redirect(url_for('finding_main'))

@app.route('/users')
def get_all_user():
    users = AuthUser.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'avatar_url': user.avatar_url
        })
    return jsonify(user_list)

@app.route('/google/')
def google():
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

   # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    app.logger.debug(str(token))

    userinfo = token['userinfo']
    app.logger.debug(" Google User " + str(userinfo))
    email = userinfo['email']
    user = AuthUser.query.filter_by(email=email).first()

    if not user:
        name = userinfo['given_name']
        if 'family_name' in userinfo:
            name += " " + userinfo['family_name']
        random_pass_len = 8
        password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                      for i in range(random_pass_len))
        picture = userinfo['picture']
        new_user = AuthUser(email=email, name=name,
                       password=generate_password_hash(
                           password, method='sha256'),
                       avatar_url=picture)
        db.session.add(new_user)
        db.session.commit()
        user = AuthUser.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/finding_discovery')

@app.route('/finding/user')
def db_user():
    contact = []
    db_blog = AuthUser.query.all()
    contact = list(map(lambda x: x.to_dict(), db_blog))
    return jsonify(contact)