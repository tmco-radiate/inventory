import sqlite3
import os.path
from datetime import datetime as dt

# テーブル作成
def create_tb():
    # 大文字部はSQL文。小文字でも問題ない。
    # persons : 担当者管理テーブル
    cur.execute('CREATE TABLE persons(id STRING PRIMARY KEY,name STRING)')

    # zaiko : 在庫管理テーブル
    cur.execute('''CREATE TABLE zaiko
                (id STRING PRIMARY KEY,
                Product_code STRING,
                Product_name STRING,
                Lot STRING,
                Initial_length real,
                Actual_length real,
                width real,
                receipt_date datetime,
                updated datetime,
                status string            
                )''')

    # データベースへコミット。これで変更が反映される。
    conn.commit()


# データ追加
def insert_data():
    # persons : 担当者管理テーブル
    cur.execute("INSERT INTO persons VALUES ('RicohTaro','リコー太郎')")

    # zaiko : 在庫管理テーブル
    cur.execute("""INSERT INTO zaiko VALUES (
                '20211103012345',
                'K80191',
                '120LCS-O PﾚｲｼｮｸM 110X1000',
                '1910301-032',
                1000,
                1000,
                110,
                '2021-11-01 12:34:56',
                '2021-11-01 12:34:56',
                'IN'
                )""")

    cur.executescript("""
                INSERT INTO zaiko VALUES (
                '20211103012346',
                'K80191',
                '120LCS-O PﾚｲｼｮｸM 110X1000',
                '1910302-032',
                1000,
                1000,
                110,
                '2021-11-01 12:34:56',
                '2021-11-01 12:34:56',
                'IN');
                INSERT INTO zaiko VALUES (
                '20211103012347',
                'K80191',
                '120LCS-O PﾚｲｼｮｸM 110X1000',
                '1910303-032',
                1000,
                1000,
                110,
                '2021-11-01 12:34:56',
                '2021-11-01 12:34:56',
                'IN');
                """)
    conn.commit()


# 在庫データ更新
def data_update(cid, cname, data):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'warehouse.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = 'UPDATE zaiko set ' + cname + '="' + data + '"'
    if cname == 'actual_length':
        sql = sql + ', status="IN" '

    sql = sql + ',updated=DATETIME("now", "localtime") WHERE id=' + cid
    cur.execute(sql)
    conn.commit()
    conn.close()


# データ検索
def data_select(s_data, s_db):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'warehouse.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = 'SELECT * FROM ' + s_db + ' WHERE id=?'
    cur.execute(sql, (s_data,))
    row = cur.fetchall()
    if len(row) > 0:
        rdata = row
    else:
        rdata = ''

    conn.close()
    return rdata


# データ一覧
def data_list(s_db):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'warehouse.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = 'SELECT * FROM ' + s_db
    cur.execute(sql)
    row = cur.fetchall()
    if len(row) > 0:
        rdata = row
    else:
        rdata = ''

    conn.close()
    return rdata


# create_tb()
# insert_data()

# c_data ='RicohTaro'
# s_db =  'persons'
# r_data = data_select(c_data, s_db)
# print(r_data)
# print(len(r_data))
# for row in r_data:
#     print(row[1])



