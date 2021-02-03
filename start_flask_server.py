import os
import sqlite3
from app import create_app
from stem.control import Controller  # tor
from config import Config
from app.db import get_db

KEY_PATH = Config.TOR_FOLDER
TOR_PORT = Config.TOR_PORT
FLASK_PORT = Config.FLASK_PORT
FLASK_TOR = Config.FLASK_TOR

app = create_app()


def write_onion_to_db(onion):
    """
    write the onion service to db to find in the app later
    """
    print('Writing onion to db')
    print(onion)
    db = sqlite3.connect(
        Config.SQLALCHEMY_DATABASE_URI,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    db.execute("INSERT INTO onion_url (onion) VALUES (?)", (onion,))
    db.commit()


# This Code here is only for Tor, will run either prod or dev setup based on
# environment variable `FLASK_TOR`
if __name__ == "__main__":
    if FLASK_TOR == 'True':
        print("Connecting to Tor")
        if os.environ.get('FLASK_ENV') == 'production':
            # https://stem.torproject.org/tutorials/over_the_river.html
            with Controller.from_port() as controller:
                controller.authenticate()

                # If we don'tt have onion address yet, create new one
                if not os.path.exists(KEY_PATH):
                    # Flask is running in PORT 5000, MAP port 80 through tor to 5000
                    service = controller.create_ephemeral_hidden_service(
                        {TOR_PORT: FLASK_PORT},
                        await_publication = True
                    )
                    print(f"{service.service_id}.onion")
                    # Write new tor keys to disk
                    with open(KEY_PATH, 'w') as key_file:
                        key_file.write(f'{service.private_key_type}:{service.private_key}')
                else:
                    with open(KEY_PATH) as key_file:
                        key_type, key_content = key_file.read().split(':', 1)

                    print(key_type, key_content)
                    service = controller.create_ephemeral_hidden_service(
                        {TOR_PORT: FLASK_PORT},
                        key_type=key_type,
                        key_content=key_content,
                        await_publication=True
                    )
                    onion = f"{service.service_id}.onion"
                    print(onion)
                    write_onion_to_db(onion)
                # Start the application
                try:
                    app.run()
                finally:
                    print("Shutting Down")
                    controller.remove_ephemeral_hidden_service(service.service_id)
        else:
            with Controller.from_port() as controller:
                controller.authenticate()
                service = controller.create_ephemeral_hidden_service(
                    {TOR_PORT: FLASK_PORT},
                    await_publication=True
                )
                onion = f"{service.service_id}.onion"
                print(onion)
                write_onion_to_db(onion)
                # Start the application
                try:
                    app.run()
                finally:
                    print("Shutting Down")
                    controller.remove_ephemeral_hidden_service(service.service_id)
