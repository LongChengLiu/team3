from flask import Flask, request, render_template, redirect, url_for
from shujku import Session, Recipe, Making
import json

app = Flask(__name__)


# @app.route('/')
# def Find_recipe_name():
#     res1 = Session.query(Recipe).filter().all()
#     # return render_template('recipe_index.html',res1=res1)
#
#     for i in res1:
#         print(i.id)
#         print(i.recipe_name)
#         print(i.recipe_list)
#
#         id = i.id
#         recipe_name=i.recipe_name
#         recipe_list = json.loads(i.recipe_list)
#         return render_template('recipe_index.html', id=id,recipe_name=recipe_name,recipe_list=recipe_list)
#     #     return render_template('recipe_index.html', id='2',recipe_name='123',recipe_list=[1,2,3,4])
#         # for o in recipe_list:
#         #     print(o)
#         #     res2 = Session.query(Making).filter(Making.recipe_id == o).first()
#         #     if res2:
#         #         print(res2.dish_name)
#         #         print(res2.product_image)
#         #         print(res2.make_method)
#         #         print(res2.make_video)
#         #     else:
#         #         return '暂无此菜'
#
#     # res2 = Session.query(Making).filter().all()
#     # for e in res2:
#     #     print(e.rec_id)
#     #     print(e.dish_name)
#     #     print(e.product_image)
#     #     print(e.make_method)
#     #     print(e.make_video)
#
#     # return 'Hello world'
#
# @app.route('/jiaoxue/<dish_name>')
# def details(dish_name):
#     res2 = Session.query(Making).filter(Making.dish_name == dish_name).first()
#     print(res2.make_method)
#     return render_template('recipe_details.html',res2=res2)


@app.route('/')
def cai_name():
    res2 = Session.query(Making).filter().all()
    return render_template('cai_name.html', res2=res2)


@app.route('/detail/<dish_name>')
def detail(dish_name):
    nm = Session.query(Making).filter(Making.dish_name == dish_name).first()
    return render_template('cai_name_detail.html',nm=nm)

@app.template_filter('int')
def int_(num):
    return int(num)

@app.template_filter('str')
def str_(num):
    return str(num)
@app.template_filter('jsonloads')
def loads_(json_):
    return json.loads(json_)


if __name__ == '__main__':
    app.run(host='192.168.1.166')
