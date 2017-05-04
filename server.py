# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, send_from_directory
from pymongo import DESCENDING
import tests
import datetime
from datetime import timedelta
from flask import make_response, current_app
from functools import update_wrapper
from bson.objectid import ObjectId
import materials as m
from collections import Counter

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
c = 0

ml = dict()
mode = True

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Allow-Methods'] = "*"
            h['Access-Control-Max-Age'] = str(max_age)
            # if headers is not None:
            #     h['Access-Control-Allow-Headers'] = headers
            h['Access-Control-Allow-Headers'] = "content-type"

            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


@app.route('/')
@crossdomain(origin="*",methods=['OPTIONS', 'GET'])
def send_index():
    return send_from_directory('tmp', 'index.html')


@app.route('/<path:path>', methods=['OPTIONS', 'GET'])
@crossdomain(origin="*")
def send_js(path):
    return send_from_directory('tmp', path)


@app.route('/startSetting', methods=['OPTIONS', 'GET'])
@crossdomain(origin="*")
def get_init_materials():
    global ml, c

    x = {"materials": [
            {"id": "1", "type": "material", "title": "AB=AC", "canBeForged": True, "amount": 3, "icon": "line"},
            {"id": "2", "type": "material", "title": "AC是圆O直径", "canBeForged": True, "amount": 2, "icon": "cir"}],
            # {"id": "3", "type": "material", "title": "AC是圆O直径", "canBeForged": True}],
            # {"id": "4", "type": "material", "title": "DF是圆O切线", "canBeForged": True},
            "drugs": [
                {"id": "5", "type": "drug", "title": "圆周角定理推论", "desc": "直径所对圆周角是直角。", "shortTitle": "圆周角定理" ,"icon": "cir"},
                {"id": "6", "type": "drug", "title": "等腰三角形性质", "desc": "等腰三角形顶角平分线、底边上中线、底边上高相互重合。", "shortTitle": "等腰三角形" ,"icon": "tran"},
                {"id": "7", "type": "drug", "title": "三角形中位线定义", "desc": "连接三角形两边重点线段叫做三角形中位线。", "shortTitle": "中位线定义", "icon": "tran"},
                {"id": "8", "type": "drug", "title": "三角形中位线定理", "desc": "三角形中位线平行于三角形第三边，且等于第三边一半。","shortTitle": "中位线定理" ,"icon": "tran"}
            ]}
    ml = {t["id"]: t for t in x["materials"]}
    y = {t["id"]: t for t in x["drugs"]}
    ml = {**ml, **y}
    c = 8
    return jsonify(x)


@app.route('/forge/<mid>', methods=['OPTIONS', 'POST', 'GET'])
@crossdomain(origin="*")
def forge(mid):
    global c, ml
    result = list()
    if request.method == "GET":
        print(mid)
        this_m = ml[mid]
        if this_m["title"] == "AC是圆O直径":
            c += 1
            r = {"id": str(c), "type": "material", "title": "CO=OA", "isGoal": True ,"canBeForged": False, "amount": 1, "icon": "line"}
            ml[str(c)] = r
            result.append(r)

        if this_m["title"] == "AB=AC":
            c += 1
            r = {"id": str(c), "type": "material", "title": "△ABC是等腰三角形", "canBeForged": False, "amount": 1, "icon": "tran"}
            ml[str(c)] = r
            result.append(r)

        if this_m["title"] == "∠ADC=90°":
            c += 1
            r = {"id": str(c), "type": "material", "title": "AD⊥BC", "canBeForged": False, "amount": 1, "icon": "line"}
            ml[str(c)] = r
            result.append(r)

        if this_m["title"] == "DF是圆O切线":
            c += 1
            r = {"id": str(c), "type": "material", "title": "OD⊥DF", "canBeForged": False, "amount": 1, "icon": "line"}
            ml[str(c)] = r
            result.append(r)

    return jsonify(result)


# {"elements": []}
@app.route('/fireinthehole', methods=['OPTIONS', 'POST', 'GET'])
@crossdomain(origin='*')
def regist_test():
    global c, ml
    result = list()
    if request.method == "POST":
        data = request.get_json()
        l = data["elements"]
        lt = [ml[t]["title"] for t in l]
        count = Counter(lt)
        if "圆周角定理推论" in lt:
            if "AC是圆O直径" in lt:
                co = min([count["AC是圆O直径"]])
                c += 1
                r = {"id": str(c), "title": "∠ADC=90°", "canBeForged": True, "amount": co, "icon": "angle"}
                ml[str(c)] = r
                result.append(r)
        if "等腰三角形性质" in lt:
            if "AB=AC" in lt and "∠ADC=90°" in lt:
                co = min([count["AB=AC"], count["∠ADC=90°"]])
                c += 1
                r = {"id": str(c), "title": "CD=DB", "canBeForged": False, "amount": co, "icon": "line"}
                ml[str(c)] = r
                result.append(r)
        if "三角形中位线定义" in lt:
            if "CD=DB" in lt and "CO=OA" in lt:
                co = min([count["CD=DB"], count["CO=OA"]])
                c += 1
                r = {"id": str(c), "title": "OD是△ABC中位线", "canBeForged": False, "amount": co, "icon": "tran"}
                ml[str(c)] = r
                result.append(r)
        if "三角形中位线定理" in lt:
            if "OD是△ABC中位线" in lt:
                co = min([count["OD是△ABC中位线"]])
                c += 1
                r = {"id": str(c), "title": "OD∥AB", "isGoal": True, "canBeForged": False, "amount": co, "icon": "line"}
                result.append(r)
    return jsonify(result)


@app.route('/result',methods=['OPTIONS', 'GET'])
@crossdomain(origin="*")
def result():
    return jsonify([
        "∵ AC为○O直径",
        "∴ ∠ADC = 90°",
        # "∵ AB = AC, ∠ADC = 90°",
        # "∴ CD = DB",
        # "∵ AC为○O直径",
        # "∴ CO = OA",
        # "∵ CD = DB, CO = OA",
        # "∴ OD是△CAB中位线",
        # "∴ OD ∥ AB"
    ])


if __name__ == "__main__":
    app.run(host='0.0.0.0')
