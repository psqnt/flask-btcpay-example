import os
from os.path import expanduser


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    HOME = expanduser("~")
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        os.path.join(BASEDIR, 'instance/app.sqlite')
    )
    STATIC_FOLDER=os.path.join(BASEDIR, 'app/static')
    UPLOAD_FOLDER=os.path.join(BASEDIR, 'app/static/images')
    INVOICE_DIR=os.path.join(BASEDIR, 'app/static/invoices')
    SECRET_KEY=os.environ.get('SECRET_KEY')
    DEBUG=os.environ.get('DEBUG') or False
    ADMINS=os.environ.get('ADMIN_EMAIL_ADDRESS_LIST')
    FLASK_PORT=5000
    # Tor
    FLASK_TOR=os.environ.get('FLASK_TOR') or False
    TOR_FOLDER=os.path.join(BASEDIR, '.tor/keys.txt')
    TOR_PORT=80
    # BTCPAYSERVER
    TIP_CURRENCY=os.environ.get("TIP_CURRENCY") or 'BTC'
    TIP_AMOUNT=os.environ.get("TIP_AMOUNT") or 0.00000010  # 10 sats
    BTCPAYSERVER_HOST=os.environ.get("BTCPAYSERVER_HOST") or "http://127.0.0.1"
    BTCPAYSERVER_PORT=os.environ.get("BTCPAYSERVER_PORT") or '49392'
    BTCPAYSERVER_TOR_HOST=os.environ.get("BTCPAYSERVER_TOR_HOST") or None
    BTCPAYSERVER_TOR_PORT=os.environ.get("BTCPAYSERVER_TOR_PORT") or None
    # Allowed extensions for file uploads
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webm', 'webp', 'mp4'])