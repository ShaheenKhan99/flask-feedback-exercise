from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import CreateUserForm, LoginForm, FeedbackForm, DeleteForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abc123'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

@app.route('/')
def home_page():
    """Show home page"""

    return redirect('/register')


@app.errorhandler(404)
def page_not_found(e):
    """ Show 404 NOT FOUND page"""

    return render_template('404.html')

############################################################################### User routes

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Display register page and handle form submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        try: 
          db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken. Please pick another username")
            form.email.errors.append("This email is already being used")
            return render_template('users/register.html', form=form)

        session['username'] = user.username
        flash("Welcome! Successfully created new account", "success")
        return redirect(f"/users/{user.username}")

    return render_template('users/register.html', form=form)


@app.route('/users/<username>')
def show_user(username):
    """ Display user information for specific user if user is logged in"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()
    
    return render_template('users/user_details.html', user=user, form=form)



@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Display login page and handle form submission"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {username}", "primary")
            session['username'] = username
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Invalid username/password"]
    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout_user():
    """ Logout user and return to home page"""

    session.pop('username')
    flash("Goodbye", "info")
    return redirect('/')


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete user from database and redirect to homepage"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    flash("User has been deleted", "info")
    session.pop("username")
    return redirect('/register')

#########################################################################
# Feedback routes

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])  
def add_feedback(username):
    """Display and handle form submission for adding feedback""" 

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        flash("Feedback created successfully", "success")
        return redirect(f"/users/{feedback.username}")

    return render_template('feedback/new.html', form=form) 


@app.route('/feedback/<feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Update feedback if user created the feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        flash(f"Updated {feedback.title}")
        return redirect(f"/users/{feedback.username}")

    return render_template('feedback/edit.html', form=form, feedback=feedback)



@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")




    








