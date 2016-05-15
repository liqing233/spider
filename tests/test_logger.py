#! usr/bin/env python

"""
@author:liqing
@email:626924971@qq.com
@tel:18674450812
@version:v1.0
function:set log
"""

import sys
sys.path.append("../../../")
import logging
import logging.config
from logging.handlers import RotatingFileHandler

RThandler = RotatingFileHandler('../logs/spider.log', maxBytes=10*1024*1024,backupCount=5)
logging.config.fileConfig("../configures/log/logger.conf")
logger = logging.getLogger(__name__).addHandler(RThandler)

logger.debug("test logger")
logger.info("test logger")
logger.warn("test logger")
logger.error("test logger")

