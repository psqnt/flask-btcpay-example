import sqlite3
import pickle
import click
from flask import current_app, g
from flask.cli import with_appcontext
from btcpay import BTCPayClient
from werkzeug.security import generate_password_hash

"""
Contains the database and command line interface functions for the app
"""
def _create_new_client(token, url=None):
    '''
    creates new client
    this only needs to be done once, since it will be saved in the database
    get the pairing code from btc pay when you pair
    example: Server initiated pairing code: XXXXXX

    TOKENS only work once, if you get a weird http /tokens not found error,
    generate a new one and try again
    python
    >>> from btcpay import BTCPayClient
    >>> url = 'http://mynode.local:49393'
    >>> client = BTCPayClient.create_client(host=url, code=token)
    '''
    if url is None:
        url = 'http://localhost:23001'
    client = BTCPayClient.create_client(host=url, code=token)
    pickled = pickle.dumps(client)
    db = get_db()
    db.execute(
        '''INSERT INTO btc_pay_server_client (pickled_client) VALUES (?)''',
        (pickled,)
    )
    db.commit()


def close_db(e=None):
    """
    Close the connection between the application and the database
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def get_db():
    """
    Connect the application to the database.

    :return: database connection
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['SQLALCHEMY_DATABASE_URI'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    """
    Read the schema.sql file and execute it so it is 'created' in sqlite3.

    schema.sql contain sql which initializes our tables. This function
    runs that sql code (sort of). The tables in that file will now exist.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    bootstrap_data = [
        ['NGU Technology', 'Bitcoin will be 100k in June'],
        ['Speculative Attack', 'Dollars only go down, bitcoin only go up'],
        ['Lightning App', 'Lightning payments are sweet and work']
    ]
    # Boostrap the database with a some junk data posts
    for data in bootstrap_data:
        db.execute(
            'INSERT INTO post (title, body) VALUES (?, ?)', (data[0], data[1])
        )
    db.commit()


@click.command('btcpay-client')
@click.argument('token', type=click.STRING)
@click.argument('url', type=click.STRING)
@with_appcontext
def create_btc_pay_client(token, url):
    """
    creates a new btc pay server client using a token from the server
    -- only need to pair once so this should be part of initial setup
    """
    click.echo('Creating New BTCPAY Server client')
    client = _create_new_client(token, url)
    return client


@click.command('init-db')  # command line function: flask init-db
@with_appcontext
def init_db_command():
    """
    Clear existing data and create new tables.
    """
    init_db()
    click.echo('Initialized database.')


def init_app(app):
    """
    app.teardown_appcontext() tells Flask to call that function when cleaning
    up after returning the response.

    app.cli.add_command() adds a new command that can be called with the flask
    command.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_btc_pay_client)
