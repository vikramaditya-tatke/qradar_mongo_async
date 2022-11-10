import asyncio
import functools
import logging
import dotenv
import os
from connectionhandler import ConnectionHandler
from encryptor import Encryptor
from connectionhandler import ConnectionHandler

# Load the environment file.
dotenv.load_dotenv(".env")

HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))


def get_ips() -> list:
    """
    Loads data into a list from an encrypted file and returns it to the calling function.
    """
    encryptor = Encryptor()
    loaded_key = encryptor.key_load("mongo_auth_key.key")
    decrypted_bytes = encryptor.file_decrypt(
        loaded_key, "enc_knownIPs.csv"
    ).decode("utf-8")
    ips = []
    for ip in decrypted_bytes.split(","):
        ips.append(ip)
    return ips


async def start_server():
    """
    Instantiates the ConnectionHandler class.
    Creates a task to run the retrieve_data() method.
    Creates a socketserver for each connection.
    """
    try:
        connection_handler = ConnectionHandler()
        asyncio.create_task(connection_handler.retrieve_data())
        server = await asyncio.start_server(
            functools.partial(
                connection_handler.handle_connect,
            ),
            HOST,
            PORT,
        )
        async with server:
            await server.serve_forever()
    except Exception as e:
        logging.info(f"The exception in main() {e}")
