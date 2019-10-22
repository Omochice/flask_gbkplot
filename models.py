"""
ビジネスロジックモジュール
"""
import json
import os
import time

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask
from matplotlib.font_manager import FontProperties
from pandas.plotting import scatter_matrix

import utils

app = Flask(__name__)

matplotlib.use('Agg')

font_path = "static/TakaoPGothic.ttf"
font_prop = FontProperties(fname=font_path)


def create_scatter(title, seq, feature_class):

    VECTOR_DICT = {"a": [1, 1], "t": [-1, 1], "g": [-1, -1], "c": [1, -1]}
    x_coodinate = [0]
    y_coodinate = [0]

    with open("./static/self_information.json", "r") as jsonfile:
        json_dict = json.load(jsonfile)

    weight_dict = json_dict[feature_class]

    for triplet in utils.window_search(seq):
        x_coodinate.append(x_coodinate[-1] + VECTOR_DICT[triplet[-1]][0] *
                           weight_dict.get(triplet, 1))
        y_coodinate.append(y_coodinate[-1] + VECTOR_DICT[triplet[-1]][1] *
                           weight_dict.get(triplet, 1))

    plt.title(title, fontproperties=font_prop)
    plt.plot(x_coodinate, y_coodinate)

    filename = time.strftime('%Y%m%d%H%M%S') + ".png"
    save_path = os.path.join(app.root_path, "static", "result", filename)
    url = "result/" + filename
    plt.savefig(save_path)
    plt.close()

    return url


def insert(con, title, data, feature_class, img):
    """ INSERT処理 """
    cur = con.cursor()
    cur.execute(
        'insert into results (title, data, feature_class, img) values (?, ?, ?, ?)',
        [title, data, feature_class, img])

    pk = cur.lastrowid
    con.commit()

    return pk


def select(con, pk):
    """ 指定したキーのデータをSELECTする """
    cur = con.execute(
        'select id, title, data, feature_class, img, created from results where id=?',
        (pk, ))
    return cur.fetchone()


def delete(con, pk):
    """ 指定したキーのデータをDELETEする """
    results = select(con, pk)
    # print(results["img"])
    cur = con.cursor()
    cur.execute('delete from results where id=?', (pk, ))
    con.commit()
    os.remove(os.path.join(app.root_path, "static", results["img"]))
    reset_autoincrement(con)


def reset_autoincrement(con):
    cur = con.cursor()
    cur.execute("delete from sqlite_sequence where name='results'")
    con.commit()


def select_all(con):
    """ SELECTする """
    cur = con.execute(
        'select id, title, data, feature_class, img, created from results order by id desc'
    )
    return cur.fetchall()
