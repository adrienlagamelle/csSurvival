"""Creation of discussion groups (selected users) and optional
restriction of topics to created groups

Internal to the group project

A user can create a group when they are authenticated. After
creating a group, they can hit My Group button to access the
groups they are in. By entering one of the group page, the user
can post threads in the group page which can only be viewed by
members in this group. Any group members in one group can add new
group member to the group by entering the user names, a non-existed
user name or an user who is already in the group cannot be added in
the group.

Construct group module, CreateGroupForm Object, AddGroupMemberForm Object
, and GroupForm Object in form.py and modify methods in route.py, then
create group, editing group threads, and create new group members will be
done.

Classes:
    CreateGroupForm - return creating new group,exception when group name
    already exists
    AddGroupMemberForm - return adding new group member to one group,
    exception when user name does not exist
    GroupForm - return to add group member page

Functions:
    group(id) - display threads under one group and add group member option,
    exception when user is not in the group
    addGroupMember(id) - add new member to one group, excption when the user is
    already in the group
    createGroup - create new group
    myGroup - display groups an user is currently in

"""
#group.py

from flask import render_template, url_for, flash, redirect, request, g, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import (
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
from app.email import send_email
import app.database as db

__all__ - ["group", "addGroupMember", "createGroup", "myGroups"]

@app.route('/group/<int:id>', methods=['GET', 'POST'])
def group(id):
    """Display threads under one group and add group member option

    Args:
        id: Id - the current group id of the group page

    Return:
        template 'group.html' - the html file that displays threads
        have relation to the group
        error - when the user is not in the group
    This invocation is also responsible for getting current group id for
    current page(session) for posting and add group member
    """
    return render_template(
        'group.html',
        form=form,
        threads=threads,
        current_user=current_user,
        id=id,
        groupName=groupName,
    )

@app.route('/addGroupMember/<id>', methods=['GET', 'POST'])
def addGroupMember(id):
    """Add new group member to the group

    Args:
        id: Id - the current group id of the group page

    Return:
        template 'add_new_group_member.html' - the html file that direct
        users to add new member
        error - when the entered username is already in the group
        error - when enter a add group member page that the user is not in
    """
    return render_template(
        'add_new_group_member.html',
        form=form,
        username=form.username,
    )

@app.route('/createGroup', methods=['GET', 'POST'])
def createGroup():
    """Create a new group
    Args:
        None
    Return:
        template 'create_group.html' - the html file that direct users to
        create new group
    This invocation is also responsible for getting current group id for
    current page(session) for posting and add group member
    """
    return render_template(
        'create_group.html',
        title= 'TITLE' + ' - New Group',
        form=form,
    )

@app.route('/myGroups', methods=['GET', 'POST'])
def myGroups():
    """Display all the groups the current user is in
    Args:
        None
    Return:
        template 'myGroups.html' - the html file that displays all the groups
        the user is in
    This invocation is also responsible for getting current group id for
    current page(session) for posting and add group member
    """
    return render_template(
        'myGroups.html',
        group=current_user.groups,
    )

#forms.py

from flask_wtf import FlaskForm
from flask_login import current_user
from app.language import Language
import app.database as db
from wtforms import (
    StringField,
    PasswordField,
    TextField,
    TextAreaField,
    BooleanField,
    SubmitField,
    SelectField,
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
    Length,
)

__all__ = ["CreateGroupForm", "AddGroupMemberForm", "GroupForm"]

class CreateGroupForm(FlaskForm):
    """Submit to create groups
    Attributes:
        name: StringField - the group name to be created in the database
        submit: SubmitField - the function of submiting creation request to the
        database
    Examples:
        An user clicks the New Group button, enters the group name in the string
        field, and then clicks submit.
        <code>
            name = StringField(Language()["New group name"],validators=[DataRequired()])
            = 2005Group
            submit = SubmitField(Language()["Submit"])
        </code>
        An user clickss the New Group button, enters the group name in the string
        filed, and then clicks submit, however the group name already exists.
        <code>
            name = StringField(Language()["New group name"], validators=[DataRequired()])
            = "2005Group"
            submit = SubmitField(Language()["Submit"])
            def validate_name(self, name):
                groupName = db.group.getFromName(2005Group)
                if groupName is not None:
                raise ValidationError(
                    Language()["groupExistError"]
                    )
        """
class AddGroupMemberForm(FlaskForm):
    """Submit to add new group member to the group
    Attributes:
        username: StringField - the user name to be added into the group
        submit: SubmitField - the function of submiting addting of new group
        members request to the database
    Examples:
        An user enters user name in the string field and then clicks submit.
        <code>
            username = StringField(Language()["Username"], validators=[DataRequired()])
            = groupmember2
            submit = SubmitField(Language()["Submit"])
        </code>
        An user enters user name in the string field and then clicks submit. However,
        the username does no exist.
        <code>
            username = StringField(Language()["Username"], validators=[DataRequired()])
            = Tom
            submit = SubmitField(Language()["Submit"])
            def validate_username(self, username):
            user = db.user.getFromUsername("Tom")
            if user == None:
                raise ValidationError(
                    Language()["userNonExistantError"]
                    )
    """

class GroupForm(FlaskForm):
    """Get into add new group member page
    Attributes:
        submit: SubmitField - the function of submiting the request to return
        to the add new group member page
    """
