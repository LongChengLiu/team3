from sqlalchemy import String, Column, create_engine,TEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
from my_config import my_secert



Base = declarative_base()
class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(String(5), primary_key=True)
    recipe_list = Column(String(10000))
    recipe_name = Column(String(10))


class Making(Base):
    __tablename__ = 'making'
    make_method = Column(TEXT())
    dish_name = Column(String(20), primary_key=True)
    image_count = Column(String(5))
    video_list = Column(String(10000))


# 连接   哪种数据库 + 数据库驱动://用户:密码@主机:端口号/数据库名

engine = create_engine(my_secert)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)()

# 插入
# recipe_list = [1,2,3,4]
# recipe_list=json.dumps(recipe_list)
# print(recipe_list)



# r1 = Session.query(Recipe).filter_by().all()
# print(r1)
Session.commit()
Session.close()
