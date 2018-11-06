""" Interface for the user profile """

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

@app.route('/user/<username>')
def user(username):
    '''Create a map to the username of the logged in user

    Args:
        username (str): The username of the looged in user

    Returns:
        html : A webpage displaying the user profile and the user's
        created threads
    '''
    user = db.user.getFromUsername(username)
    threads = user.threads
    session['cur_group_id'] = None
    return render_template(
        'user.html',
        user=user,
        threads=threads
    )


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    ''' Let the logged in user change their username and
    their information

    Returns:
        html : Updated webpage of the user's profile
    '''
    form = EditProfileForm(current_user.username)
    session['cur_group_id'] = None
    if form.validate_on_submit():
        db.user.update(
            current_user.id,
            username=form.username.data,
            about=form.about.data,
            language=form.language.data,
        )
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about

    return render_template(
        'edit_profile.html',
        title='Edit Profile',
        form=form
    )
