# jamulus-json-rpc-tests

Some rudimentary test suite for Jamulus JSON-RPC. Written in dependency-free Python 3.

```sh
# Create a secret key
echo 09047593a76ab3304f4f75a52f6485a6 > ~/.jamulusjsonrpcsecret

# Launch Jamulus client with JSON-RPC
./Jamulus --jsonrpcport 22222 --jsonrpcsecretfile ~/.jamulusjsonrpcsecret

# Run tests (in another terminal)
python3 client_tests.py
```