from flask import render_template, url_for, flash, redirect, request, g, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from css.app import app
from css.app.forms import (
    LoginForm,
    RegistrationForm,
    ThreadForm,
    CommentForm,
    EditProfileForm,
    CreateGroupForm,
    GroupForm,
    AddGroupMemberForm,
    SearchForm,
)
from css.app.emailer import send_email
from css.app import database as db
from css.app.search import *
from css.app.user_profile import *
from css.app.group import *

@app.route('/', methods=['GET'])
def root():
    '''Redirect user to login page if not authenticated
    Else, redirect user to the home page of the website
    '''
    if not current_user:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))

@app.route('/index', methods=['GET'])
@login_required
def index():
    ''' The home page for the website. It displays all the threads created
    by all the users, except threads created in groups
    '''
    threads = db.thread.getAll()
    session['cur_group_id'] = None
    return render_template(
        'index.html',
        title=app.config['TITLE'] + ' - Home',
        copyright=app.config['COPYRIGHT'],
        threads=threads,
        current_user=current_user,
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' The log in page for the website
    If user already authenticated, redirects to home page.
    '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.user.getFromUsername(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template(
        'login.html',
        title=app.config['TITLE'] + ' - Login',
        copyright=app.config['COPYRIGHT'],
        form=form,
    )


@app.route('/logout', methods=['GET'])
def logout():
    ''' Log out the user from the website and redirect to the
    log in page.
    '''
    logout_user()

    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' Let the user register and redirects to log in page
    If user already authenticated, redirects to home page
    '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        db.user.new(
            form.username.data,
            form.email.data,
            form.password.data,
        )
        flash('Thank you for joining ' + app.config['TITLE'] + ' .')
        return redirect(url_for('login'))

    return render_template(
        'register.html',
        title=app.config['TITLE'] + ' - Registration',
        form=form,
    )


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    ''' Let the users edit their created posts
    If user not authenticated, redirect to login page
    '''
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    thread_id = request.args.get('thread')
    group_id = session.get('cur_group_id', None)
    if group_id:
        group = db.group.get(group_id)
        group_name = group.name
    else:
        group_name = 'Frontpage'
    form = ThreadForm()
    if request.method == "GET":
        if thread_id:
            thread = db.thread.get(int(thread_id))
            form.title.data = thread.title
            form.body.data = thread.body
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        user_id = current_user.id
        group_id = group_id
        if thread_id:
            db.thread.update(
                int(thread_id),
                title=title,
                group_id=group_id,
                body=body
            )
        else:
            db.thread.new(title, body, user_id, group_id)
        if group_id is None:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('group', id=group_id))

    return render_template(
        'post.html',
        title=app.config['TITLE'] + ' - New Post',
        form=form,
        group_name=group_name,
    )


@app.route('/thread/<int:id>', methods=['GET', 'POST'])
def thread(id):
    ''' Display the requested thread

    Args:
        id (int) : the id for the thread

    Returns
        html : the thread requested
    '''
    thread = db.thread.get(id)
    group_id = thread.group_id
    session['cur_group_id'] = group_id
    if group_id != None:
        group = db.group.get(group_id)
    comments = thread.comments
    form = CommentForm()
    is_subscribed = False
    user_id = current_user.id
    thread_id = id

    sub = db.subscription.getFromMembers(user_id, thread_id)

    if group_id != None:
        if current_user not in group.members:
            flash ('You do not have access to this thread.')
            return redirect(url_for('index'))

    if sub is not None:
        is_subscribed = True

    if form.subscribe.data:
        db.subscription.new(
            user_id=user_id,
            thread_id=id,
        )
        is_subscribed = True
        return redirect(url_for('thread', id=id))

    if form.unsubscribe.data:
        db.subscription.delete(user_id, id)
        is_subscribed = False
        return redirect(url_for('thread', id=id))

    if form.validate_on_submit():
        body = form.body.data
        user_id = current_user.id
        db.comment.new(body, user_id, id)

        for sub in thread.subscribers:
            user = db.user.get(sub.user_id)
            send_email(
                user.email,
                "Thread Update",
                user.username,
                thread.title,
            )

        return redirect(url_for('thread', id=id))

    return render_template(
        'thread.html',
        current_user=current_user,
        thread=thread,
        comments=comments,
        is_subscribed=is_subscribed,
        form=form,
    )


@app.route('/deleteComment/<id>')
def deleteComment(id):
    ''' Let users delete their comments

    Args:
        id (int) : id for the comments

    Returns:
        html : display the thread
    '''
    comment = db.comment.get(id)
    if comment.user_id == current_user.id:
        db.comment.delete(id)
    return redirect(url_for('thread', id=comment.thread_id))


@app.route('/deleteThread/<id>')
def deleteThread(id):
    ''' Let users delete their thread

    Args:
        id (int) : id for the thread

    Returns:
        html : Redirect the user to the home page
    '''
    thread = db.thread.get(id)
    if thread.user_id == current_user.id:
        db.thread.delete(id)
    return redirect(url_for('index'))
