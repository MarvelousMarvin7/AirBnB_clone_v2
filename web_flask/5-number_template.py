#!/usr/bin/python3
"""starts a Flask web application:"""


from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Display Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """display HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def C_is_fun(text):
    """display “C ” followed by the value of the text variable"""
    return "C {}".format(text.replace('_', ' '))


@app.route("/python/")
@app.route("/python/<text>", strict_slashes=False)
def python_is_cool(text='is cool'):
    """display Python followed by the value of the text variable"""
    return "Python {}".format(text.replace('_', ' '))


@app.route("/number/<int:n>", strict_slashes=False)
def is_number(n):
    """display n is a number” only if n is an integer"""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def display_page(n):
    """display n is a HTML page” only if n is an integer"""
    return render_template("5-number.html", n=n)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
