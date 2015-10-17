# -*- encoding:utf8 -*-
from entry import app
import logging
if app.config['DEBUG'] == False:

    print "LOGGING MODULE INIT AS RELEASE MODE"
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('log/server_info.log')
    fh.setLevel(logging.INFO)

    # 再创建一个handler，用于输出到控制台
    ch = logging.FileHandler('log/server_warn.log')
    ch.setLevel(logging.WARN)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)
else:
    print "LOGGING MODULE INIT AS DEBUG MODE (ONLY CONSOLE)"

    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(ch)

