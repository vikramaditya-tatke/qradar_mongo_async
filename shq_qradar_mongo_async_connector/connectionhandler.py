import asyncio
from asyncio import StreamReader, StreamWriter
import logging
import json
import startserver
from datetime import datetime
from asyncio import Queue
from mongoclient import MyMongoClient

#TODO: Use a dataclass
class ConnectionHandler:
    def __init__(self) -> None:
        """
        Initialise a Queue that is shared among the producers and the consumers.
        Assigns the name of the default collection to be created for each customer.
        Gets a MongoClient.
        """
        self.queue = Queue()
        self.coll = "Dump"
        self.mongo_client = MyMongoClient().get_client()
        self.verfication_list = startserver.get_ips()

    def insert_data(self, log: dict, customer: str):
        """
        Insert data into the default collection, one log at a time and return the _id.
        """
        try:
            database = self.mongo_client.get_database(customer)
            document_id = database.get_collection(self.coll).insert_one(log)
            print(f"ID: {document_id.inserted_id}")
        except Exception as e:
            logging.info(f"The exception in main() {e}")

    async def handle_data(self, data: bytes):
        """
        Decode the data line (JSON ByteString) to a regular string.
        Remove the prefix and convert it into a Python dictionary.
        """
        try:
            stripped_data = (data.decode("utf-8")).removeprefix(
                "<01>- hostname "
            )
            log: dict = json.loads(stripped_data)
            if log is not None:
                await self.process_log(log)
        except Exception as e:
            logging.info(f"The exception in handle_data() {e}")

    async def process_log(self, log: str):
        """
        Appends the timestamp and the client address to the log.
        """
        try:
            address, _port = self.writer.get_extra_info("peername")
            log["createdAt"] = datetime.now()
            log["eventProcessor"] = address
            # Removing spaces and periods because MongoDB doesn't accept those as Database names
            customer = log.get("domainName").replace(" ", "").replace(".", "")
            await asyncio.to_thread(self.insert_data, log, customer)
        except Exception as e:
            logging.info(f"The exception in process_log() {e}")

    async def retrieve_data(self):
        """
        Retrieves the data from the Queue and sends it to the handle_data() method.
        """
        try:
            if self.queue.qsize() > 20:
                logging.info(
                    f"Number of items in the queue: {self.queue.qsize()}"
                )
            while data := await self.queue.get():
                if data is not None:
                    await self.handle_data(data)
            logging.info(f"No data in queue: {self.queue}")
        except Exception as e:
            logging.info(f"The exception in worker() {e}")

    async def handle_connect(
        self,
        reader: StreamReader,
        writer: StreamWriter,
    ):
        """
        This is a callback function and is called as many times as required by for each new connection.
        Checks if the client address exists in our list of known IPs. Yes -> Proceeed, No -> Exit.
        Reads 1 line of data and if it is not None, puts it in a queue without waiting.
        """
        try:
            # Creates an instance variable so that it is accessible throughout the class.
            self.writer = writer
            address, port = self.writer.get_extra_info("peername")
            logging.info(f"Connection coming from {address, port}")
            if address not in self.verfication_list:
                logging.info(
                    f"Connection coming from an unknown address {address, port}. Exiting now."
                )
                exit()
            else:
                while data := await reader.readline():
                    if data is not None:
                        self.queue.put_nowait(data)
        except Exception as e:
            logging.info(f"The exception in handle_connect() {e}")
