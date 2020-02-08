# -*- coding: utf-8 -*-
#########################################################
# python
import os
import sys
import traceback

# third-party

# sjva 공용
from framework import db, scheduler, path_data
from framework.job import Job
from framework.util import Util

# 패키지
import system
from .plugin import package_name, logger
from .model import ModelSetting

class LogicNormal(object):
    @staticmethod
    def get_zip_list():
        try:
            ret = []
            download_path = ModelSetting.get('library_path')
            download_paths = download_path.split('|')
            logger.debug(download_paths)
            for d in download_paths:
                ret = LogicNormal.explorer(d.strip(), ret)
            for r in ret:
                logger.debug(r)
            return ret
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    @staticmethod
    def explorer(dirname, ret):
        if os.path.exists(dirname) and os.path.isdir(dirname):
            tmp = os.listdir(dirname)
            for t in tmp:
                name = os.path.join(dirname, t)
                if os.path.isdir(name):
                    LogicNormal.explorer(name, ret)
                else:
                    if os.path.isfile(name) and name.endswith('.zip'):
                        ret.append('dp%s' % name)
        return ret