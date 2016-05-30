#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
parse_whitelist.py

Author: Jason liu
Date: 2016-04-25
"""
import codecs
import json
import logging
import logging.config
import os
import sys
import MySQLdb
import time
import settings
from core.url_parser import url_object
from core.spider_run import run_spiders

reload(sys)
sys.setdefaultencoding('utf-8')

logging.config.fileConfig("logging.conf")  # 选定配置文件

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run():
    """生成白名单信息保存到数据库中。"""
    json_path = os.path.join(BASE_PATH, 'file/chinaz.json')  # 获取指定文件的目录信息

    # 创建一个日志记录器
    white_logger = logging.getLogger('white')
    white_logger.info('Loading log modules success!')

    modify_time = os.path.getctime(json_path)
    now_time = time.time()

    # 检测中间文件的修改时间距离今天的修改时间大于7天，则执行爬虫，否则直接分析文件
    if now_time - modify_time >= 7 * 24 * 60 * 60:
        white_logger.info('Begin to running spider!')
        run_spiders()
        white_logger.info('Spider close success!')
    try:
        result_file = codecs.open(json_path, mode='rb', encoding='utf-8')
    except Exception as msg:
        result_file.close()
        white_logger.error(msg)
    else:
        result_list = []
        for line in result_file:
            result_list.append(line)
        result_file.close()
        value_list = []
        for result in result_list:
            try:
                result = json.loads(result)
            except Exception as msg:
                white_logger.error(msg)
                continue
            else:
                domain = result['web_url']
                try:
                    root_domain = url_object(domain).getRootDomain
                except Exception as msg:
                    white_logger.error(msg)
                    continue
                else:
                    title = result['web_title']
                    value_list.append((domain, title, root_domain))
        value_list = list(set(value_list))

    white_logger.info('parse json result success!')

    """
    开始执行数据库操作
    """
    # 打开数据库连接
    db = MySQLdb.connect(settings.HOST, settings.USER, settings.PASSWORD, settings.DBNAME, charset="utf8")
    # 获取数据库游标
    cursor = db.cursor()
    # 清空白名单数据库语句
    clear_sql = """truncate table tb_MDarkWhites"""
    # 执行白名单数据库清除工作
    try:
        # 执行语句
        cursor.execute(clear_sql)
        # 提交语句
        db.commit()
    except Exception as msg:
        # 失败则回滚，并且输出错误日志
        db.rollback()
        white_logger.error(msg)
    else:
        white_logger.info('Clear whitelist table success!')

    # 插入白名单数据语句
    insert_sql = """insert into tb_MDarkWhites(WhiteUrl, UrlTitle, RootDomain) values (%s, %s, %s)"""
    try:
        # 执行语句
        cursor.executemany(insert_sql, value_list)
        db.commit()
    except Exception as msg:
        db.rollback()
        white_logger.error(msg)
    else:
        cursor.close()
        db.close()
        white_logger.info('Update whitelist success!')

    white_logger.disabled = True


if __name__ == "__main__":
    run()
