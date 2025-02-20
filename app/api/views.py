from flask import render_template, request, jsonify, redirect, url_for, abort, current_app, \
    send_from_directory, flash
from flask_login import login_required, current_user
from ..models import db, Role, User, Ion_User, Ion_Wallet, Ion_Obu_List, Subject_Support, Status_Support, Support, Inbox, Ion_Notification_Type, Ion_Notification, Ion_Product_Category, Ion_Obu_Detail, Ion_Upgrade, Ion_Request, Rdb_Transaction_Type
from werkzeug.utils import secure_filename
import pymongo, requests, calendar, os, json
from datetime import datetime
from sqlalchemy import asc, extract
from bson import ObjectId
from .. import mongo, csrf
from ..models_mongo import TransLog, Rapilog
from . import api
from ..utils import user_log, resize_files
import xmlrpc.client, requests, time, ast
from os.path import join, dirname, realpath

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']

# @main.route('/google273b4a5af9f9bf98.html')
# def google():
#     return render_template('google273b4a5af9f9bf98.html')


# ==============================================================================
# SPECIFICS DATA [API]
# ==============================================================================

@api.route('/dashboard', methods=['POST', 'GET'])
@csrf.exempt
def _api_dashboard():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        january = Ion_User.query.filter(extract('month',Ion_User.added_time) == 1).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        february = Ion_User.query.filter(extract('month',Ion_User.added_time) == 2).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        march = Ion_User.query.filter(extract('month',Ion_User.added_time) == 3).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        april = Ion_User.query.filter(extract('month',Ion_User.added_time) == 4).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        may = Ion_User.query.filter(extract('month',Ion_User.added_time) == 5).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        june = Ion_User.query.filter(extract('month',Ion_User.added_time) == 6).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        july = Ion_User.query.filter(extract('month',Ion_User.added_time) == 7).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        august = Ion_User.query.filter(extract('month',Ion_User.added_time) == 8).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        september = Ion_User.query.filter(extract('month',Ion_User.added_time) == 9).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        october = Ion_User.query.filter(extract('month',Ion_User.added_time) == 10).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        november = Ion_User.query.filter(extract('month',Ion_User.added_time) == 11).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        december = Ion_User.query.filter(extract('month',Ion_User.added_time) == 12).filter(extract('year', Ion_User.added_time) == (apidata['year'])).count()
        new_user_month = Ion_User.query.filter(extract('month',Ion_User.added_time) == datetime.now().month).count()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['count_user'] = Ion_User()._count()
                response['total_wallet'] = Ion_Wallet()._total_wallet()
                response['total_wallet_jan'] = Ion_Wallet()._total_wallet_jan(year=(apidata['year']))
                response['total_wallet_feb'] = Ion_Wallet()._total_wallet_feb(year=(apidata['year']))
                response['total_wallet_mar'] = Ion_Wallet()._total_wallet_mar(year=(apidata['year']))
                response['total_wallet_apr'] = Ion_Wallet()._total_wallet_apr(year=(apidata['year']))
                response['total_wallet_may'] = Ion_Wallet()._total_wallet_may(year=(apidata['year']))
                response['total_wallet_jun'] = Ion_Wallet()._total_wallet_jun(year=(apidata['year']))
                response['total_wallet_jul'] = Ion_Wallet()._total_wallet_jul(year=(apidata['year']))
                response['total_wallet_agt'] = Ion_Wallet()._total_wallet_agt(year=(apidata['year']))
                response['total_wallet_sep'] = Ion_Wallet()._total_wallet_sep(year=(apidata['year']))
                response['total_wallet_oct'] = Ion_Wallet()._total_wallet_oct(year=(apidata['year']))
                response['total_wallet_nov'] = Ion_Wallet()._total_wallet_nov(year=(apidata['year']))
                response['total_wallet_des'] = Ion_Wallet()._total_wallet_des(year=(apidata['year']))
                response['january'] = january
                response['february'] = february
                response['march'] = march
                response['april'] = april
                response['may'] = may
                response['june'] = june
                response['july'] = july
                response['august'] = august
                response['september'] = september
                response['october'] = october
                response['november'] = november
                response['december'] = december
                response['new_user_month'] = new_user_month
                response['count_user'] = Ion_User()._count()
                response['total_wallet'] = Ion_Wallet()._total_wallet()
                response['status'] = '00'
                response['list'] = TransLog()._list_highest(apidata['skip'])
                response['message'] = 'Sukses'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))


# THIS IS VIEWS FOR ADMIN PAGE
@api.route('/users', methods=['POST', 'GET'])
@csrf.exempt
def _api_users():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_User()._list(page=int(apidata['page']))
                response['count_user'] = Ion_User()._count()
                response['total_wallet'] = Ion_Wallet()._total_wallet()
                response['total_trx'] = Ion_Wallet()._total_trx()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/users_upgraded', methods=['POST', 'GET'])
@csrf.exempt
def _api_users_upgraded():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Upgrade()._list_upgraded(page=int(apidata['page']))
                response['count_user'] = Ion_User()._count()
                response['total_wallet'] = Ion_Wallet()._total_wallet()
                response['total_trx'] = Ion_Wallet()._total_trx()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/users_suspended', methods=['POST', 'GET'])
@csrf.exempt
def _api_users_suspended():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_User()._list_suspended(page=int(apidata['page']))
                response['count_user'] = Ion_User()._count()
                response['total_wallet'] = Ion_Wallet()._total_wallet()
                response['total_trx'] = Ion_Wallet()._total_trx()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/users_request_upgrade', methods=['POST', 'GET'])
@csrf.exempt
def _api_users_request_upgrade():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Upgrade()._list_request_upgrade(page=int(apidata['page']))
                response['count_user'] = Ion_User()._count()
                response['total_wallet'] = Ion_Wallet()._total_wallet()
                response['total_trx'] = Ion_Wallet()._total_trx()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/userdetail', methods=['POST', 'GET'])
@csrf.exempt
def _api_userdetail():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id_admin']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['id'] = Ion_User()._data(user_id=(apidata['user_id']))
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/upgradedetail', methods=['POST', 'GET'])
@csrf.exempt
def _api_upgradedetail():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id_admin']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Upgrade()._data(apidata['id_upgrade'])
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/obu', methods=['POST', 'GET'])
@csrf.exempt
def _api_obus():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Obu_List()._list_all(page=int(apidata['page']))
                response['count_obu'] = Ion_Obu_List()._count()
                # response['detail'] = Ion_Obu_Detail()._list(apidata['user_id'])
                response['total_wallet'] = Ion_Wallet()._total_wallet()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/obu_show_owned', methods=['POST', 'GET'])
@csrf.exempt
def _api_obus_show_owned():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Obu_List()._list_by_user(page=int(apidata['page']))
                response['count_obu'] = Ion_Obu_List()._count()
                response['total_wallet'] = Ion_Wallet()._total_wallet()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/obu_active', methods=['POST', 'GET'])
@csrf.exempt
def _api_obus_active():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Obu_List()._list_active(page=int(apidata['page']))
                response['count_obu'] = Ion_Obu_List()._count()
                response['total_wallet'] = Ion_Wallet()._total_wallet()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/obu_nonactive', methods=['POST', 'GET'])
@csrf.exempt
def _api_obus_nonactive():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Obu_List()._list_nonactive(page=int(apidata['page']))
                response['count_obu'] = Ion_Obu_List()._count()
                response['total_wallet'] = Ion_Wallet()._total_wallet()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/obudetail', methods=['POST', 'GET'])
@csrf.exempt
def _api_obudetail():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id_admin']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Obu_Detail()._list(obu_id=(apidata['obu_id']))
                response['detail'] = Ion_Obu_List()._data(apidata['obu_id'])
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/obuunitdetail', methods=['POST', 'GET'])
@csrf.exempt
def _api_obuunitdetail():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id_admin']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Obu_Detail()._data(apidata['obu_id'])
                # response['detail'] = Ion_Obu_List()._data(apidata['user_id'])
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/admin', methods=['POST', 'GET'])
@csrf.exempt
def _api_admins():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = User()._list(page=int(apidata['page']))
                response['count_admin'] = User()._count()
                response['admin_detail'] = User()._data(apidata['id'])
                response['status'] ='00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/role', methods=['POST', 'GET'])
@csrf.exempt
def _api_roles():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Role()._list()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/detail', methods=['POST', 'GET'])
@csrf.exempt
def _api_detail():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id_admin']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['id'] = User()._data(_id=(apidata['id']))
                response['status'] = '00'
                response['message'] = 'Sukses'
            elif int(apidata['status']) == 1:
                response['status'] = '00'
                response['message'] = 'Sukses'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/edit_detail', methods=['POST', 'GET'])
@csrf.exempt
def _api_edit_detail():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id_admin']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['id'] = User()._data(_id=(apidata['id']))
                response['status'] = '00'

        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/history', methods=['GET', 'POST'])
@csrf.exempt
def _read_history():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        cur_user = User.query.filter_by(id=apidata['id']).first()
        if cur_user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response = TransLog()._list(apidata['user_id'], apidata['skip'])
                # response = Rapilog()._list(apidata['client_id'], apidata['skip'])
                response['status'] = '00'
                response['message'] = 'Sukses'
            elif int(apidata['status']) == 1:
                response = TransLog()._data(cur_user.id, apidata['_id'])
                response['status'] = '00'
                response['message'] = 'Sukses'
        else:
            response['status'] = '50'
            response['message'] = 'User tidak terverifikasi'
        return jsonify(response)
    return redirect("main.index", code=302)

@api.route('/client_history', methods=['GET', 'POST'])
@csrf.exempt
def _read_client_history():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        cur_user = User.query.filter_by(id=apidata['id']).first()
        if cur_user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response = Rapilog()._list(apidata['client_id'], apidata['skip'])
                response['status'] = '00'
                response['message'] = 'Sukses'
            elif int(apidata['status']) == 1:
                response['data'] = Rapilog()._data(apidata['_obu_uid'], apidata['_id'])
                response['status'] = '00'
                response['message'] = 'Sukses'
        else:
            response['status'] = '50'
            response['message'] = 'User tidak terverifikasi'
        return jsonify(response)
    return redirect("main.index", code=302)

@api.route('/trx_log', methods=['GET', 'POST'])
@csrf.exempt
def _trx_log():
    if request.method == 'POST':
        response = {}
        apidata = request.form
        cur_user = User.query.filter_by(id=apidata['id']).first()
        if cur_user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response = TransLog()._list_all(apidata['skip'])
                response['status'] = '00'
                response['message'] = 'Sukses'
            elif int(apidata['status']) == 1:
                response['data'] = TransLog()._data_all(apidata['_id'])
                response['status'] = '00'
                response['message'] = 'Sukses'
        else:
            response['status'] = '50'
            response['message'] = 'User tidak terverifikasi'
        return jsonify(response)
    return redirect("main.index", code=302)
############################################################################


# THIS IS VIEWS FOR SUPPORT PAGE

@api.route('/subject_support', methods=['POST', 'GET'])
@csrf.exempt
def _api_subject_support():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Subject_Support()._list()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/support', methods=['POST', 'GET'])
@csrf.exempt
def _api_supports():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Support()._list(page=int(apidata['page']))
                response['count_support'] = Support()._count()
                # response['support_detail'] = Support()._data(apidata['id'])
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/support_detail', methods=['POST', 'GET'])
@csrf.exempt
def _api_support_detail():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id_admin']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['id'] = Support()._data(_id=(apidata['id']))
                response['status'] = '00'

        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))


@api.route('/add_message', methods=['GET', 'POST'])
@csrf.exempt
def _add_message():
    if request.method == "POST":
        response = {}
        apidata = request.files
        cur_user = User.query.filter_by(id=apidata['id'].filename).first()
        if cur_user.verify_token(apidata['token'].filename):
            # stored_file = resize_files(cur_user.id, apidata['image'])
            Inbox()._insert(apidata['subject'].filename,apidata['content'].filename,'inbox.png',apidata['link'].filename,apidata['product_cat'].filename,apidata['image'].filename)
            response['status'] = '00'
            response['messages'] = 'success'
        else:
            response['status'] = '50'
            response['messages'] = 'user tidak terverifikasi'
        return jsonify(response)
    return redirect(url_for('main.index'))

@api.route('/sent_message', methods=['POST', 'GET'])
@csrf.exempt
def _api_sent_message():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print("apidata")
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Inbox()._list(page=int(apidata['page']))
                response['count_message'] = Inbox()._count()
                response['status'] ='00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/trash_message', methods=['POST', 'GET'])
@csrf.exempt
def _api_trash_message():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        notif_type = Ion_Notification_Type.query.filter_by(id=2).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Inbox()._trash_list(page=int(apidata['page']))
                response['count_message'] = Inbox()._count()
                response['status'] ='00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/message_category', methods=['POST', 'GET'])
@csrf.exempt
def _api_message_category():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Product_Category()._list()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))


@api.route('/request_log', methods=['POST', 'GET'])
@csrf.exempt
def _api_request_log():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_Request()._list(page=int(apidata['page']))
                response['count_request'] = Ion_Request()._count()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/bujt', methods=['POST', 'GET'])
@csrf.exempt
def _api_bujt():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Ion_User()._list_bujt(page=int(apidata['page']))
                response['count_user'] = Ion_User()._count()
                response['total_wallet'] = Ion_Wallet()._total_wallet_client()
                response['total_trx'] = Rapilog()._count()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))

@api.route('/trxtype', methods=['POST', 'GET'])
@csrf.exempt
def _api_trxtype():
    # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
    # user_log('/', ip_list)
    if request.method == 'POST':
        apidata = request.form
        app = current_app._get_current_object()
        print(apidata)
        response = {}
        user = User.query.filter_by(id=apidata['id']).first()
        if user is not None and user.verify_token(apidata['token']):
            if int(apidata['status']) == 0:
                response['data'] = Rdb_Transaction_Type()._list()
                response['status'] = '00'
        else:
            response['status'] = '50'
            response['message'] = 'Your credential are invalid.'
        return jsonify(response)
    else:
        return redirect(url_for('main.index'))
# """
# route: /api/v1/ams/sector
# bertujuan untuk read/write data sector dari website ini.
# """
# @admin.route('/api/v1/ams/dashboard', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_dashboard():
#     # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
#     # user_log('/', ip_list)
#     if request.method == 'POST':
#         apidata = request.form
#         print(apidata)
#         response = {}
#         user = User.query.filter_by(id=apidata['id']).first()
#         if user is not None and user.verify_token(token=apidata['token']):
#             sector_id = None
#             if int(apidata['sector_id']) != 0:
#                 sector_id = int(apidata['sector_id'])
#             if int(apidata['status']) == 0:
#                 response['jumbo_list'] = home_jumbotron().jumbo_list(sector_id)
#                 response['home_title'] = home_title()._data(sector_id)
#                 response['home_about'] = about_db()._find_one(sector_id)
#                 response['status'] = '00'
#             # HOME JUMBOTRON
#             elif int(apidata['status']) == 1:
#                 response['data'] = gallery()._list(sector_id)
#                 response['jumbo_list'] = home_jumbotron().jumbo_list(sector_id)
#                 response['status'] = '00'
#             elif int(apidata['status']) == 2:
#                 if len(apidata['id'].strip()) > 0:
#                     data = ast.literal_eval(apidata['list'])
#                     for i in home_jumbotron.query.filter_by(sector_id=sector_id, status=True).all():
#                         i.status = False
#                         db.session.add(i)
#                         db.session.commit()
#                     for i in data:
#                         jumbo = home_jumbotron()
#                         jumbo.gallery_id = int(i['id'])
#                         jumbo.sector_id = sector_id
#                         db.session.add(jumbo)
#                         db.session.commit()
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 3:
#                 if len(apidata['id'].strip()) > 0 and len(apidata['short_desc'].strip()) > 0:
#                     mongo.db.home.update_one({
#                         '_id': ObjectId(apidata['id']),
#                         'sector_id': sector_id
#                     },{
#                         '$set': {
#                             'short_desc': apidata['short_desc']
#                         }
#                     })
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             # HOME TITLE
#             elif int(apidata['status']) == 4:
#                 response['data'] = home_title()._data(sector_id)
#                 response['status'] = '00'
#             elif int(apidata['status']) == 5:
#                 if len(apidata['id'].strip()) > 0:
#                     for i in home_title.query.filter_by(sector_id=sector_id, status=True).all():
#                         i.status = False
#                         db.session.add(i)
#                         db.session.commit()
#                     _title = home_title()
#                     _title.title = apidata['title'] if len(apidata['title'].strip()) > 0 else None
#                     _title.subtitle = apidata['subtitle'] if len(apidata['subtitle'].strip()) > 0 else None
#                     _title.sector_id = sector_id
#                     db.session.add(_title)
#                     db.session.commit()
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             # HOME ABOUT
#             elif int(apidata['status']) ==6:
#                 response['data'] = about_db()._find_one(sector_id)
#                 response['status'] = '00'
#             elif int(apidata['status']) == 7:
#                 if len(apidata['id'].strip()) > 0:
#                     about_db()._insert(sector_id, apidata['content'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))
#
# @admin.route('/api/v1/ams/news', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_news():
#     # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
#     # user_log('/', ip_list)
#     if request.method == 'POST':
#         apidata = request.form
#         response = {}
#         user = User.query.filter_by(id=apidata['id']).first()
#         print(apidata)
#         if user is not None and user.verify_token(token=apidata['token']):
#             sector_id = None
#             if int(apidata['sector_id']) != 0:
#                 sector_id = int(apidata['sector_id'])
#             if int(apidata['status']) == 0:
#                 response['data'] = news_db()._news_list(sector_id=sector_id, page=int(apidata['page']))
#                 response['count'] = news_db()._count(sector_id=sector_id, page=int(apidata['page']))
#                 response['status'] = '00'
#             elif int(apidata['status']) == 1:
#                 if len(apidata['title'].strip()) > 0 and len(apidata['summary'].strip()) > 0 \
#                         and len(apidata['content'].strip()) > 0:
#                     response['data'] = news_db()._insert(apidata['title'], apidata['summary'], apidata['content'], sector_id)
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 2:
#                 if len(apidata['id'].strip()) > 0:
#
#                     response['data'] = news_db()._find_one(sector_id, apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 3:
#                 if len(apidata['id'].strip()) > 0 and len(apidata['title'].strip()) > 0 and len(apidata['summary'].strip()) > 0 \
#                         and len(apidata['content'].strip()) > 0:
#                     _thumbnail = None
#                     if len(apidata['thumbnail']) > 0:
#                         _thumbnail = apidata['thumbnail']
#                     response['data'] = news_db()._update(sector_id, apidata['_id'], apidata['title'], apidata['summary'], apidata['content'], _thumbnail)
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 4:
#                 if len(apidata['id'].strip()) > 0:
#                     response['data'] = news_db()._remove(sector_id, apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))
#
# @admin.route('/api/v1/ams/sosialisasi', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_sosialisasi():
#     # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
#     # user_log('/', ip_list)
#     if request.method == 'POST':
#         apidata = request.form
#         response = {}
#         user = User.query.filter_by(id=apidata['id']).first()
#         print(apidata)
#         if user is not None and user.verify_token(token=apidata['token']):
#             sector_id = None
#             if int(apidata['sector_id']) != 0:
#                 sector_id = int(apidata['sector_id'])
#             if int(apidata['status']) == 0:
#                 response['data'] = sosialisasi_db()._list(sector_id)
#                 response['status'] = '00'
#             elif int(apidata['status']) == 1:
#                 if len(apidata['date'].strip()) > 0 and len(apidata['activity'].strip()) > 0 \
#                         and len(apidata['lembaga'].strip()) > 0 and len(apidata['speaker'].strip()) > 0 \
#                         and len(apidata['location'].strip()) > 0:
#                     response['data'] = sosialisasi_db()._insert(apidata['date'], apidata['activity'], apidata['lembaga'], apidata['speaker'], apidata['location'], apidata['description'], sector_id)
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 2:
#                 if len(apidata['id'].strip()) > 0:
#                     response['data'] = sosialisasi_db()._data(sector_id, apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 3:
#                 if len(apidata['id'].strip()) > 0 and len(apidata['date'].strip()) > 0 and \
#                     len(apidata['activity'].strip()) > 0 and len(apidata['lembaga'].strip()) > 0 and \
#                     len(apidata['speaker'].strip()) > 0 and len(apidata['location'].strip()) > 0:
#                     _thumbnail = None
#                     if len(apidata['thumbnail']) > 0:
#                         _thumbnail = apidata['thumbnail']
#                     response['data'] = sosialisasi_db()._update(sector_id, apidata['_id'], apidata['date'], apidata['activity'], apidata['lembaga'], apidata['speaker'], apidata['location'], apidata['description'], _thumbnail)
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 4:
#                 if len(apidata['id'].strip()) > 0:
#                     response['data'] = sosialisasi_db()._remove(sector_id, apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))
#
# @admin.route('/api/v1/ams/dpo', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_dpo():
#     # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
#     # user_log('/', ip_list)
#     if request.method == 'POST':
#         apidata = request.form
#         response = {}
#         user = User.query.filter_by(id=apidata['id']).first()
#         print(apidata)
#         if user is not None and user.verify_token(token=apidata['token']):
#             if int(apidata['status']) == 0:
#                 response['data'] = dpo()._list()
#                 response['status'] = '00'
#             elif int(apidata['status']) == 1:
#                 if len(apidata['name'].strip()) > 0 and len(apidata['case'].strip()) > 0 \
#                         and len(apidata['description'].strip()) > 0:
#                     _gender = True
#                     if int(apidata['gender'])  == 0:
#                         _gender = False
#                     response['data'] = dpo()._insert(apidata['name'], apidata['birth_place'], \
#                         apidata['birth_date'], _gender, apidata['nationality'], \
#                         apidata['religion'], apidata['address'], apidata['job'],\
#                         apidata['short_case'], apidata['case'], apidata['description'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 2:
#                 if len(apidata['_id'].strip()) > 0:
#                     response['data'] = dpo()._data(apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 3:
#                 if len(apidata['_id'].strip()) > 0 and len(apidata['name'].strip()) > 0 and len(apidata['case'].strip()) > 0 \
#                         and len(apidata['description'].strip()) > 0:
#                     _image = None
#                     if len(apidata['image']) > 0:
#                         _image = apidata['image']
#                     _gender = True
#                     if int(apidata['gender'])  == 0:
#                         _gender = False
#                     response['data'] = dpo()._update(apidata['_id'], apidata['name'], apidata['birth_place'], \
#                         apidata['birth_date'], _gender, apidata['nationality'], \
#                         apidata['religion'], apidata['address'], apidata['job'],\
#                         apidata['short_case'], apidata['case'], apidata['description'], \
#                         _image)
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 4:
#                 if len(apidata['id'].strip()) > 0:
#                     response['data'] = dpo()._remove(apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))
#
# @admin.route('/api/v1/ams/posko', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_posko():
#     # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
#     # user_log('/', ip_list)
#     if request.method == 'POST':
#         apidata = request.form
#         response = {}
#         user = User.query.filter_by(id=apidata['id']).first()
#         print(apidata)
#         if user is not None and user.verify_token(token=apidata['token']):
#             if int(apidata['status']) == 0:
#                 response['data'] = posko()._list()
#                 response['status'] = '00'
#             elif int(apidata['status']) == 1:
#                 if len(apidata['name'].strip()) > 0 and len(apidata['unit_kerja'].strip()) > 0 \
#                     and len(apidata['location'].strip()) > 0:
#                     _gender = True
#                     koor = requests.get(
#                             "https://maps.google.com/maps/api/geocode/json?address=" + apidata['location'] + "&sensor=false&key=AIzaSyA_PMy05-8LxBhgPL_14IY0B4XbSLqaUBo").json()
#                     if koor['status'] == 'OK':
#                         lat = koor['results'][0]['geometry']['location']['lat']
#                         lng = koor['results'][0]['geometry']['location']['lng']
#                         response['data'] = posko()._insert(apidata['name'], \
#                             apidata['area'], apidata['unit_kerja'], apidata['location'], \
#                             lat, lng, user.id)
#                         response['status'] = '00'
#                     else:
#                         response['status'] = '50'
#                         response['message'] = 'Lokasi yang anda cari tidak ditemukan.'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 2:
#                 if len(apidata['_id'].strip()) > 0:
#                     response['data'] = posko()._data(apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 3:
#                 if len(apidata['_id'].strip()) > 0 and len(apidata['name'].strip()) > 0 and len(apidata['unit_kerja'].strip()) > 0 \
#                         and len(apidata['location'].strip()) > 0:
#                     koor = requests.get(
#                             "https://maps.google.com/maps/api/geocode/json?address=" + apidata['location'] + "&sensor=false&key=AIzaSyA_PMy05-8LxBhgPL_14IY0B4XbSLqaUBo").json()
#                     if koor['status'] == 'OK':
#                         _image = None
#                         if len(apidata['image']) > 0:
#                             _image = apidata['image']
#                         lat = koor['results'][0]['geometry']['location']['lat']
#                         lng = koor['results'][0]['geometry']['location']['lng']
#                         response['data'] = posko()._update(apidata['_id'], apidata['name'], apidata['area'], \
#                             apidata['unit_kerja'], apidata['location'], \
#                             _image, lat, lng, user.id)
#                         response['status'] = '00'
#                     else:
#                         response['status'] = '50'
#                         response['message'] = 'Lokasi yang anda cari tidak ditemukan.'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 4:
#                 if len(apidata['id'].strip()) > 0:
#                     response['data'] = posko()._remove(apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))
#
# @admin.route('/api/v1/ams/kinerja', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_kinerja():
#     if request.method == 'POST':
#         apidata = request.form
#         app = current_app._get_current_object()
#         print(apidata)
#         response = {}
#         user = User.query.filter_by(id=int(apidata['id'])).first()
#         if user is not None:
#             if user.verify_token(apidata['token']):
#                 if apidata['sector'] == 'tp4p':
#                     if int(apidata['status']) == 0:
#                         response['data'] = kinerja_tp4p()._list()
#                         response['year_list'] = [i for i in reversed(range(1965, int(datetime.now().year) + 1))]
#                         response['status'] = '00'
#                     elif int(apidata['status']) == 1:
#                         if len(apidata['year'].strip()) > 0 and len(apidata['instansi'].strip()) > 0 \
#                             and len(apidata['description'].strip()) > 0 and len(apidata['anggaran'].strip()) > 0:
#                             response['data'] = kinerja_tp4p()._insert(apidata['year'], apidata['instansi'], \
#                                 apidata['anggaran'], apidata['description'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 2:
#                         if len(apidata['_id'].strip()) > 0:
#                             response['data'] = kinerja_tp4p()._data(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                     elif int(apidata['status']) == 3:
#                         if len(apidata['_id'].strip()) > 0 and len(apidata['year'].strip()) > 0 and len(apidata['instansi'].strip()) > 0 \
#                                 and len(apidata['anggaran'].strip()) > 0 and len(apidata['description'].strip()) > 0:
#                             response['data'] = kinerja_tp4p()._update(apidata['_id'], apidata['year'], apidata['instansi'], \
#                                 apidata['anggaran'], apidata['description'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 4:
#                         if len(apidata['id'].strip()) > 0:
#                             response['data'] = kinerja_tp4p()._remove(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                 elif apidata['sector'] == 'tp4d':
#                     if int(apidata['status']) == 0:
#                         print('test')
#                         response['data'] = kinerja_tp4d()._list()
#                         response['year_list'] = [i for i in reversed(range(1965, int(datetime.now().year) + 1))]
#                         response['month_list'] = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
#                                               'August', 'September', 'October', 'November', 'December']
#                         response['kejati'] = [{'id': i.id, 'name': i.name} for i in Kejati.query.filter_by(status=True).all()]
#                         response['status'] = '00'
#                     elif int(apidata['status']) == 1:
#                         if len(apidata['year'].strip()) > 0 and len(apidata['month_1'].strip()) > 0 \
#                             and len(apidata['month_2'].strip()) > 0:
#                             response['data'] = kinerja_tp4d()._insert(apidata['year'], apidata['month_1'], \
#                                 apidata['month_2'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 2:
#                         if len(apidata['_id'].strip()) > 0:
#                             response['data'] = kinerja_tp4d()._data(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                     elif int(apidata['status']) == 3:
#                         if len(apidata['_id'].strip()) > 0 and len(apidata['month_1'].strip()) > 0 and len(apidata['month_2'].strip()) > 0 \
#                             and len(apidata['year'].strip()) > 0:
#                             response['data'] = kinerja_tp4d()._update(apidata['_id'], apidata['year'], apidata['month_1'], \
#                                 apidata['month_2'], apidata['instansi'], apidata['kegiatan'], apidata['anggaran'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 4:
#                         if len(apidata['id'].strip()) > 0:
#                             response['data'] = kinerja_tp4d()._remove(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                 elif apidata['sector'] == 'tabur':
#                     if int(apidata['status']) == 0:
#                         print('test')
#                         response['data'] = tabur()._list()
#                         response['status'] = '00'
#                     elif int(apidata['status']) == 1:
#                         if len(apidata['mail_no'].strip()) > 0 and len(apidata['mail_date'].strip()) > 0 \
#                             and len(apidata['source'].strip()) > 0 and len(apidata['name'].strip()) > 0 \
#                             and len(apidata['origin'].strip()) > 0 and len(apidata['description'].strip()) > 0:
#                             response['data'] = tabur()._insert(apidata['mail_no'], \
#                                 apidata['mail_date'], apidata['source'], \
#                                 apidata['name'], apidata['origin'], apidata['place_tangkap'], \
#                                 apidata['date_tangkap'], apidata['description'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 2:
#                         if len(apidata['_id'].strip()) > 0:
#                             response['data'] = tabur()._data(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                     elif int(apidata['status']) == 3:
#                         if len(apidata['_id'].strip()) > 0 and len(apidata['mail_date'].strip()) > 0\
#                             and len(apidata['source'].strip()) > 0 and len(apidata['name'].strip()) > 0 \
#                             and len(apidata['origin'].strip()) > 0 and len(apidata['description'].strip()):
#                             response['data'] = tabur()._update(apidata['_id'], apidata['image'], \
#                                 apidata['mail_no'], apidata['mail_date'], apidata['source'], \
#                                 apidata['name'], apidata['origin'], apidata['place_tangkap'], \
#                                 apidata['date_tangkap'], apidata['description'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 4:
#                         if len(apidata['id'].strip()) > 0:
#                             response['data'] = tabur()._remove(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                 elif apidata['sector'] == 'barcet':
#                     if int(apidata['status']) == 0:
#                         print('test')
#                         response['data'] = kinerja_barcet()._list()
#                         response['status'] = '00'
#                     elif int(apidata['status']) == 1:
#                         if len(apidata['name'].strip()) > 0 and len(apidata['type'].strip()) > 0:
#                             response['data'] = kinerja_barcet()._insert(apidata['name'], \
#                                 apidata['type'], apidata['description'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 2:
#                         if len(apidata['_id'].strip()) > 0:
#                             response['data'] = kinerja_barcet()._data(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                     elif int(apidata['status']) == 3:
#                         if len(apidata['_id'].strip()) > 0 and len(apidata['name'].strip()) > 0\
#                             and len(apidata['type'].strip()) > 0:
#                             response['data'] = kinerja_barcet()._update(apidata['_id'], apidata['image'], \
#                                 apidata['name'], apidata['type'], apidata['description'], ast.literal_eval(apidata['data_list']))
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 4:
#                         if len(apidata['id'].strip()) > 0:
#                             response['data'] = kinerja_barcet()._remove(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                 elif apidata['sector'] == 'cekal':
#                     if int(apidata['status']) == 0:
#                         print('test')
#                         response['data'] = kinerja_cekal()._list()
#                         response['year_list'] = [i for i in reversed(range(1965, int(datetime.now().year) + 1))]
#                         response['month_list'] = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
#                                               'August', 'September', 'October', 'November', 'December']
#                         response['kejati'] = [{'id': i.id, 'name': i.name} for i in Kejati.query.filter_by(status=True).all()]
#                         response['status'] = '00'
#                     elif int(apidata['status']) == 1:
#                         if len(apidata['year'].strip()) > 0 and len(apidata['month'].strip()) > 0:
#                             response['data'] = kinerja_cekal()._insert(
#                                 apidata['month'], apidata['year'], apidata['cegah_kejagung'], \
#                                 apidata['cegah_kejati'], apidata['cegah_polri'], apidata['cegah_other'], \
#                                 apidata['panjang_kejagung'], apidata['panjang_kejati'], apidata['panjang_polri'], \
#                                 apidata['panjang_other'], apidata['cabut_kejagung'], apidata['cabut_kejati'], \
#                                 apidata['cabut_polri'], apidata['cabut_other'], apidata['akhir_kejagung'], \
#                                 apidata['akhir_kejati'], apidata['akhir_polri'], apidata['akhir_other']
#                             )
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 2:
#                         if len(apidata['_id'].strip()) > 0:
#                             response['data'] = kinerja_cekal()._data(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                     elif int(apidata['status']) == 3:
#                         if len(apidata['_id'].strip()) > 0 and len(apidata['year'].strip()) > 0 and len(apidata['month'].strip()) > 0:
#                             response['data'] = kinerja_cekal()._update( apidata['_id'], \
#                                 apidata['month'], apidata['year'], apidata['cegah_kejagung'], \
#                                 apidata['cegah_kejati'], apidata['cegah_polri'], apidata['cegah_other'], \
#                                 apidata['panjang_kejagung'], apidata['panjang_kejati'], apidata['panjang_polri'], \
#                                 apidata['panjang_other'], apidata['cabut_kejagung'], apidata['cabut_kejati'], \
#                                 apidata['cabut_polri'], apidata['cabut_other'], apidata['akhir_kejagung'], \
#                                 apidata['akhir_kejati'], apidata['akhir_polri'], apidata['akhir_other']
#                             )
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 4:
#                         if len(apidata['id'].strip()) > 0:
#                             response['data'] = kinerja_cekal()._remove(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                 elif apidata['sector'] == 'pora':
#                     if int(apidata['status']) == 0:
#                         print('test')
#                         response['data'] = kinerja_pora()._list()
#                         response['year_list'] = [i for i in reversed(range(1965, int(datetime.now().year) + 1))]
#                         response['month_list'] = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
#                                               'August', 'September', 'October', 'November', 'December']
#                         response['kejati'] = [{'id': i.id, 'name': i.name} for i in Kejati.query.filter_by(status=True).all()]
#                         response['status'] = '00'
#                     elif int(apidata['status']) == 1:
#                         if len(apidata['year'].strip()) > 0 and len(apidata['month'].strip()) > 0:
#                             response['data'] = kinerja_pora()._insert(apidata['year'], apidata['month'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 2:
#                         if len(apidata['_id'].strip()) > 0:
#                             response['data'] = kinerja_pora()._data(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                     elif int(apidata['status']) == 3:
#                         if len(apidata['_id'].strip()) > 0 and len(apidata['month'].strip()) > 0 \
#                             and len(apidata['year'].strip()) > 0:
#                             response['data'] = kinerja_pora()._update(apidata['_id'], \
#                                 apidata['month'], apidata['year'], \
#                                 apidata['oap'], apidata['tka'], apidata['student'], \
#                                 apidata['researcher'], apidata['family'], \
#                                 apidata['other'], apidata['illegal'], apidata['usaha'], \
#                                 apidata['sosbud'], apidata['wisata'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 4:
#                         if len(apidata['id'].strip()) > 0:
#                             response['data'] = kinerja_pora()._remove(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))
#
# @admin.route('/api/v1/ams/pakem', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_pakem():
#     if request.method == 'POST':
#         apidata = request.form
#         app = current_app._get_current_object()
#         print(apidata)
#         response = {}
#         user = User.query.filter_by(id=int(apidata['id'])).first()
#         if user is not None:
#             if user.verify_token(apidata['token']):
#                 if apidata['sector'] == 'data':
#                     if int(apidata['status']) == 0:
#                         response['data'] = pakem_data()._list()
#                         response['year_list'] = [i for i in reversed(range(1965, int(datetime.now().year) + 1))]
#                         response['status'] = '00'
#                     elif int(apidata['status']) == 1:
#                         print('haha')
#                         if len(apidata['name'].strip()) > 0 and len(apidata['invent'].strip()) > 0 \
#                             and len(apidata['jw'].strip()) > 0 and len(apidata['address_1'].strip()) > 0 \
#                             and len(apidata['current_status'].strip()) > 0:
#                             if len(apidata['address_1'].strip()) > 0:
#                                 koor = requests.get(
#                                         "https://maps.google.com/maps/api/geocode/json?address=" + apidata['address_1'] + "&sensor=false&key=AIzaSyA_PMy05-8LxBhgPL_14IY0B4XbSLqaUBo").json()
#                                 if koor['status'] == 'OK':
#                                     lat = koor['results'][0]['geometry']['location']['lat']
#                                     lng = koor['results'][0]['geometry']['location']['lng']
#                                     response['data'] = pakem_data()._insert(apidata['name'],
#                                     apidata['invent'], apidata['jw'], apidata['current_status'],
#                                     apidata['data_sector'], apidata['address_1'],
#                                     apidata['address_2'], apidata['phone_1'],
#                                     apidata['phone_2'], apidata['phone_3'], apidata['phone_4'],
#                                     apidata['phone_5'], apidata['email_1'], apidata['email_2'],
#                                     apidata['website'], apidata['ss'], apidata['p'],
#                                     apidata['k'], apidata['s'], apidata['b'],
#                                     apidata['description'], lat, lng)
#                                     response['status'] = '00'
#                                 else:
#                                     response['status'] = '50'
#                                     response['message'] = 'Lokasi yang anda masukkan tidak ditemukan.'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 2:
#                         if len(apidata['_id'].strip()) > 0:
#                             response['data'] = pakem_data()._data(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                     elif int(apidata['status']) == 3:
#                         if len(apidata['name'].strip()) > 0 and len(apidata['invent'].strip()) > 0 \
#                             and len(apidata['jw'].strip()) > 0 and len(apidata['address_1'].strip()) > 0 \
#                             and len(apidata['current_status'].strip()) > 0 and len(apidata['_id'].strip()) > 0:
#                             if len(apidata['address_1'].strip()) > 0:
#                                 koor = requests.get(
#                                         "https://maps.google.com/maps/api/geocode/json?address=" + apidata['address_1'] + "&sensor=false&key=AIzaSyA_PMy05-8LxBhgPL_14IY0B4XbSLqaUBo").json()
#                                 if koor['status'] == 'OK':
#                                     lat = koor['results'][0]['geometry']['location']['lat']
#                                     lng = koor['results'][0]['geometry']['location']['lng']
#                                     response['data'] = pakem_data()._update(apidata['_id'], apidata['name'],
#                                     apidata['invent'], apidata['jw'], apidata['current_status'],
#                                     apidata['data_sector'], apidata['address_1'],
#                                     apidata['address_2'], apidata['phone_1'],
#                                     apidata['phone_2'], apidata['phone_3'], apidata['phone_4'],
#                                     apidata['phone_5'], apidata['email_1'], apidata['email_2'],
#                                     apidata['website'], apidata['ss'], apidata['p'],
#                                     apidata['k'], apidata['s'], apidata['b'],
#                                     apidata['description'], apidata['image'], lat, lng)
#                                     response['status'] = '00'
#                                 else:
#                                     response['status'] = '50'
#                                     response['message'] = 'Lokasi yang anda masukkan tidak ditemukan.'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 4:
#                         if len(apidata['id'].strip()) > 0:
#                             response['data'] = pakem_data()._remove(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                 elif apidata['sector'] == 'ensiklopedia':
#                     if int(apidata['status']) == 0:
#                         response['data'] = pakem_ensiklopedia()._list()
#                         response['category'] = ['tradisi', 'kepercayaan', 'himpunan', 'aliran', 'ajaran', 'perguruan', 'gerakan', 'organisasi', 'istilah', 'tokoh', 'agama', 'paham']
#                         response['status'] = '00'
#                     elif int(apidata['status']) == 1:
#                         print('haha')
#                         if len(apidata['name'].strip()) > 0 and len(apidata['category'].strip()) > 0 \
#                             and len(apidata['author'].strip()) > 0 and len(apidata['description'].strip()) > 0 :
#                                 response['data'] = pakem_ensiklopedia()._insert(apidata['name'],
#                                 apidata['category'], apidata['author'], apidata['description'])
#                                 response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 2:
#                         if len(apidata['_id'].strip()) > 0:
#                             response['data'] = pakem_ensiklopedia()._data(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                     elif int(apidata['status']) == 3:
#                         if len(apidata['name'].strip()) > 0 and len(apidata['category'].strip()) > 0 \
#                             and len(apidata['author'].strip()) > 0 and len(apidata['description'].strip()) > 0 \
#                             and len(apidata['_id'].strip()) > 0:
#                             response['data'] = pakem_ensiklopedia()._update(apidata['_id'],
#                             apidata['name'], apidata['category'], apidata['author'],
#                             apidata['description'], apidata['image'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 4:
#                         if len(apidata['id'].strip()) > 0:
#                             response['data'] = pakem_ensiklopedia()._remove(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                 elif apidata['sector'] == 'bunga-rampai':
#                     if int(apidata['status']) == 0:
#                         print('test')
#                         response['data'] = pakem_bunga_rampai()._list()
#                         response['status'] = '00'
#                     elif int(apidata['status']) == 1:
#                         if len(apidata['name'].strip()) > 0:
#                             response['data'] = pakem_bunga_rampai()._insert(apidata['name'], \
#                                 apidata['description'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 2:
#                         if len(apidata['_id'].strip()) > 0:
#                             response['data'] = pakem_bunga_rampai()._data(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#                     elif int(apidata['status']) == 3:
#                         if len(apidata['_id'].strip()) > 0 and len(apidata['name'].strip()) > 0:
#                             response['data'] = pakem_bunga_rampai()._update(apidata['_id'], apidata['image'], \
#                                 apidata['name'], apidata['description'], ast.literal_eval(apidata['data_list']))
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Isi semua field dengan benar.'
#                     elif int(apidata['status']) == 4:
#                         if len(apidata['id'].strip()) > 0:
#                             response['data'] = pakem_bunga_rampai()._remove(apidata['_id'])
#                             response['status'] = '00'
#                         else:
#                             response['status'] = '50'
#                             response['message'] = 'Your credential are invalid.'
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))
#
# @admin.route('/api/v1/ams/gallery', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_gallery():
#     # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
#     # user_log('/', ip_list)
#     if request.method == 'POST':
#         apidata = request.form
#         app = current_app._get_current_object()
#         print(apidata)
#         response = {}
#         user = User.query.filter_by(id=apidata['id']).first()
#         if user is not None and user.verify_token(apidata['token']):
#             sector_id = None
#             if int(apidata['sector_id']) > 0:
#                 sector_id = int(apidata['sector_id'])
#             if int(apidata['status']) == 0:
#                 print('gallery test')
#                 response['data'] = gallery()._list(sector_id)
#                 response['status'] = '00'
#             elif int(apidata['status']) == 1:
#                 file = request.files['file']
#                 if file is not None:
#                     if file != '' and allowed_file(file.filename):
#                         _save = _save_img(file)
#                         response['data'] = gallery()._insert(user.id, _save['name'], sector_id)
#                         response['status'] = '00'
#                     else:
#                         response['status'] = '50'
#                         response['message'] = 'Masukkan file dengan format jpg/jpeg/png'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 2:
#                 if len(apidata['id'].strip()) > 0:
#                     response['data'] = gallery()._data(apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 3:
#                 if len(apidata['_id'].strip()) > 0:
#                     _status = True if apidata['activity_status'] == 'true' else False
#                     response['data'] = gallery()._update(int(apidata['_id']), apidata['short_description'], apidata['description'], _status)
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 4:
#                 if len(apidata['_id'].strip()) > 0:
#                     _gallery = gallery()._remove(int(apidata['_id']))
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))





# ==============================================================================
# GENERAL DATA [API]
# ==============================================================================

"""
NOTE:
route: /api/v1/ams/general
merupakan api yang bertujuan untuk read/write data admin secara general dipisahkan dengan jenis status,

Contoh data:
-Sector List
-Change password

route: /api/v1/ams/sector
merupakan api yang bertujuan untuk read/write data sector dari website ini.

route: /api/v1/ams/menus
merupakan api yang bertujuan untuk read/write data menu/header di website ini.
"""

# @admin.route('/api/v1/ams/general', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_general():
#     if request.method == 'POST':
#         apidata = request.form
#         app = current_app._get_current_object()
#         print(apidata)
#         response = {}
#         user = User.query.filter_by(id=int(apidata['id'])).first()
#         if user is not None:
#             if user.verify_token(apidata['token']):
#                 if apidata['status'] == 'sector_list':
#                     response['data'] = Sector()._list(apidata['sector_id'])
#                     response['status'] = '00'
#                 elif apidata['status'] == 'change-password':
#                     if user.verify_password(apidata['current_password']):
#                         if apidata['password'] == apidata['verify_password']:
#                             if len(apidata['password'].strip()) >= 8:
#                                 response['data'] = User()._change_password(apidata['id'], apidata['password'])
#                                 response['status'] = '00'
#                             else:
#                                 response['message'] = 'Password yang anda masukan kurang dari 8 karakter.'
#                                 response['status'] = '50'
#                         else:
#                             response['message'] = 'Password yang anda masukan tidak sama.'
#                             response['status'] = '50'
#                     else:
#                         response['status'] = '50'
#                         response['message'] = 'Password yang and masukkan salah.'
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))
#
#
# @admin.route('/api/v1/ams/sector', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_sector():
#     # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
#     # user_log('/', ip_list)
#     if request.method == 'POST':
#         apidata = request.form
#         print(apidata)
#         response = {}
#         user = User.query.filter_by(id=apidata['id']).first()
#         if user is not None and user.verify_token(token=apidata['token']):
#             if int(apidata['status']) == 0:
#                 response['data'] = Sector()._list(0)
#                 response['status'] = '00'
#             elif int(apidata['status']) == 1:
#                 if len(apidata['name'].strip()) > 0 and len(apidata['uid'].strip()) > 0:
#
#                     if Sector.query.filter_by(name=apidata['name'].lower()).count() != 0:
#                         response['status'] = '50'
#                         response['message'] = 'Maaf Sector dengan nama ini sudah terdaftar.'
#                     elif Sector.query.filter_by(uid=apidata['uid'].lower()).count() != 0:
#                         response['status'] = '50'
#                         response['message'] = 'Maaf sector dengan uid ini sudah terdaftar.'
#                     else:
#                         response['data'] = Sector()._insert(apidata['name'], apidata['uid'].strip().lower().replace(' ', '-'))
#                         response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 2:
#                 if len(apidata['id'].strip()) > 0:
#                     response['data'] = Sector().sector_data(apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 3:
#                 if len(apidata['_id'].strip()) > 0 and len(apidata['name'].strip()) > 0 and \
#                         len(apidata['uid'].strip()) > 0:
#                     if Sector.query.filter_by(uid=apidata['uid'].lower()).filter(Sector.id != int(apidata['_id'])).count() == 0:
#                         response['data'] = Sector()._update(apidata['_id'], apidata['name'], apidata['uid'].strip().lower().replace(' ', '-'))
#                         response['status'] = '00'
#                     else:
#                         response['status'] = '50'
#                         response['message'] = 'Maaf Sector dengan uid ini sudah terdaftar.'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Isi semua field dengan benar.'
#             elif int(apidata['status']) == 4:
#                 response['data'] = Sector()._remove(apidata['_id'])
#                 response['status'] = '00'
#             else:
#                 response['status'] = '50'
#                 response['message'] = 'Your credential are invalid.'
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))
#
# @admin.route('/api/v1/ams/menus', methods=['POST', 'GET'])
# @csrf.exempt
# def _api_menus():
#     # ip_list = request.environ['HTTP_X_FORWARDED_FOR']
#     # user_log('/', ip_list)
#     if request.method == 'POST':
#         apidata = request.form
#         print(apidata)
#         response = {}
#         user = User.query.filter_by(id=apidata['id']).first()
#         if user is not None and user.verify_token(apidata['token']):
#             sector_id = None
#             if int(apidata['sector_id']) > 0:
#                 sector_id = int(apidata['sector_id'])
#             if int(apidata['status']) == 0:
#                 response['data'] = nav_list()._nav_menu(sector_id)
#                 response['status'] = '00'
#             elif int(apidata['status']) == 1:
#                 if len(apidata['name']) > 0:
#                     _nav = nav_list()
#                     _nav.name = apidata['name']
#                     _nav.parent_status = True if apidata['parent_status'] == 'true' else False
#                     _nav.sector_id = sector_id
#                     _nav.uid = apidata['slug'].strip().lower().replace(' ', '-')
#                     if _nav.parent_status is True:
#                         _nav.uid = None
#                     db.session.add(_nav)
#                     db.session.commit()
#                     response['id'] = _nav.id
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'The field name cannot be empty.'
#             elif int(apidata['status']) == 2:
#                 if len(apidata['id'].strip()) > 0:
#                     response['data'] = nav_list()._data(apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 3:
#                 if len(apidata['_id'].strip()) > 0:
#                     _nav = nav_list.query.filter_by(id=int(apidata['_id']), status=True).first()
#                     _nav.name = apidata['name']
#                     _nav.parent_status = True if apidata['parent_status'] == 'true' else False
#                     _nav.uid = apidata['slug'].strip().lower().replace(' ', '-')
#                     if _nav.parent_status is True:
#                         _nav.uid = None
#                     db.session.add(_nav)
#                     db.session.commit()
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 4:
#                 if len(apidata['id'].strip()) > 0:
#                     response['data'] = nav_list()._data(apidata['parent_id'])
#                     response['submenu_list'] = nav_list()._nav_submenu(apidata['sector_id'], apidata['parent_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 5:
#                 if len(apidata['_id'].strip()) > 0:
#                     _nav = nav_list.query.filter_by(id=int(apidata['_id']), status=True).first()
#                     _nav.status = False
#                     db.session.commit()
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 6:
#                 response['data'] = nav_list()._nav_submenu(sector_id, apidata['parent_id'])
#                 response['parent'] = nav_list()._data(apidata['parent_id'])
#                 response['status'] = '00'
#             elif int(apidata['status']) == 7:
#                 if len(apidata['name']) > 0:
#                     if nav_list().query.filter_by(parent_id=int(apidata['parent_id']), sector_id=sector_id, status=True, uid=apidata['slug'].lower().replace(' ', '-')).count() == 0:
#                         _nav = nav_list()
#                         _nav.name = apidata['name']
#                         _nav.uid = apidata['slug'].strip().lower().replace(' ', '-')
#                         _nav.sector_id = sector_id
#                         _nav.parent_id = apidata['parent_id']
#                         _nav.type = 2
#                         db.session.add(_nav)
#                         db.session.commit()
#                         response['id'] = _nav.id
#                         response['status'] = '00'
#                     else:
#                         response['status'] = '50'
#                         response['message'] = 'The field name cannot be empty.'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'The field name cannot be empty.'
#             elif int(apidata['status']) == 8:
#                 if len(apidata['_id'].strip()) > 0:
#                     response['data'] = nav_list()._data(apidata['_id'])
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#             elif int(apidata['status']) == 9:
#                 if len(apidata['_id'].strip()) > 0:
#                     _nav = nav_list.query.filter_by(id=int(apidata['_id']), status=True).first()
#                     _nav.name = apidata['name']
#                     _nav.uid = apidata['slug'].lower().replace(' ', '-')
#                     db.session.add(_nav)
#                     db.session.commit()
#                     response['status'] = '00'
#                 else:
#                     response['status'] = '50'
#                     response['message'] = 'Your credential are invalid.'
#
#         else:
#             response['status'] = '50'
#             response['message'] = 'Your credential are invalid.'
#         return jsonify(response)
#     else:
#         return redirect(url_for('main.index'))
