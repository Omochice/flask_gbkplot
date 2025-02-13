"""
ビジネスロジックモジュール
"""
import json
import os
import pickle
import time

import matplotlib
import matplotlib.pyplot as plt
from flask import Flask
from matplotlib.font_manager import FontProperties

import local_pattern
import similarity_measure
import utils
import db_utils

app = Flask(__name__)

matplotlib.use('Agg')

font_path = "static/TakaoPGothic.ttf"
font_prop = FontProperties(fname=font_path)


def create_scatter(title, seq, feature_class):

    with open("./static/self_information.json", "r") as jsonfile:
        json_dict = json.load(jsonfile)

    weight_dict = json_dict[feature_class]

    time_str = time.strftime('%Y%m%d%H%M%S')

    if not title:
        title = time_str

    x_coodinate, y_coodinate = utils.calculate_coordinates(seq, weight_dict)

    hist = local_pattern.make_local_pattern_histgram(x_coodinate, y_coodinate)
    # hist_str = ",".join(map(str, hist))

    plt.title(title, fontproperties=font_prop)
    plt.plot(x_coodinate, y_coodinate)

    filename = time_str + ".png"
    save_path = os.path.join(app.root_path, "static", "result", filename)
    image_path = "result/" + filename
    plt.savefig(save_path)
    plt.close()

    return image_path, hist


def decrypt_histgram(hist_str):
    decrypted_hist = list(map(int, hist_str.split(",")))
    return decrypted_hist


def calculate_similarity(histgram):
    # 比較対象の生物の(名前, ヒストグラム)のリストを取得
    # pickleから呼び出す

    similarity_results = []
    with open("static/samples/comparisons.pickle", "rb") as f:
        comparisons = pickle.load(f)

    for comparison in comparisons:
        similarity = similarity_measure.cosine_similarity(
            histgram, comparison[1])
        similarity_results.append((comparison[0], similarity))

    similarity_results.sort(key=lambda x: x[1], reverse=True)

    return similarity_results[:5]
