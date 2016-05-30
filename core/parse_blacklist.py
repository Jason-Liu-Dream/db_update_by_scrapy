#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
parse_blacklist.py

Author: Jason liu
Date: 2016-04-25
"""
import codecs
import os
import sys
import logging
import logging.config
import MySQLdb
import settings

reload(sys)
sys.setdefaultencoding('utf-8')

logging.config.fileConfig("logging.conf")  # 选定配置文件

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 数据库方法
def run():
    """生成黑名单信息保存到数据库中。"""
    # 创建一个日志记录器
    black_logger = logging.getLogger('black')
    black_logger.info('Loading log modules success!')
    try:
        json_path = os.path.join(BASE_PATH, 'file/keyword.list')
        result_file = codecs.open(json_path, mode='rb', encoding='utf-8')
    except Exception as msg:
        result_file.close()
        black_logger.error(msg)
    else:
        result_list = []
        for line in result_file:
            result_list.append(line)
        result_file.close()
        value_list = []
        for result in result_list:
            result = result.strip('\r\n').split('\t')
            value_list.append((result[0], int(result[1]), result[0]))
        value_list = list(set(value_list))

    black_logger.info('parse list result success!')

    """
    开始执行数据库操作
    """
    # 打开数据库连接
    db = MySQLdb.connect(settings.HOST, settings.USER, settings.PASSWORD, settings.DBNAME, charset="utf8")
    # 获取数据库游标
    cursor = db.cursor()
    # 清空黑名单数据库语句
    clear_sql = """truncate table tb_MDarkKeywords"""
    # 执行黑名单数据库清除工作
    try:
        # 执行语句
        cursor.execute(clear_sql)
        # 提交语句
        db.commit()
    except Exception as msg:
        # 失败则回滚，并且输出错误日志
        db.rollback()
        black_logger.error(msg)
    else:
        black_logger.info('Clear blacklist table success!')
    
    # 插入黑名单数据语句
    insert_sql = """insert into tb_MDarkKeywords(DarkKeyword, KeywordCategory)
                    select %s, %s from dual where not exists
                    (select * from tb_MDarkKeywords where DarkKeyword = %s)"""
    try:
        # 执行语句
        cursor.executemany(insert_sql, value_list)
        db.commit()
    except Exception as msg:
        db.rollback()
        black_logger.error(msg)
    else:
        cursor.close()
        db.close()
        black_logger.info('Update blacklist success!')

    black_logger.disabled = True


if __name__ == "__main__":
    run()
