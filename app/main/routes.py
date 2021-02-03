import random
from app.db import get_db
from app.main import bp
from flask import request, redirect, url_for, render_template
from app.btcpayserver_helper import create_invoice


@bp.route('/create', methods=('GET', 'POST'))
def create():
    """
    Creates a new post -- like a blog or something
    """
    # if POST
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.execute(
                'INSERT INTO post (title, body) VALUES (?, ?)', (title, body)
            )
            db.commit()
            # get the id of the post that was just added to db
            return redirect(url_for('main.lightning_app'))

    # if GET
    return render_template('main/create.html')


@bp.route('/')
@bp.route('/lightning-app')
def lightning_app():
    """
    Redirect to random post on lightning invoice payment
    This function generates lightning invoice using the btcpay client 
    to connect to the btcpayserver instance
    """
    # get all available ids from post table and select random one
    db = get_db()
    ids = [id[0] for id in db.execute('SELECT id from post').fetchall()]
    random_post = random.choice(ids)
    btc_pay_invoice_id = create_invoice()
    url_for_post = url_for('main.view_post', post_id=random_post)
    return render_template(
        'main/lightning.html',
        invoice_id=btc_pay_invoice_id,
        redirect=url_for_post
    )


@bp.route('/post/<int:post_id>', methods=('GET',))
def view_post(post_id):
    """
    Generate the view post page.

    GET: This is retrieving a specific post

    :param post_id: id of specific post
    :return render_template
    """
    post = get_db().execute(
        'SELECT title, body FROM post WHERE id = ?', (post_id,)
    ).fetchone()
    btc_pay_invoice_id = create_invoice()
    return render_template(
        'main/post.html',
        post=post,
        invoice_id=btc_pay_invoice_id
    )
