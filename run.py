import os
import sqlite3
import json

from flask import Flask, flash, g, redirect, render_template, request, url_for

import models
import pickle
import bz2

app = Flask(__name__)
app.config.from_object(__name__)

PROTOCOL = pickle.HIGHEST_PROTOCOL

app.config.update(
    dict(
        DATABASE=os.path.join(app.root_path, 'db.sqlite3'),
        SECRET_KEY='mizuta-labo',
    ))

# 以下、DB接続関連の関数


def connect_db():
    """ データベース接続に接続します """
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def get_db():
    """ connectionを取得します """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """ db接続をcloseします """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def ptoz(obj):
    return bz2.compress(pickle.dumps(obj, PROTOCOL), 3)


def ztop(b):
    return pickle.loads(bz2.decompress(b))


# 以下、画面/機能毎の関数


@app.route('/')
def index():
    """ 一覧画面 """
    con = get_db()
    results = models.select_all(con)
    return render_template('index.html', results=results)


@app.route('/create')
def create():
    """ 新規作成画面 """
    json_path = os.path.join(app.root_path, "static", "self_information.json")
    with open(json_path, "r") as jsonfile:
        json_dict = json.load(jsonfile)

    classes = sorted(list(json_dict.keys()))
    return render_template('edit.html', classes=classes)


@app.route('/analysis', methods=['POST'])
def analysis():
    """ 分析実行処理 """

    title = request.form['title']
    data = request.form['data']
    feature_class = request.form['class']

    img, hist = models.create_scatter(title, data, feature_class)

    con = get_db()

    pk = models.insert(con, title, data, feature_class, img, ptoz(hist))
    flash('登録処理が完了しました。')
    return redirect(url_for('view', pk=pk))


@app.route('/delete/<pk>', methods=['POST'])
def delete(pk):
    """ 結果削除処理 """
    con = get_db()
    models.delete(con, pk)
    flash('削除処理が完了しました。')
    return redirect(url_for('index'))


@app.route('/view/<pk>')
def view(pk):
    """ 結果参照処理 """
    con = get_db()
    result = models.select(con, pk)
    histgram = ztop(result["hist"])

    similary_top_five = models.calculate_similarity(histgram)

    return render_template('view.html',
                           result=result,
                           histogram=histgram,
                           top_five=similary_top_five)


if __name__ == '__main__':
    app.run(debug=True)
