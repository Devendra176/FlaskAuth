from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask.globals import current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .methods import add_video_file, wifi_qr, ExtractText
import os
from .models import User
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/get_audio')
@login_required
def get_audio():
    return render_template('get_audio.html')

@main.route('/get_wifi_qr')
@login_required
def get_wifi_qr():
    return render_template('get_wifi_qr.html')


@main.route('/get-text')
@login_required
def get_text():
    return render_template('extract_text.html')


@main.route('/update/profile')
@login_required
def update_profile():
    return render_template('update_profile.html', name=current_user.name)


@main.route('/update/profile', methods=['POST'])
@login_required
def update_profile_post():
    old_pass = request.form.get('old_password')
    new_pass = request.form.get('new_password')
    user = User.query.filter_by(email=current_user.email)
    if not check_password_hash(current_user.password, old_pass):
        flash('Please enter correct password')
        return redirect(url_for('main.update_profile_post'))
    user.password = new_pass
    user.update(
        {'password': generate_password_hash(new_pass, method='sha256')})
    db.session.commit()
    db.session.close()
    flash('Password changed')
    return redirect(url_for('main.profile'))


@main.route('/download/auido',methods=['POST'])
@login_required
def download():
    t = datetime.now()
    file_name = request.files["file_name"]
    file_ = file_name.filename.replace(" ", "_")
    file , extension = os.path.splitext(file_)
    new_name = "_".join([file,t.strftime('%s'),extension])
    file_name.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_name))
    add_video = add_video_file(filename = os.path.join(current_app.config['UPLOAD_FOLDER'], new_name), Out_path = current_app.config['DOWNLOAD_FOLDER'], new_file_name = new_name)
    return jsonify(add_video)


@main.route('/download/wifi_qr',methods=['POST'])
@login_required
def get_wifi_qr_post():
    status = {}
    wifi_name = request.form.get('wifi_name')
    hid = request.form.get('hid')
    hid = True if hid == 'true' else False
    password = request.form.get('password')
    encryption = request.form.get('encryption')
    genrate = wifi_qr(wifi_name=wifi_name,hidden=hid,encryption=encryption,password=password,destination=current_app.config['WIFI_FOLDER'])
    if genrate['status']:
        status = {'status':genrate['status'],'output':genrate['output'].split('login_project')[1],'file_name':genrate['file_name']}
    else:
        status = {'status':genrate['status']}
    return jsonify(status)

@main.route('/get-text/extract-text',methods=['POST'])
@login_required
def get_text_post():
    status = {}
    t = datetime.now()
    file_name = request.files["file_name"]
    file_ = file_name.filename.replace(" ", "_")
    file , extension = os.path.splitext(file_)
    new_name = "_".join([file,t.strftime('%s'),extension])
    file_name.save(os.path.join(current_app.config['EXTRACT_FOLDER_RAW'], new_name)) 
    eT = ExtractText()
    output = eT.get_image(os.path.join(current_app.config['EXTRACT_FOLDER_RAW'], new_name), output_path=current_app.config['EXTRACT_FOLDER_OUTPUT'],file_name=new_name)
    if output['status']:
        status ={'status':output['status'],'result':output['output'],'filename':output['out_filename'].split('login_project')[1]}
    else:
        status = {'status':output['status']}
    return jsonify(status)