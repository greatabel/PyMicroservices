# boom 调用方法：
boom http://127.0.0.1:5000/api -c 100 -d 10 -q

# molotov调用方式： 
molotov i5scenarios.py -p 10 -w 200 -d 60 -qx

# 调用pytest：
python3 -m pytest
<!-- https://stackoverflow.com/questions/35998992/py-test-command-not-found-but-library-is-installed -->
完整调用： python3 -m pytest --cov=. --flake8 
