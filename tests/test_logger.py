#! usr/bin/env python

"""
@author:liqing
@email:626924971@qq.com
@tel:18674450812
@version:v1.0
function:set log
"""

import logging
import logging.config

logging.config.fileConfig("../configures/log/logger.conf")
logger = logging.getLogger(__name__)

logger.debug("test logger")
logger.info("test logger")
logger.warn("test logger")
logger.error("test logger")

