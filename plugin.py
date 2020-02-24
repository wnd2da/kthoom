# -*- coding: utf-8 -*-
#########################################################
# 고정영역
#########################################################
# python
import os
import sys
import traceback
import json

# third-party
from flask import Blueprint, request, render_template, redirect, jsonify, send_from_directory
from flask_login import login_required

# sjva 공용
from framework.logger import get_logger
from framework import path_app_root

            
# 패키지
package_name = __name__.split('.')[0]
logger = get_logger(package_name)

from .model import ModelSetting
from .logic import Logic
from .logic_normal import LogicNormal

blueprint = Blueprint(package_name, package_name, url_prefix='/%s' %  package_name, template_folder=os.path.join(os.path.dirname(__file__), 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'kthoom'), static_url_path='kthoom')

def plugin_load():
    Logic.plugin_load()

def plugin_unload():
    Logic.plugin_unload()

plugin_info = {
    'version' : '0.1.0',
    'name' : 'KTHOOM 만화 뷰어',
    'category_name' : 'service',
    'icon' : '',
    'developer' : 'soju6jan',
    'description' : 'KTHOOM 만화 뷰어',
    'home' : 'https://github.com/soju6jan/kthoom',
    'more' : '',
}
#########################################################

# 메뉴 구성.
menu = {
    'main' : [package_name, 'KTHOOM 만화 뷰어'],
    'sub' : [
        ['setting', '설정'], ['viewer', '뷰어'], ['log', '로그']
    ], 
    'category' : 'service',
}  

#########################################################
# WEB Menu
#########################################################
@blueprint.route('/')
def home():
    return redirect('/%s/viewer' % package_name)
    
@blueprint.route('/<sub>')
@login_required
def first_menu(sub): 
    arg = ModelSetting.to_dict()
    arg['package_name']  = package_name
    if sub == 'setting':
        return render_template('%s_%s.html' % (package_name, sub), arg=arg)
    elif sub == 'kthoom':
        return blueprint.send_static_file('index.html')
    elif sub == 'viewer':
        site = "/%s/kthoom?bookUri=dp" % (package_name)
        return render_template('iframe.html', site=site)
    elif sub == 'log':
        return render_template('log.html', package=package_name)
    return render_template('sample.html', title='%s - %s' % (package_name, sub))

#########################################################
# For UI (보통 웹에서 요청하는 정보에 대한 결과를 리턴한다.)
#########################################################
@blueprint.route('/ajax/<sub>', methods=['GET', 'POST'])
@login_required
def ajax(sub):
    logger.debug('AJAX %s %s', package_name, sub)
    try:
        if sub == 'setting_save':
            ret = ModelSetting.setting_save(request)
            return jsonify(ret)
        elif sub == 'zip_list':
            ret = LogicNormal.get_zip_list()
            return jsonify(ret)
    except Exception as e: 
        logger.error('Exception:%s', e)
        logger.error(traceback.format_exc())  
        return jsonify('fail')   

#########################################################
# kthroom
#########################################################
@blueprint.route('/code/<path:path>', methods=['GET', 'POST'])
def kthroom(path):
    return blueprint.send_static_file('code/' + path)

@blueprint.route('/images/<path:path>', methods=['GET', 'POST'])
def kthroom_images(path):
    return blueprint.send_static_file('images/' + path)

@blueprint.route('/examples/<path:path>', methods=['GET', 'POST'])
def kthroom_examples(path):
    return blueprint.send_static_file('examples/' + path)

@blueprint.route('/dp/<path:path>', methods=['GET', 'POST'])
def kthroom_dp(path):
    path = '/%s' % path
    real_path = path.replace(path_app_root, '')[1:].replace('\\', '/')
    #logger.debug('load:%s', real_path)
    return send_from_directory('', real_path)
