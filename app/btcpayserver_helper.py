"""
Utility functions for the btcpayserver client
"""
import pickle
from app.db import get_db
from config import Config


def get_client():
    """
    Loads the serialized client from database
    """
    db = get_db()
    pickled_client = db.execute(
        "SELECT pickled_client FROM btc_pay_server_client ORDER BY id"
    ).fetchone()
    return pickle.loads(pickled_client['pickled_client'])


def create_invoice(price=Config.TIP_AMOUNT, currency=Config.TIP_CURRENCY, order_id=None, desc=None, notification_url=None, redirect_url=None):
    """
    Creates a new invoice and returns invoice id
    :param price: a given price (default is bitcoin)
    :param currency: currency ticker from bitpay API: 'USD', 'EUR', 'BTC' etc
    :return: invoice_id -> str
    """
    client = get_client()
    try:
        new_invoice = client.create_invoice(
            {
                'price': price,
                'currency': currency,
                'orderId': order_id,
                'itemDesc': desc,
                'notificationUrl': notification_url,
                'redirectUrl': redirect_url
            }
        )
        return new_invoice['id']
    except Exception as e:
        print(e)
        return 'XXX'


def get_invoice(invoice_id: str):
    """
    Get an invoice by ID
    """
    client = get_client()
    return client.get_invoice(invoice_id)


def get_most_recent_invoice():
    """
    Returns the most return invoice created
    """
    client = get_client()
    return client.get_invoices()[:1]
