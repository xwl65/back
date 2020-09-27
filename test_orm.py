from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
host = '127.0.0.1'
user = 'root'
password = '123456'
db = 'hogwartsdb'
charset = 'utf8mb4'

Base= declarative_base()

class User(Base):
    #如果创建的表结构和自己的是不相等的，那么需要加下如下语句。指明对应的表是哪一个
    __tablename__ = 'demo_user'
    id  = Column(Integer,primary_key=True)
    username = Column(String)

    password = Column(String)
    email = Column(String)

def test_orm():
    engine = create_engine(
        #传递数据库连接的方式
        'mysql+pymysql://{user}:{password}@{host}/{db}'.format(
            host=host, db=db, user=user, password=password),
        echo=True
    )
    Session = sessionmaker(bind=engine)
    sesion = Session()
    print(sesion)
    #数据的插入操作
    u1 = User(
        username="1",
        password="123456_demo",
        email="xwl65@139.com",
        id=12

    )
    sesion.add(u1)
    sesion.commit()
    u2 = sesion.query(User).filter_by(username="root_demo").first()




