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



@app.route('/group/<int:id>', methods=['GET', 'POST'])
def group(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = GroupForm()
    group = db.group.get(id)
    groupName = group.name
    session['cur_group_id'] = id
    if current_user not in group.members:
        flash('You do not have access to this group.')
        return redirect(url_for('index'))
    threads = db.thread.getAll()
    if form.validate_on_submit():
        return redirect(url_for('addGroupMember', id=id))
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
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = AddGroupMemberForm()
    group_id = session.get('cur_group_id', None)
    group = db.group.get(group_id)
    group1 = db.group.get(id)
    if current_user not in group1.members:
        flash('You do not have access to this group.')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        if db.user.getFromUsername(form.username.data) in group.members:
            flash('This user is alredy in this group.')
            return redirect(url_for('group', id=group_id))
        db.group.newMember(
            group.id,
            db.user.getFromUsername(form.username.data).id,
        )
        flash('You have successfully added a new group member.')
        return redirect(url_for('group', id=group_id))
    return render_template(
        'add_new_group_member.html',
        form=form,
        username=form.username,
    )


@app.route('/createGroup', methods=['GET', 'POST'])
def createGroup():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    session['cur_group_id'] = None
    form = CreateGroupForm()
    if form.validate_on_submit():
        db.group.new(
            form.name.data,
        )
        db.group.newMember(db.group.getFromName(form.name.data).id, current_user.id)
        flash('You have successfully created a new group.')
        return redirect(url_for('index'))
    return render_template(
        'create_group.html',
        title= 'TITLE' + ' - New Group',
        form=form,
    )




@app.route('/myGroups', methods=['GET', 'POST'])
def myGroups():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    session['cur_group_id'] = None
    return render_template(
        'myGroups.html',
        group=current_user.groups,
    )
