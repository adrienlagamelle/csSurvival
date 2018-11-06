'''Interface for the search feature of the website using a custom
package Flask-Whooshalcemy by Miguel Grinberg
Source: github.com/miguelgrinberg/flask-whooshalchemy.git
'''

from flask import render_template, url_for, flash, redirect, request, g, session
from flask_login import current_user, login_user, logout_user, login_required
from css.app import app
from css.app.forms import (
    SearchForm,
)
from css.app import database as db

@app.route('/search', methods=['POST'])
@login_required
def search():
    '''Collect the search query from the form and redirects to search_results.html
    passing its query as an argument
    '''
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    '''Take a query string as argument from the form, and POST handler sends it
    via page redirection to the search_results handler
    The search results view function sends the query to Whoosh
    '''
    results = db.thread.search(query)
    return render_template('search_results.html', query=query, results=results)

@app.before_request
def before_request():
    ''' Create a search form object and make it available to all templates by using
    the Flask's global g
    '''
    g.user = current_user
    if current_user.is_authenticated:
        db.user.updateActivity(current_user.id)
        g.search_form = SearchForm()
