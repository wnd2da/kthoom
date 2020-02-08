# -*- coding: utf-8 -*-
#########################################################
# python
import os
import sys
import traceback
import logging
import time

# third-party

# sjva 공용
from framework import db, scheduler, path_data
from framework.job import Job
from framework.util import Util

# 패키지
from .plugin import package_name, logger
from .model import ModelSetting

#########################################################


class Logic(object):
    db_default = {
        'db_version' : '1',
        #'library_path' : '%s|%s' % (os.path.join(path_data, 'manamoa'), os.path.join(path_data, 'webtoon_naver'))
        'library_path' : ''
    }

    @staticmethod
    def db_init():
        try:
            for key, value in Logic.db_default.items():
                if db.session.query(ModelSetting).filter_by(key=key).count() == 0:
                    db.session.add(ModelSetting(key, value))
            db.session.commit()
            Logic.migration()
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())


    @staticmethod
    def plugin_load():
        try:
            logger.info('%s plugin_load', package_name)
            Logic.db_init()
            # 편의를 위해 json 파일 생성
            from plugin import plugin_info
            Util.save_from_dict_to_json(plugin_info, os.path.join(os.path.dirname(__file__), 'info.json'))
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())


    @staticmethod
    def plugin_unload():
        try:
            logger.debug('%s plugin_unload', package_name)
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())
    
    @staticmethod
    def migration():
        try:
            pass
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())
    

    # 기본 구조 End
    ##################################################################

    