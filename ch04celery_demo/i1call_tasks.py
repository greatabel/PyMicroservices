from i0tasks import add
from i0tasks import app



r = add.delay(4, 46)
print(r, '#'*20, r.get(timeout=1))