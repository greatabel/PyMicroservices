1.
安装python3.6 以上版本

2. 
安装pip3 
（如果网速慢 可以pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package  把some-package替换成自己的慢的包 )

3.
可选  可以不做（创建python3虚拟目录，隔绝不同版本库之间相互影响）
https://docs.python.org/zh-cn/3/tutorial/venv.html
创建：
python3 -m venv tutorial-env

激活它（在Unix或MacOS上）：
source tutorial-env/bin/activate


4.
4.1
terminal底下进入工程目录下，在requirements.txt同级目录下运行：
pip install --upgrade -r requirements.txt

5.
模拟运行在:
python3 i1wsgi.py



6.
浏览器访问：

http://localhost:5000/home

已经注册好的管理员账号 可以直接登录：
管理员1
username: greatabel1@126.com
password: abel
你也可以自己注册和登录


-------------------
一般用户测试账号:(geust_test)
username:test@126.com
password: test

7.
个人主页： http://localhost:5000/profile
aws :https://ec2-35-78-249-90.ap-northeast-1.compute.amazonaws.com:80/home/1

8.可选

aws 登陆：
ssh -i "a25066_aws.pem" ubuntu@ec2-35-78-249-90.ap-northeast-1.compute.amazonaws.com
tmux
即先按下，ctrl+b，再按下d（detach）