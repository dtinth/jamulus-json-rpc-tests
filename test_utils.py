import asyncio

# Wait until a predicate returns true
async def wait_until(description: str, predicate: callable, timeout=10):
    start = asyncio.get_event_loop().time()
    while asyncio.get_event_loop().time() - start < timeout:
        if predicate():
            return
        await asyncio.sleep(0.1)
    raise Exception("Timed out waiting until {}".format(description))
