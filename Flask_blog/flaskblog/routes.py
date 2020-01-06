from flask import render_template, url_for, flash, redirect, request, render_template_string
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdateAccountFormURL
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
import urllib.request


posts = [
    {
        'author': 'Son Beo 1',
        'title': 'Blog Post 1',
        'content': 'First post',
        'date_posted': 'December 25, 2019'
    },
    {
        'author': 'Son Beo 2',
        'title': 'Blog Post 2',
        'content': 'Second post',
        'date_posted': 'December 25, 2019'
    }
]


@app.route("/page")
def page():
    exploit = request.args.get('exploit')
    print ('exploit')
    rendered_template = render_template("app.html", exploit=exploit)
    print(rendered_template)
    return render_template_string(rendered_template)
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created ! Able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/image_file', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


def save_picture_url(url, file_path):
    file_name = secrets.token_hex(8)
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)
    return file_name


@app.route('/accounturl', methods=['GET', 'POST'])
@login_required
def accounturl():
    form = UpdateAccountFormURL()
    if form.validate_on_submit():
        if form.url.data:
            picture_file = save_picture_url(form.url.data,'flaskblog/static/image_file/')
            current_user.image_file = picture_file + '.jpg'
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('accounturl'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='image_file/' + current_user.image_file )
    return render_template('accounturl.html', title='AccountURL', image_file=image_file, form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='image_file/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
