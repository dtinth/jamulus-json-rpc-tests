import json
import asyncio
import uuid
import logging

logger = logging.getLogger(__name__)


class JamulusJsonRpcClient:
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.received = []
        self.connected = False
        self.disconnected = False

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.server, self.port)
        self.worker_task = asyncio.create_task(self.worker())
        self.connected = True

    async def worker(self):
        while True:
            data = await self.reader.readline()
            # If data is an empty bytes object, the connection is closed.
            if data == b"":
                logger.debug("Connection closed by server.")
                self.disconnected = True
                break
            logger.debug("Received: %s", data.decode())
            response = json.loads(data.decode())
            self.received.append(response)

    def send_line(self, line):
        self.writer.write(line.encode() + b"\n")

    def send_message(self, message):
        self.send_line(json.dumps(message))

    def send(self, method, params):
        message_id = str(uuid.uuid4())
        message = {
            "jsonrpc": "2.0",
            "id": message_id,
            "method": method,
            "params": params,
        }
        self.send_message(message)

    def received_error(self, code: int):
        """
        Returns True if an error was received.
        """
        for message in self.received:
            if message["error"] is not None:
                if message["error"]["code"] == code:
                    return True
        return False


# async def request_rpc(method, params={}):
#     reader, writer = await asyncio.open_connection("127.0.0.1", jamulus_jsonrpcport)
#     try:
#         # Create a message to get connected clients
#         message_id = str(uuid.uuid4())
#         message = {
#             "jsonrpc": "2.0",
#             "id": message_id,
#             "method": method,
#             "params": params,
#         }
#         writer.write(json.dumps(message).encode() + b"\n")

#         # Wait for the response with matching message id
#         while True:
#             data = await reader.readline()
#             response = json.loads(data.decode())
#             if response["id"] == message_id:
#                 if "result" in response:
#                     logger.debug(
#                         "Got response for {}: {}".format(method, response["result"])
#                     )
#                     return response["result"]
#                 else:
#                     # Raise an error if the response contains an error
#                     error_message = "Got error response: {}".format(response)
#                     raise Exception(error_message)
#     finally:
#         writer.close()
