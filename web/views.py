﻿# flask server
# Author : minku Koo
# Project Start:: 2021.03.10
# Last Modified from Ji-yong 2021.06.11

from flask import Flask, request, render_template, jsonify, Blueprint, redirect, url_for, session, current_app
import os

import logging
from static.db import control_sql
from raspberry import rasp_control

views = Blueprint("server", __name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@views.route("/", methods=["GET"])
def index():
    if "id" not in session:
        # session["id"] = get_job_id()
        pass
    
    return render_template("index.html")

@views.route("/login", methods=["GET"])
def login():
    if "id" not in session:
        # session["id"] = get_job_id()
        pass
    
    return render_template("login.html")

@views.route("/join", methods=["GET"])
def join():
    id = request.form["ID"]
    pw = request.files["pass"]
    pwc = request.files["passck"]
    phone = request.files["PHONE"]
    b_type = request.files["kinds"]
    b_name = request.files["store"]
    
    
    
    if "id" not in session:
        session["id"] = get_job_id()
        pass
    
    return render_template("index.html")

@views.route("/regist", methods=["GET"])
def regist():
    return render_template("regist.html")


@views.route("/check_label", methods=["POST"])
def check_label():
    label_code = request.form["tcodext"]
    label_img = request.files["img"]

    print(f'label_text : {label_code}')
    print(f'label_img : {label_img.filename}')

    is_label_code = label_code == ""
    is_label_img = label_img.filename == ""


    if is_label_code:
        pass

    elif is_label_img:
        pass

    else:
        print("아무것도 안올림 에러")

    # 이미지 업로드 안했을 때
    if label_img.filename == "":
        pass

    return jsonify(data="success")
    
@views.route("/map", methods=["GET"])
def map():
    if "id" not in session:
        # session["id"] = get_job_id()
        pass
    
    return render_template("map.html")
    
@views.route("/grade", methods=["GET"])
def grade():
    if "id" not in session:
        # session["id"] = get_job_id()
        pass
    
    return render_template("grade.html")

@views.route("/check_grade", methods=["GET", "POST"])
def check_grade():
    if request.method == "GET":
        if "id" not in session:
            # session["id"] = get_job_id()
            pass

    elif request.method == "POST":
        rasp_control.shot_cam()
        rasp_control.get_img()
        return jsonify(data="success")
        
    return render_template("check_grade.html")

@views.route("/uploadIMG", methods=["POST"])
def upload_img():
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('file')

    errors = {}
    success = False
    filepath = None

    for file in files:
        if file:
            # filename = secure_filename(file.filename) # secure_filename은 한글명을 지원하지 않음
            filename = file.filename 
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            filepath = filepath.replace("\\", "/")
            # file_page_path = os.path.splitext(filepath)[0]
            
            # file save (with uploaded)
            file.save(filepath)
            success = True

        else:
            errors[file.filename] = 'File type is not allowed'
    
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 206
        return resp

    # main 
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp

    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp