#!/usr/bin/python3
"""starts a Flask web application"""

from flask import Flask, render_template
from models.state import State
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def close_db(exc):
    """remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/states_list')
def states_list():
    """ display a HTML page: (inside the tag BODY)"""
    states = storage.all(Stat).values()
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
