import logging
import unittest

from jamulus import JamulusJsonRpcClient
from test_utils import wait_until


class TestJamulusClientRpc(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = JamulusJsonRpcClient("127.0.0.1", 22222)

    async def test_unparseable_json_should_close_connection(self):
        await self.client.connect()
        self.client.send_line("GET / HTTP/1.1")
        await wait_until("client is disconnected", lambda: self.client.disconnected)

    async def test_empty_array_should_result_in_invalid_request_error(self):
        await self.client.connect()
        self.client.send_line("[]")
        await wait_until(
            "error is received", lambda: self.client.received_error(-32600)
        )

    async def test_should_tolerate_blank_line_without_disconnecting(self):
        await self.client.connect()
        self.client.send_line("")
        await wait_until(
            "error is received", lambda: self.client.received_error(-32700)
        )
        self.client.send_line("[]")
        await wait_until(
            "error is received", lambda: self.client.received_error(-32600)
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
