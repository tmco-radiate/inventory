import logging
import time
import webbrowser

from flask import render_template, request, jsonify, redirect, url_for, Response, json
import config
import qrdetect.db_tool as db_tool

logger = logging.getLogger(__name__)
app = config.app
app.config['JSON_AS_ASCII'] = False
certification = True


@app.route('/')
def home():
    return render_template('index.html',
                           index=True,
                           name="index",
                           title='在庫管理')


@app.route('/stock')
def stock():
    return render_template('stock.html',
                           home=True,
                           name="home",
                           title='在庫の出入庫管理')


@app.route('/stock_proc', methods=['POST'])
def stock_proc():
    proc = request.form.get('process')
    act = request.form.get('action')
    pid = request.form.get('ID')
    logger.info({'action': act, 'ID': pid, 'process': proc})

    if act == 'out':
        cname = 'status'
        data = 'OUT'
        db_tool.data_update(pid, cname, data)
    elif act == 'in':
        cname = 'actual_length'
        data = request.form.get('length')
        db_tool.data_update(pid, cname, data)

    n_act = {
        "action": act
    }

    return n_act


@app.route('/stock_list')
def stock_list():
    cdata = db_tool.data_list('zaiko')
    # print(cdata)
    result = []
    for r in cdata:
        result.append({
            "ID": r[0],
            "code": r[1],
            "name": r[2],
            "Lot": r[3],
            "width": r[6],
            "Initial_length": r[4],
            "Actual_length": r[5],
            "status": r[9],
            "receipt_date":r[7],
            "updated":r[8],
        })

    # print(result)

    return render_template('stock_list.html',
                           stock_list=True,
                           data=result,
                           titile='在庫一覧')


@app.route('/qrcode', methods=['POST'])
def qr_code():
    qrcode = request.form.get('qrcode')
    proc = request.form.get('process')
    n_proc = ""
    logger.info({'action': 'qr_code', 'qr_code': qrcode, 'process': proc})
    if proc == "home":
        cdata = db_tool.data_select(qrcode, 'persons')
        if len(cdata) == 0:
            # 個人認証エラー
            n_proc = {
                "proc": "NG_Person"
            }
        else:
            # 個人認証OK
            for r in cdata:
                rdata = r[1]
            n_proc = {
                "proc": "stock",
                "name": rdata
            }

    elif proc == "stock":
        cdata = db_tool.data_select(qrcode, 'zaiko')
        if len(cdata) == 0:
            # 対象在庫なし
            n_proc = {
                "proc": "NG_Zaiko"
            }
        else:
            # 対象在庫のステータス取得
            # print(cdata)
            for r in cdata:
                rid = r[0]
                rcode = r[1]
                rname = r[2]
                rLot = r[3]
                rlength = str(r[5])
                rwidth = str(r[6])
                rstatus = r[9]
            n_proc = {
                "proc": "use",
                "ID": rid,
                "status": rstatus,
                "code": rcode,
                "name": rname,
                "Lot": rLot,
                "width": rwidth,
                "Actual_length": rlength
            }
            # print(n_proc)

    return n_proc


def run():
    app.run()
