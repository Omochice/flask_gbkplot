import pickle
import bz2
import os

PROTOCOL = pickle.HIGHEST_PROTOCOL


def ptoz(obj):
    return bz2.compress(pickle.dumps(obj, PROTOCOL), 3)


def ztop(b):
    return pickle.loads(bz2.decompress(b))


def insert(con, title, data, feature_class, img, hist):
    """ INSERT処理 """
    cur = con.cursor()
    cur.execute(
        'insert into results (title, data, feature_class, img, hist) values (?, ?, ?, ?, ?)',
        [title, data, feature_class, img, hist])

    pk = cur.lastrowid
    con.commit()

    return pk


def select(con, pk):
    """ 指定したキーのデータをSELECTする """
    cur = con.execute(
        'select id, title, data, feature_class, img, hist, created from results where id=?',
        (pk, ))
    return cur.fetchone()


def delete(con, pk, app_root_path):
    """ 指定したキーのデータをDELETEする """
    results = select(con, pk)
    # print(results["img"])
    cur = con.cursor()
    cur.execute('delete from results where id=?', (pk, ))
    con.commit()
    os.remove(os.path.join(app_root_path, "static", results["img"]))
    reset_autoincrement(con)


def reset_autoincrement(con):
    cur = con.cursor()
    cur.execute("delete from sqlite_sequence where name='results'")
    con.commit()


def select_all(con):
    """ SELECTする """
    cur = con.execute(
        'select id, title, data, feature_class, img, hist, created from results order by id desc'
    )
    return cur.fetchall()