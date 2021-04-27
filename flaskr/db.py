import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# g:
# special object (unique) for each request. To store data that might be accessed by multiple functs during the request.
# The conn is stored and reused instead of creating a new conn if get_db is called a second time in the same request.

# current_app:
# is another special object that points to the Flask application handling the request.
# Since you used an application factory, there is no application object when writing the rest of your code.
# get_db will be called when the application has been created and is handling a request, so current_app can be used.

# open_resource()
# opens a file relative to the flaskr package, which is useful since you won’t necessarily know where that location is
# when deploying the application later.
# get_db returns a database connection, which is used to execute the commands read from the file.

#
# Register with the Application:

# app.teardown_appcontext()
# tells Flask to call that function when cleaning up after returning the response.

# app.cli.add_command()
# adds a new command that can be called with the flask command.

# Run the init-db command:
# $ flask init-db
