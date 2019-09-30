import msgpack

data = {"this": "is", "some": "data", 1: 2}

r = msgpack.dumps(data)
print(r)

o = msgpack.loads(r)
print(o)