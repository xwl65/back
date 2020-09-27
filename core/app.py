from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import json
from flask_jwt_extended import  jwt_manager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from jenkinsapi.jenkins import Jenkins

from json import dumps
app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
#此为轻量级的数据库，不适应于大量的数据库
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#使用自己本地的mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/python14'
#token管理 。#密码改个名字，不然会被不怀好意的人窃取
app.config['JWT_SECRET_KEY'] = 'localhost'  # Change this
# done: 输出中文json
app.config["JSON_AS_ASCII"] = False
db = SQLAlchemy(app)
jenkins=Jenkins(
    'http://localhost:8080',
    username='x',
    password='11bc63a77c1808e57f2dfeaafef3fc7f31' )
class User(db.Model):
    __tablename__ = "userxwl"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Testcase(db.Model):
    __tablename__ = "xwl_testcase"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    data = db.Column(db.String(1024), unique=False, nullable=False)

    def __repr__(self):
        return '<TestCase %r>' % self.name

class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Integer, unique=True, nullable=False,default=0)

    def __repr__(self):
        return '<Task %r>' % self.name

class TestCaseApi(Resource):
    #有如下装饰器，就对一些操作有了要求，必须得有token才能进行操作
    @jwt_required
    def get(self):
        r=[]
        res={}
        for t in Testcase.query.all():
            res['id']=t.id
            res['name']=t.name
            res['description']=t.description
            res['data']=t.data
            r.append(res)
        #查询所有的case出来
        #return  Testcase.query.all()
        return r
        #return {'id':t.id,'name':t.name}

    @jwt_required
    def post(self):
        t = Testcase(
            name = request.json['name'],
            description = request.json['description'],
            data = request.json['data']
        )
        # # # 新增数据
        db.session.add(t)
        db.session.commit()
        return {
            'msg': 'ok'
        }
    @jwt_required
    def put(self):
        '''
        用例更新:先查找需要更新的用例,再更新内容;
        :return:
        '''
        name = request.json.get('name', None)
        description = request.json.get('description', None)
        update_name = request.json.get('update_name', None)
        update_description = request.json.get('update_description', None)
        update_data = request.json.get('update_data', None)

        t = Testcase.query.filter_by(name=name, description=description).first()
        if t is None:
            return jsonify(
                errcode=1,
                errmsg='用例不存在')
        else:
            t.name = update_name
            t.description = update_description
            t.data = update_data
            db.session.commit()
            return {
                'msg': 'update success'
            }

    # done：删除用例
    @jwt_required
    def delete(self):
        name = request.json.get('name', None)
        description = request.json.get('description', None)
        t = Testcase.query.filter_by(name=name, description=description).first()
        if t is None:
            return jsonify(
                errcode=1,
                errmsg='用例不存在')
        else:
            db.session.delete(t)
            db.session.commit()
            return {
                'msg': 'ok'
            }


# done: 注册用户
class RegisterApi(Resource):

    def get(self):
        return {'hello': '123'}
    def post(self):
        '''
        :return: 注册成功信息
        '''
        t = User(username=request.json['username'],
                 password=request.json['password'],
                 email=request.json['email'])
        db.session.add(t)
        db.session.commit()
        return {
            'msg': 'ok'
        }

class Hello(Resource):
    def get(self):
        return {'hello': 'world'}

class LoginApi(Resource):
    def get(self):



        pass

    def post(self):
        #todo：查询数据库
        username=request.json.get('username',None)
        print(123456)
        print(username)
        #通常密码不能原文存储
        password=request.json.get('password',None)
        print('--------')
        print(password)

        user=User.query.filter_by(username=username,password=password).first()
        print(789)
        print(user)
        print(type(user))
        if user is None:
            return jsonify(
                errcode=1,
                errmsg='用户名或者密码不对'
            )
        else:
            return {
                'errcode':0,
                'errmsg':'ok',
                'username':user.username,
                'token': create_access_token(identity=user.username)

            }

class TaskApi(Resource):
    #get里面只是一个获取，真正的执行是在post里面。这是task任务属性所决定的。
    def get(self):
        count = 0
        my_job = {}
        for job_name in jenkins.keys():
            job_name = jenkins.get_job(job_name)
            count = count + 1
            my_job[count]=job_name

            # m = Task.query.filter_by(task_name=job, id=count).first()
            # if m is None:
            #     return jsonify(
            #         errcode=1,
            #         errmsg='用例不存在')
            #     db.session.add(t)
            #     db.session.commit()


        return my_job


    @jwt_required
    def post(self):
        #todo:用例获取
        testcases=request.json.get('testcases',None)
        print(111)
        print(testcases)
        #todo：调度Jenkins
        jenkins['testcase'].invoke(securitytoken='11bc63a77c1808e57f2dfeaafef3fc7f31',
                                   build_params={
                                       'testcases': testcases

                                   })
        return {
            'errcode': 0,
            'errmsg': 'ok'
        }

        #todo:异步处理
        pass

class ReportApi(Resource):
    def get(self):
        # 展示报告数据和曲线图

        pass

    def post(self):
        # todo: pull模式 主动从jenkins中拉取数据
        jenkins['testcase'].get_last_build().get_resultset()
        # todo: push模式 让jenkins node主动push到服务器
        # todo: 把测试报告数据与测试报告文件保存
        pass

api.add_resource(TestCaseApi, '/testcase')

api.add_resource(RegisterApi, '/registerapi')
api.add_resource(LoginApi, '/login')
api.add_resource(TaskApi, '/task')
api.add_resource(Hello, '/')
if __name__ == '__main__':
    app.run(debug=True)