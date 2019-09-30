from requests import Session



s = Session()
s.headers['Content-Type'] = 'application/json'
s.auth = 'tarek', 'password'

# doing some calls, auth and headers are all set!
r0 = s.get('http://localhost:5000/api').json()
r1 = s.get('http://localhost:5000/api1').json()

print(r0, '#'*20, r1)