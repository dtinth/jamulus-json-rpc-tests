import logging
import unittest

from jamulus import JamulusJsonRpcClient
from test_utils import wait_until


class TestJamulusClientRpc(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = JamulusJsonRpcClient("127.0.0.1", 22222)

    async def test_unparseable_json_should_close_connection(self):
        # https://github.com/jamulussoftware/jamulus/pull/1975#discussion_r787726223
        await self.client.connect()
        self.client.send_line("GET / HTTP/1.1")
        await wait_until("client is disconnected", lambda: self.client.disconnected)

    async def test_should_tolerate_blank_line_without_disconnecting(self):
        await self.client.connect()
        self.client.send_line("")
        await wait_until(
            "error -32700 is received", lambda: self.client.received_error(-32700)
        )
        self.client.send_line("[]")
        await wait_until(
            "error -32600 is received", lambda: self.client.received_error(-32600)
        )

    async def test_empty_array_should_result_in_invalid_request_error(self):
        await self.client.connect()
        self.client.send_line("[]")
        await wait_until(
            "error -32600 is received", lambda: self.client.received_error(-32600)
        )

    async def test_should_stop_processing_if_params_is_not_an_object(self):
        # https://github.com/jamulussoftware/jamulus/pull/1975#discussion_r788096958
        await self.client.connect()
        self.client.send("jamulus/getMode", "not an object")
        await wait_until(
            "error -32602 is received", lambda: self.client.received_error(-32602)
        )

    async def test_should_reject_if_unauthenticated(self):
        await self.client.connect()
        self.client.send("jamulus/getMode", {})
        await wait_until(
            "error 401 is received", lambda: self.client.received_error(401)
        )

    async def test_should_return_mode_if_authenticated(self):
        await self.client.connect()
        id = self.client.send(
            "jamulus/apiAuth", {"secret": "09047593a76ab3304f4f75a52f6485a6"}
        )
        self.client.send("jamulus/getMode", {})
        await wait_until(
            "received getMode",
            lambda: self.client.received_reply(id),
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
