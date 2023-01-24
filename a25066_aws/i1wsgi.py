"""App entry point."""
import os
import sys
import json
import random
import flask_login
from flask_cors import CORS

from flask import send_from_directory
from flask import request
from flask import url_for
from flask import redirect, session
from flask import Blueprint, render_template as rt
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, Response
from flask import jsonify
from flask_cors import CORS
from flask import make_response

# from flask_wtf.csrf import CSRFProtect
from flask import flash

from movie import create_app

import es_search
import logging


import recommandation

# from movie.domain.model import Director, Review, Movie

# from html_similarity import style_similarity, structural_similarity, similarity
# from common import set_js_file

app = create_app()
app.secret_key = "ABCabc123"
app.debug = True


handler = logging.FileHandler("flask.log", encoding="UTF-8")
handler.setLevel(
    logging.DEBUG
)  # 设置日志记录最低级别为DEBUG，低于DEBUG级别的日志记录会被忽略，不设置setLevel()则默认为NOTSET级别。
logging_format = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s"
)
handler.setFormatter(logging_format)
app.logger.addHandler(handler)


CORS(app)

# 防御点3: CSRF攻击模拟 防御
# CSRFProtect(app)

# --- total requirement ----


# ---start  数据库 ---

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campus_data.db"
# 防御点1: 防止入sql-inject ，不实用sql注入，sqlchemy让代码ORM化，安全执行
db = SQLAlchemy(app)

last_upload_filename = None
# --- end   数据库 ---
admin_list = ["admin@126.com", "greatabel1@126.com"]


class User(db.Model):
    """Create user table"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    nickname = db.Column(db.String(80))
    role = db.Column(db.String(80))
    school_class = db.Column(db.String(80))
    school_grade = db.Column(db.String(80))

    def __init__(
        self, username, password, nickname="", role="", school_class="", school_grade=""
    ):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.role = role
        self.school_class = school_class
        self.school_grade = school_grade


class Blog(db.Model):
    """
    ppt数据模型
    """

    # 主键ID
    id = db.Column(db.Integer, primary_key=True)
    # ppt标题
    title = db.Column(db.String(100))
    # ppt正文
    text = db.Column(db.Text)

    def __init__(self, title, text):
        """
        初始化方法
        """
        self.title = title
        self.text = text


# # 老师当前布置作业的表
# class TeacherWork(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(80), unique=True)
#     detail = db.Column(db.String(500))
#     answer = db.Column(db.String(5000))
#     course_id = db.Column(db.Integer)

#     def __init__(self, title, detail, answer, course_id):
#         self.title = title
#         self.detail = detail
#         self.answer = answer
#         self.course_id = course_id


# class StudentWork(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     userid = db.Column(db.Integer)
#     answer = db.Column(db.String(5000))
#     score = db.Column(db.DECIMAL(10, 2))
#     course_id = db.Column(db.Integer)

#     def __init__(self, userid, answer, score, course_id):
#         self.userid = userid
#         self.answer = answer
#         self.score = score
#         self.course_id = course_id


### -------------start of home
def replace_html_tag(text, word):
    new_word = '<font color="red">' + word + "</font>"
    len_w = len(word)
    len_t = len(text)
    for i in range(len_t - len_w, -1, -1):
        if text[i : i + len_w] == word:
            text = text[:i] + new_word + text[i + len_w :]
    return text


class PageResult:
    def __init__(self, data, page=1, number=3):
        self.__dict__ = dict(zip(["data", "page", "number"], [data, page, number]))
        self.full_listing = [
            self.data[i : i + number] for i in range(0, len(self.data), number)
        ]
        self.totalpage = len(data) // number
        print("totalpage=", self.totalpage)

    def __iter__(self):
        if self.page - 1 < len(self.full_listing):
            for i in self.full_listing[self.page - 1]:
                yield i
        else:
            return None

    def __repr__(self):  # used for page linking
        return "/home/{}".format(self.page + 1)  # view the next page


@app.route("/home/<int:pagenum>", methods=["GET"])
@app.route("/home", methods=["GET", "POST"])
def home(pagenum=1):
    print("home " * 10)
    app.logger.info("home info log")

    blogs = Blog.query.all()
    user = None
    if "userid" in session:
        user = User.query.filter_by(id=session["userid"]).first()
    else:
        print("userid not in session")
    print("in home", user, "blogs=", len(blogs), "*" * 20)
    if request.method == "POST":
        search_list = []
        keyword = request.form["keyword"]
        print("keyword=", keyword, "-" * 10)
        if keyword is not None:
            for blog in blogs:
                if keyword in blog.title or keyword in blog.text:
                    blog.title = replace_html_tag(blog.title, keyword)
                    print(blog.title)
                    blog.text = replace_html_tag(blog.text, keyword)

                    search_list.append(blog)

            if len(search_list) == 0 and keyword in ["天气", "心情"]:
                es_content = es_search.mysearch(keyword)
                search_list.append(es_content)
            # for movie in notice_list:
            #     if movie.director.director_full_name == keyword:
            #         search_list.append(movie)

            #     for actor in movie.actors:
            #         if actor.actor_full_name == keyword:
            #             search_list.append(movie)
            #             break

            #     for gene in movie.genres:
            #         if gene.genre_name == keyword:
            #             search_list.append(movie)
            #             break
        print("search_list=", search_list, "=>" * 5)
        return rt(
            "home.html",
            listing=PageResult(search_list, pagenum, 10),
            user=user,
            keyword=keyword,
        )
        # return rt("home.html", listing=PageResult(search_list, pagenum, 2), user=user)

    return rt("home.html", listing=PageResult(blogs, pagenum), user=user)


@app.route("/blogs/create", methods=["GET", "POST"])
def create_blog():
    """
    创建ppt文章
    """
    if request.method == "GET":
        # 如果是GET请求，则渲染创建页面
        return rt("create_blog.html")
    else:
        # 从表单请求体中获取请求数据
        title = request.form["title"]
        text = request.form["text"]

        # 创建一个ppt对象
        blog = Blog(title=title, text=text)
        db.session.add(blog)
        # 必须提交才能生效
        db.session.commit()
        # 创建完成之后重定向到ppt列表页面
        return redirect("/blogs")


@app.route("/blogs", methods=["GET"])
def list_notes():
    """
    查询ppt列表
    """
    blogs = Blog.query.all()
    # 渲染ppt列表页面目标文件，传入blogs参数
    return rt("list_blogs.html", blogs=blogs)


@app.route("/blogs/update/<id>", methods=["GET", "POST"])
def update_note(id):
    """
    更新cousre
    """
    if request.method == "GET":
        # 根据ID查询ppt详情
        blog = Blog.query.filter_by(id=id).first_or_404()
        # 渲染修改笔记页面HTML模板
        return rt("update_blog.html", blog=blog)
    else:
        # 获取请求的ppt标题和正文
        title = request.form["title"]
        text = request.form["text"]

        # 更新ppt
        blog = Blog.query.filter_by(id=id).update({"title": title, "text": text})
        # 提交才能生效
        db.session.commit()
        # 修改完成之后重定向到ppt详情页面
        return redirect("/blogs/{id}".format(id=id))


@app.route("/blogs/<id>", methods=["GET", "DELETE"])
def query_note(id):
    """
    查询cousre详情、删除cousre
    """
    if request.method == "GET":
        # 到数据库查询ppt详情
        blog = Blog.query.filter_by(id=id).first_or_404()
        print(id, blog, "in query_blog", "@" * 20)
        # 渲染ppt详情页面
        return rt("query_blog.html", blog=blog)
    else:
        # 删除ppt
        blog = Blog.query.filter_by(id=id).delete()
        # 提交才能生效
        db.session.commit()
        # 返回204正常响应，否则页面ajax会报错
        return "", 204


@app.route("/users", methods=["GET"])
def list_users():
    """
    查询用户列表
    """
    users = User.query.all()
    print("users=", users)
    # 渲染ppt列表页面目标文件，传入blogs参数
    return rt("list_users.html", users=users)


@app.route("/users/create", methods=["GET", "POST"])
def create_user():
    """
    创建android_security_apk文章
    """
    if request.method == "GET":
        # 如果是GET请求，则渲染创建页面
        return rt("create_user.html")
    else:
        # 从表单请求体中获取请求数据
        username = request.form["username"]
        nickname = request.form["nickname"]
        password = request.form["password"]
        role = request.form["role"]
        school_grade = request.form["school_grade"]
        school_class = request.form["school_class"]

        # 创建一个ppt对象
        user = User(
            username=username,
            nickname=nickname,
            password=password,
            role=role,
            school_grade=school_grade,
            school_class=school_class,
        )
        db.session.add(user)
        # 必须提交才能生效
        db.session.commit()
        # 创建完成之后重定向到ppt列表页面
        return redirect("/users")


@app.route("/users/<id>", methods=["GET", "DELETE"])
def query_user(id):
    """
    查询android_security_apk详情、删除ppt
    """
    if request.method == "GET":
        # 到数据库查询ppt详情
        user = User.query.filter_by(id=id).first_or_404()
        print(id, user, "in query_user", "@" * 20)
        # 渲染ppt详情页面
        return rt("query_user.html", user=user)
    else:
        print("delete user")
        # 删除ppt
        user = User.query.filter_by(id=id).delete()
        # 提交才能生效
        db.session.commit()
        # 返回204正常响应，否则页面ajax会报错
        return "", 204


### -------------end of home
@app.route("/recommend", methods=["GET", "DELETE"])
def recommend():
    """
    查询cousre item 推荐
    """
    if request.method == "GET":
        choosed = recommandation.main()
        print("给予离线交互数据进行协同推荐")
        print(choosed, "#" * 20)
        print("给予离线交互数据进行协同推荐")

        # 添加一些冷启动的推荐, 弥补协同过滤启动数据不足的问题
        blogs = Blog.query.all()
        r_index = random.randint(0, len(blogs) - 1)
        cold_r = blogs[r_index].title

        print(cold_r, "#####in cold start")
        choosed.append(cold_r)
        return rt("recommend.html", choosed=choosed)


### -------------start of profile


@app.route("/profile", methods=["GET", "DELETE"])
def query_profile():
    """
    查询cousre详情、删除ppt
    """

    id = session["userid"]

    if request.method == "GET":

        # 到数据库查询ppt详情
        user = User.query.filter_by(id=id).first_or_404()
        print(user.username, user.password, "#" * 5)
        # 渲染ppt详情页面
        r = make_response(rt("profile.html", user=user))
        # 防御点2：xss攻击，实用csp方式： https://content-security-policy.com/
        r.headers.set(
            "Content-Security-Policy",
            "default-src * 'unsafe-inline'; connect-src 'self' 'nonce-987654321' ",
        )
        return r
    else:
        # 删除ppt
        user = User.query.filter_by(id=id).delete()
        # 提交才能生效
        db.session.commit()
        # 返回204正常响应，否则页面ajax会报错
        return "", 204


@app.route("/profiles/update/<id>", methods=["GET", "POST"])
def update_profile(id):
    """
    更新ppt
    """
    if request.method == "GET":
        # 根据ID查询ppt详情
        user = User.query.filter_by(id=id).first_or_404()
        # 渲染修改笔记页面HTML模板
        return rt("update_profile.html", user=user)
    else:
        # 获取请求的ppt标题和正文
        password = request.form["password"]
        nickname = request.form["nickname"]
        school_class = request.form["school_class"]
        school_grade = request.form["school_grade"]
        role = request.form["role"]
        # 更新ppt
        user = User.query.filter_by(id=id).update(
            {
                "password": password,
                "nickname": nickname,
                "school_class": school_class,
                "school_grade": school_grade,
                "role": role,
            }
        )
        # 提交才能生效
        db.session.commit()
        # 修改完成之后重定向到ppt详情页面
        return redirect("/profile")


### -------------end of profile


@app.route("/course/<id>", methods=["GET"])
def course_home(id):
    """
    查询ppt详情、删除ppt
    """
    if request.method == "GET":
        # 到数据库查询ppt详情
        blog = Blog.query.filter_by(id=id).first_or_404()
        teacherWork = TeacherWork.query.filter_by(course_id=id).first()
        print(id, blog, "in query_blog", "@" * 20)
        # 渲染ppt详情页面
        return rt("course.html", blog=blog, teacherWork=teacherWork)
    else:
        return "", 204


login_manager = flask_login.LoginManager(app)
user_pass = {}


# @app.route("/call_bash", methods=["GET"])
# def call_bash():
#     i0bash_caller.open_client("")
#     return {}, 200


@app.route("/statistics", methods=["GET"])
def relationship():
    # static/data/test_data.json
    filename = os.path.join(app.static_folder, "data.json")
    # with open(filename) as test_file:
    with open(filename, "r", encoding="utf-8") as test_file:
        d = json.load(test_file)
    print(type(d), "#" * 10, d)
    return jsonify(d)


@app.route("/index_a/")
def index():
    return rt("index-A.html")


@app.route("/index_b/")
def index_b():
    return rt("index-B.html")


@login_manager.user_loader
def load_user(email):
    print("$" * 30)
    return user_pass.get(email, None)


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        data = User.query.filter_by(username=email, password=password).first()
        print(data, "@" * 10)
        if data is not None:
            print("test login")
            session["logged_in"] = True

            if email in admin_list:
                session["isadmin"] = True
                print("@" * 20, "setting isadmin")
            session["userid"] = data.id

            print("login sucess", "#" * 20, session["logged_in"])

            # w = TeacherWork.query.get(1)
            # print('w=', w, w.answer, w.title)
            # if w is not None:
            #     session['title'] = w.title
            #     session['detail'] = w.detail
            #     session['answer'] = w.answer

            return redirect(url_for("home", pagenum=1))
        else:
            return "Not Login"
    except Exception as e:
        print(e)
        return "Not Login"
    return redirect(url_for("home", pagenum=1))


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for("home", pagenum=1))
    # if DB.get_user(email):
    data = User.query.filter_by(username=email).first()
    # if email in user_pass:
    if data is not None:
        print("already existed user")
        flash("already existed user")
        return redirect(url_for("home", pagenum=1))
    # salt = PH.get_salt()
    # hashed = PH.get_hash(pw1 + salt)
    print("register", email, pw1)
    new_user = User(username=email, password=pw1)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("home", pagenum=1))


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("home", pagenum=1))


reviews = []


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized"


# --------------------------
@app.route("/add_ppt", methods=["GET"])
def add_ppt():
    return rt("index.html")


@app.route("/upload_ppt", methods=["POST"])
def upload_ppt():

    # detail = request.form.get("detail")
    # 从表单请求体中获取请求数据

    title = request.form.get("title")
    text = request.form.get("detail")

    # 创建一个ppt对象
    blog = Blog(title=title, text=text)
    db.session.add(blog)
    # 必须提交才能生效
    db.session.commit()
    # 创建完成之后重定向到ppt列表页面
    # return redirect("/blogs")

    return redirect(url_for("add_ppt"))


@app.route("/student_work", methods=["POST"])
def student_work():
    return redirect(url_for("student_index"))


@app.route("/student_index", methods=["GET"])
def student_index():
    return rt("student_index.html")


# @app.route("/", methods=["GET"])
# def index():
#     return rt("index.html")


@app.route("/file/upload", methods=["POST"])
def upload_part():  # 接收前端上传的一个分片
    task = request.form.get("task_id")  # 获取文件的唯一标识符
    chunk = request.form.get("chunk", 0)  # 获取该分片在所有分片中的序号
    filename = "%s%s" % (task, chunk)  # 构造该分片的唯一标识符
    print("filename=", filename)
    upload_file = request.files["file"]
    upload_file.save("./upload/%s" % filename)  # 保存分片到本地
    return rt("index.html")


@app.route("/file/merge", methods=["GET"])
def upload_success():  # 按序读出分片内容，并写入新文件
    global last_upload_filename
    target_filename = request.args.get("filename")  # 获取上传文件的文件名
    last_upload_filename = target_filename
    print("last_upload_filename=", last_upload_filename)
    task = request.args.get("task_id")  # 获取文件的唯一标识符
    chunk = 0  # 分片序号
    with open("./upload/%s" % target_filename, "wb") as target_file:  # 创建新文件
        while True:
            try:
                filename = "./upload/%s%d" % (task, chunk)
                source_file = open(filename, "rb")  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间

    return rt("index.html")


@app.route("/file/list", methods=["GET"])
def file_list():
    files = os.listdir("./upload/")  # 获取文件目录
    # print(type(files))
    files.remove(".DS_Store")
    # files = map(lambda x: x if isinstance(x, unicode) else x.decode('utf-8'), files)  # 注意编码
    return rt("list.html", files=files)


@app.route("/file/download/<filename>", methods=["GET"])
def file_download(filename):
    def send_chunk():  # 流式读取
        store_path = "./upload/%s" % filename
        print("store_path=", store_path)
        with open(store_path, "rb") as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type="application/octet-stream")


# Custom static data
@app.route("/cdn/<path:filename>")
def custom_static(filename):
    print("#" * 20, filename, " in custom_static", app.root_path)
    return send_from_directory(
        "/Users/abel/Downloads/AbelProject/FlaskRepository/ppt_platform/upload/",
        filename,
    )


# --------------------------


if __name__ == "__main__":
    db.create_all()

    app.run(host="localhost", port=5000, threaded=False)
