import json
from molotov import scenario

# https://molotov.readthedocs.io/en/stable/
# 调用方式： molotov i5scenarios.py -p 10 -w 200 -d 60 -qx



_API = 'http://localhost:5000/api'

@scenario(5)
async def scenario_one(session):
    async with session.get(_API) as resp:
        res = await resp.json()
        assert resp['Hello'] == 'World!'
        assert resp.status == 200
        # print(res)

# @scenario(5)
# async def scenario_one(session):
#     res = await session.get('http://localhost:5000/api').json()
#     assert res['Hello'] == 'World!'
#     print('#'*10, res)

@scenario(30)
async def scenario_two(session):
    somedata = json.dumps({'OK': 1})
    async with session.post(_API, data=somedata) as resp:
        assert resp.status == 200

# @scenario(30)
# async def scenario_two(session):
#     somedata = json.dumps({'OK': 1})
#     res = await session.post('http://localhost:5000/api', data=somedata)
#     assert res.status_code == 200