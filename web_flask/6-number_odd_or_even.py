#!/usr/bin/python3
"""
Starts a Flask web application:
listening on 0.0.0.0, port 5000
Routes: /: display “Hello HBNB!”

"""
from markupsafe import escape
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """
    Display Hello HBNB!
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Display HBNB
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """
    Display C is ...
    """
    return f'C {escape(text).replace("_", " ")}'


@app.route("/python/", defaults={'text': "is_cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is cool"):
    """
    Display Python is ...
    """
    return f'Python {escape(text).replace("_", " ")}'


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    """
    Display n is a number if n is int
    """
    if type(n) is int:
        return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n=None):
    """
    Display a HTML page only if n is an integer:
    """
    if isinstance(n, int):
        return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n=None):
    """
    Display a HTML page only if n is an integer:
    """
    if isinstance(n, int) and n % 2 == 0:
        return render_template('6-number_odd_or_even.html', n=n, txt="even")
    elif isinstance(n, int) and n % 2 != 0:
        return render_template('6-number_odd_or_even.html', n=n, txt="odd")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
